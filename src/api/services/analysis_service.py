"""
Analysis service — calls OpenRouter to perform QA analysis on a cleaned call
transcript and produces a report JSON file.

Flow:
  1. Load system prompt from config/analysis_prompt.md.
  2. Build user message: cleaned transcript + course CSV + incident level defs.
  3. Call OpenRouter via the openai SDK (OpenAI-compatible endpoint).
  4. Parse and validate the JSON response against the expected report schema.
  5. Save to output/<stem>.report.json and return the path.

On JSON parse failure the service retries once with a corrective prompt. If
the second attempt also fails, it saves the raw LLM response to
output/<stem>.raw_llm_response.txt for debugging and raises RuntimeError.

Model selection is per-call — any model supported by OpenRouter can be used
by passing its model string (e.g. "anthropic/claude-3-5-sonnet",
"openai/gpt-4o", "google/gemini-pro").
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Generous ceiling. The compliance report is long by design; running out of
# room here is far more expensive than the unused headroom, because a truncated
# response costs a full call and yields nothing.
MAX_OUTPUT_TOKENS = 16000

# Derive incidents from checklist FAILs rather than trusting the model's
# separate incident list. Set to "0" to fall back to the model's own list.
DERIVE_INCIDENTS_FROM_CHECKLIST = os.environ.get(
    "DERIVE_INCIDENTS_FROM_CHECKLIST", "1") == "1"

_ANALYSIS_PROMPT_PATH = _PROJECT_ROOT / "config" / "analysis_prompt.md"
_INCIDENT_LEVELS_PATH = _PROJECT_ROOT / "config" / "incident_levels.md"
_GROUND_TRUTH_PATH = _PROJECT_ROOT / "config" / "accredian_ground_truth.yaml"



# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------
# Three separate sources of run-to-run drift, all of which have to be closed:
#
# 1. Sampling. temperature must be exactly 0, not 0.1. At 0.1 a borderline
#    "is this an L2 or not" call flips between runs, and each L2 is worth 7
#    points — enough to move a report a full grade.
#
# 2. Provider routing. OpenRouter resolves one model string to whichever
#    provider is cheapest/fastest right now, and those differ in quantisation
#    and serving stack. Same prompt, different backend, different output. Pin
#    the provider and disable fallbacks so a run is reproducible.
#
# 3. Seed. Honoured by some providers, ignored by others. Free when supported.
OPENROUTER_PROVIDER_ORDER = os.environ.get("OPENROUTER_PROVIDER_ORDER", "").strip()
DETERMINISTIC_SEED = int(os.environ.get("LLM_SEED", "20260101"))


def _determinism_kwargs() -> dict:
    """Extra body params that pin the run as far as the provider allows."""
    extra: dict = {}
    if OPENROUTER_PROVIDER_ORDER:
        extra["provider"] = {
            "order": [p.strip() for p in OPENROUTER_PROVIDER_ORDER.split(",") if p.strip()],
            "allow_fallbacks": False,
        }
    return extra


def _load_system_prompt() -> str:
    if not _ANALYSIS_PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"Analysis prompt not found: {_ANALYSIS_PROMPT_PATH}"
        )
    return _ANALYSIS_PROMPT_PATH.read_text(encoding="utf-8")


def _slim_yaml(text: str) -> str:
    """Strip comments and blank lines before sending a config to the model.

    accredian_ground_truth.yaml is written to be maintained by a person, so
    roughly half of it is explanation of why the lists exist and how to keep
    them current. The model needs the lists, not the rationale — the rules that
    act on them live in the system prompt. Same treatment the rubric gets.
    """
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Trailing comment, but a '#' inside a quoted scalar is data, not a
        # comment — `- "#\s*1"` is a real pattern in the ranking config. Track
        # quote state and require the leading space YAML demands of an inline
        # comment, rather than testing quote parity, which a line like that one
        # passes while still being entirely inside a string.
        quote = ""
        cut = -1
        for i, ch in enumerate(line):
            if quote:
                if ch == quote:
                    quote = ""
            elif ch in "\"'":
                quote = ch
            elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
                cut = i
                break
        if cut >= 0:
            line = line[:cut].rstrip()
            if not line.strip():
                continue
        out.append(line)
    return "\n".join(out)


def _build_user_message(
    cleaned_vtt_path: str,
    course_path: str,
    sales_pitch_path: str | None = None,
) -> str:
    transcript = Path(cleaned_vtt_path).read_text(encoding="utf-8", errors="replace")
    course_data = Path(course_path).read_text(encoding="utf-8", errors="replace")
    incident_levels = _INCIDENT_LEVELS_PATH.read_text(encoding="utf-8")

    msg = (
        "## Cleaned Transcript\n\n"
        f"{transcript}\n\n"
        "## Course Offering Data\n\n"
        f"{course_data}\n\n"
    )

    # Company-wide facts the course CSV cannot carry: the closed partner list,
    # verified rankings, and what the credential is NOT equivalent to. Without
    # this section a fabricated partnership or an inflated ranking has nothing
    # to contradict, so the model correctly passes it.
    if _GROUND_TRUTH_PATH.exists():
        ground_truth = _slim_yaml(_GROUND_TRUTH_PATH.read_text(encoding="utf-8"))
        msg += "## Accredian Ground Truth\n\n```yaml\n" + ground_truth + "\n```\n\n"
    else:
        print(f"[analysis] WARNING: {_GROUND_TRUTH_PATH.name} not found — "
              f"partner, ranking and credential-equivalence checks will not "
              f"have anything to verify against.", flush=True)

    msg += "## Incident Level Definitions\n\n" + incident_levels + "\n\n"

    if sales_pitch_path and Path(sales_pitch_path).exists():
        sales_pitch_data = Path(sales_pitch_path).read_text(encoding="utf-8", errors="replace")
        msg += "## Sales Pitch\n\n" + sales_pitch_data + "\n\n"

    msg += (
        "Analyze the transcript against the course data, the ground truth and "
        "the incident definitions. Return only the JSON report object."
    )
    return msg


def _call_openrouter(
    system_prompt: str,
    user_message: str,
    model: str,
) -> tuple[str, dict]:
    """Call OpenRouter and return the raw text response and token usage."""
    from openai import OpenAI

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your .env file."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            # OpenRouter recommends identifying your app.
            "HTTP-Referer": "https://accredian.com",
            "X-Title": "Accredian Call Quality Agent",
        },
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,   # exactly 0 — see the Determinism note above
        # Set explicitly. Without it OpenRouter applies the model's default,
        # which is 4096 on several models — well under what this report needs
        # (35-item checklist + incidents + sales intelligence + score is
        # routinely 5-8k output tokens on a long call). The response then gets
        # cut mid-JSON and every parse fails.
        max_tokens=MAX_OUTPUT_TOKENS,
        seed=DETERMINISTIC_SEED,
        extra_body=_determinism_kwargs(),
    )

    finish_reason = getattr(response.choices[0], "finish_reason", None)
    usage = response.usage
    usage_dict = {
        "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
        "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
        "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
    }

    usage_dict["finish_reason"] = finish_reason
    return response.choices[0].message.content or "", usage_dict


def _repair_truncated_json(text: str) -> dict | None:
    """Recover a usable report from a response cut off at the token limit.

    Naive bracket-closing fails on the most common cut point — mid-string —
    because it leaves a half-written object behind. Instead, scan forward
    tracking string state and bracket depth, remember the last position where
    the document was structurally complete (just after a closed element), then
    rewind to it and close whatever is still open.

    The result is the report minus however many trailing checklist items or
    incidents were lost, which is far better than discarding the whole call.
    """
    stack: list[str] = []
    in_string = False
    escaped = False
    # (index_after_char, depth_at_that_point)
    safe: list[tuple[int, int]] = []

    for i, ch in enumerate(text):
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            if not in_string:
                safe.append((i + 1, len(stack)))
            continue
        if in_string:
            continue
        if ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]":
            if stack:
                stack.pop()
            safe.append((i + 1, len(stack)))
        elif ch in "0123456789" and not in_string:
            pass

    # Walk back through candidate cut points until one parses.
    for cut, _depth in reversed(safe[-400:]):
        head = text[:cut].rstrip().rstrip(",")
        # Recompute what is still open at this cut.
        st: list[str] = []
        ins = False
        esc = False
        for ch in head:
            if esc:
                esc = False
                continue
            if ch == "\\" and ins:
                esc = True
                continue
            if ch == '"':
                ins = not ins
                continue
            if ins:
                continue
            if ch in "{[":
                st.append("}" if ch == "{" else "]")
            elif ch in "}]" and st:
                st.pop()
        if ins:
            continue
        candidate = head + "".join(reversed(st))
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict) and obj:
                return obj
        except json.JSONDecodeError:
            continue
    return None


def _parse_json_response(raw: str) -> dict:
    """
    Attempt to parse the LLM response as JSON.

    The model may wrap the object in markdown fences even when asked not to.
    We strip those before parsing.
    """
    text = raw.strip()

    # Strip ```json ... ``` fences if present.
    if text.startswith("```"):
        lines = text.splitlines()
        # Drop first and last fence lines.
        inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        text = "\n".join(inner).strip()

    return json.loads(text)


def _inject_metadata(
    report: dict,
    *,
    cleaned_vtt_path: str,
    call_id: str | None,
    call_recording_file: str | None,
    call_stt_file: str | None,
    sales_rep_name: str | None,
    sales_rep_id: str | None,
    customer_name: str | None,
    call_duration: str | None,
    no_of_words: int | None,
    stats: dict | None,
    usage: dict | None = None,
) -> dict:
    """
    Overwrite top-level metadata fields with values from the pipeline context.
    The LLM fills these in from the transcript, but the pipeline has the
    authoritative values from clean.py stats and submit arguments.
    """
    if call_id is not None:
        report["call_id"] = call_id
    if call_recording_file is not None:
        report["call_recording_file"] = call_recording_file
    if call_stt_file is not None:
        report["call_stt_file"] = call_stt_file
    if sales_rep_name is not None:
        report["sales_rep_name"] = sales_rep_name
    if sales_rep_id is not None:
        report["sales_rep_id"] = sales_rep_id
    if customer_name is not None:
        report["customer_name"] = customer_name
        if "report" in report:
            report["report"]["customer"] = customer_name
    if call_duration is not None:
        report["call_duration"] = call_duration
    if no_of_words is not None:
        report["no_of_words"] = no_of_words

    # Inject analysis date
    if "report" in report:
        report["report"]["analysis_date"] = date.today().isoformat()
        report["report"]["transcript_file"] = Path(cleaned_vtt_path).name

    # Overwrite call_statistics from authoritative stats dict when available.
    if stats and "report" in report:
        cs = report["report"].setdefault("call_statistics", {})
        cs["duration_seconds"] = int(stats.get("duration_sec", 0))
        cs["total_words"] = stats.get("total_words", 0)
        cs["rep_words"] = stats.get("rep_words", 0)
        cs["customer_words"] = stats.get("customer_words", 0)
        total = cs["total_words"] or 1
        cs["rep_talk_ratio_pct"] = round(cs["rep_words"] / total * 100, 1)
        cs["sales_rep_utterances"] = stats.get("rep_utterances", 0)
        cs["customer_utterances"] = stats.get("customer_utterances", 0)
        cs["transcript_tokens"] = stats.get("estimated_tokens", 0)

        if usage:
            cs["input_tokens"] = usage.get("prompt_tokens", 0)
            cs["output_tokens"] = usage.get("completion_tokens", 0)
            cs["total_tokens"] = usage.get("total_tokens", 0)
            report["tokens_utilized"] = usage.get("total_tokens", 0)

    return report


def run_analysis(
    pipeline_id: str,
    cleaned_vtt_path: str,
    course_path: str,
    model: str,
    sales_pitch_path: str | None = None,
    *,
    call_id: str | None = None,
    call_recording_file: str | None = None,
    call_stt_file: str | None = None,
    sales_rep_name: str | None = None,
    sales_rep_id: str | None = None,
    customer_name: str | None = None,
    call_duration: str | None = None,
    no_of_words: int | None = None,
    stats: dict | None = None,
) -> dict[str, Any]:
    """
    Run OpenRouter QA analysis on a cleaned transcript.

    Returns:
        {
          "report_json_path": str,
          "model_used": str,
          "tokens_utilized": int,
        }

    Raises:
        RuntimeError if the LLM fails to return valid JSON after two attempts.
    """
    system_prompt = _load_system_prompt()
    user_message = _build_user_message(cleaned_vtt_path, course_path, sales_pitch_path)

    # --- First attempt ---
    raw, usage = _call_openrouter(system_prompt, user_message, model)
    truncated = usage.get("finish_reason") == "length"

    try:
        report = _parse_json_response(raw)
    except json.JSONDecodeError:
        if truncated:
            # A corrective prompt cannot help here: the model did not
            # misunderstand the format, it ran out of room. Re-prompting adds
            # input tokens and leaves the ceiling untouched, so the second call
            # fails identically and doubles the cost and the wall-clock time.
            # Try to salvage the partial document instead.
            report = _repair_truncated_json(raw.strip().removeprefix("```json").removeprefix("```"))
            if report is None:
                stem = Path(cleaned_vtt_path).stem.replace(".cleaned", "")
                output_dir = _PROJECT_ROOT / "data" / "output" / pipeline_id / "report"
                output_dir.mkdir(parents=True, exist_ok=True)
                raw_path = output_dir / f"{stem}.raw_llm_response.txt"
                raw_path.write_text(raw, encoding="utf-8")
                raise RuntimeError(
                    f"Analysis response was TRUNCATED at the model's output limit "
                    f"({usage.get('completion_tokens')} completion tokens, "
                    f"max_tokens={MAX_OUTPUT_TOKENS}) and could not be repaired. "
                    f"Raise MAX_OUTPUT_TOKENS or shorten the report schema. "
                    f"Raw response saved to {raw_path}"
                )
            print(
                f"[analysis] WARNING: response truncated at "
                f"{usage.get('completion_tokens')} tokens; recovered a partial "
                f"report by closing open structures. Some checklist items or "
                f"incidents are likely missing. Raise MAX_OUTPUT_TOKENS.",
                flush=True,
            )
        else:
            # Genuine format problem — a corrective prompt is the right fix.
            correction_message = (
                "Your previous response was not valid JSON. "
                "Return only the raw JSON object — no markdown, no explanation, no fences."
            )
            raw, usage2 = _call_openrouter(
                system_prompt, user_message + "\n\n" + correction_message, model
            )
            usage = {k: (usage.get(k, 0) + usage2.get(k, 0)) if isinstance(usage2.get(k), int)
                     else usage2.get(k) for k in usage2}
            try:
                report = _parse_json_response(raw)
            except json.JSONDecodeError as exc:
                stem = Path(cleaned_vtt_path).stem.replace(".cleaned", "")
                output_dir = _PROJECT_ROOT / "data" / "output" / pipeline_id / "report"
                output_dir.mkdir(parents=True, exist_ok=True)
                raw_path = output_dir / f"{stem}.raw_llm_response.txt"
                raw_path.write_text(raw, encoding="utf-8")
                raise RuntimeError(
                    f"OpenRouter returned invalid JSON after two attempts "
                    f"(finish_reason={usage.get('finish_reason')}). "
                    f"Raw response saved to {raw_path}"
                ) from exc

    # Replace the model's free-form incident list with one derived from the
    # checklist. The checklist is 39 fixed decisions made in a fixed order on
    # every run; open-ended incident discovery is a recall task over the whole
    # transcript, and recall is the least reproducible thing an LLM does. This
    # makes incident detection inherit the checklist's stability.
    if DERIVE_INCIDENTS_FROM_CHECKLIST:
        try:
            from src.incidents import reconcile
            before = len(report.get("report", {}).get("incidents") or [])
            reconcile(report)
            after = len(report.get("report", {}).get("incidents") or [])
            if before != after:
                print(f"[analysis] incidents reconciled from checklist: "
                      f"{before} reported -> {after} derived", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[analysis] WARNING: incident reconciliation failed ({exc}); "
                  f"keeping the model's list", flush=True)

    # Inject pipeline-authoritative metadata.
    report = _inject_metadata(
        report,
        cleaned_vtt_path=cleaned_vtt_path,
        call_id=call_id,
        call_recording_file=call_recording_file,
        call_stt_file=call_stt_file,
        sales_rep_name=sales_rep_name,
        sales_rep_id=sales_rep_id,
        customer_name=customer_name,
        call_duration=call_duration,
        no_of_words=no_of_words,
        stats=stats,
        usage=usage,
    )

    # Enforce optional sales pitch fields are null if no sales pitch was provided.
    has_sales_pitch = bool(sales_pitch_path and Path(sales_pitch_path).exists())
    if not has_sales_pitch and "report" in report:
        report["report"]["overall_call_score"] = None
        report["report"]["sales_pitch_coverage"] = None

    # Save report JSON.
    stem = Path(cleaned_vtt_path).stem.replace(".cleaned", "")
    output_dir = _PROJECT_ROOT / "data" / "output" / pipeline_id / "report"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{stem}.report.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    tokens_utilized = (
        report.get("tokens_utilized")
        or report.get("report", {}).get("call_statistics", {}).get("total_tokens")
        or 0
    )

    return {
        "report_json_path": str(out_path),
        "model_used": model,
        "tokens_utilized": tokens_utilized,
    }
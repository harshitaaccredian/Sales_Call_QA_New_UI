"""
Derive incidents from the compliance checklist.

The consistency problem
-----------------------
`analysis_prompt.md` asks the model to do two different things:

  1. Walk a FIXED 36-item checklist, in a fixed order, marking PASS / FAIL /
     NOT_DISCUSSED with evidence.
  2. Separately "identify incidents where the rep misrepresented details".

The first is stable: the same 36 decisions get made on every run, so run-to-run
differences are limited to individual verdicts flipping.

The second is not. It is an open-ended recall task over a 5,000-word transcript
with no fixed decision set, so nothing forces run 2 to examine the same moments
run 1 examined. Recall is the least reproducible thing an LLM does, and each
missed L2 is 7 points plus a cap change.

This module removes task 2 entirely. Every checklist FAIL *is* an incident, and
severity comes from a lookup table rather than a second model judgment. Incident
detection then inherits the checklist's stability, which is the same property
that already makes the methodology scoring reproducible.

Two variable judgments become one.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_severity_map(config_dir: Path | str | None = None) -> dict:
    d = Path(config_dir) if config_dir else CONFIG_DIR
    return yaml.safe_load((d / "incident_severity_map.yaml").read_text(encoding="utf-8"))


def _severity_for(category: str, item: str, smap: dict) -> str:
    """Look up severity by item first, then category, then the default.

    Item-level overrides exist because severity is not uniform inside a
    category: under Career & Placement, a placement *guarantee* is an L3
    fabrication while imprecise career-assistance wording is an L1.
    """
    overrides = smap.get("item_overrides", {})
    for pattern, sev in overrides.items():
        if pattern.lower() in item.lower():
            return sev
    return smap.get("categories", {}).get(category, smap.get("default", "L1"))


def derive_incidents(report: dict, config_dir: Path | str | None = None) -> list[dict]:
    """Build the incident list from checklist FAILs.

    Reads `report.report.checklist` and returns incidents in checklist order,
    so ids are stable across runs too — run 1 and run 2 number the same
    violation identically, which matters when diffing reports.
    """
    smap = load_severity_map(config_dir)
    node = report.get("report", report)
    checklist = node.get("checklist") or []

    incidents: list[dict] = []
    for row in checklist:
        status = str(row.get("status", "")).upper()
        if status not in ("FAIL", "VIOLATION", "INCORRECT"):
            continue

        # The schema calls this field `item`; earlier prompt revisions emitted
        # `check`. Accept both so a report produced by either never silently
        # loses its item text — an empty item would fall through every
        # item_override and get the category default severity.
        item = str(row.get("item") or row.get("check") or "").strip()
        category = (row.get("category") or item.split(":")[0]).strip() or "Uncategorised"

        evidence = row.get("evidence") or row.get("what_rep_said")
        reason = row.get("reason") or row.get("why_incident")
        correct = row.get("correct_information") or row.get("what_is_correct")

        # Field names must match what the report renders, which is the model's
        # own incident schema from analysis_prompt.md:
        #   transcript_quote / what_rep_said / violation_basis / what_is_correct
        # Emitting correct_information and why_incident instead left the
        # "Official course data" panel and the "Violation grounds" line blank on
        # every derived incident. The older names are kept as aliases so any
        # other consumer that already reads them keeps working.
        incidents.append({
            "id": len(incidents) + 1,
            "severity": _severity_for(category, item, smap),
            "category": f"{category} — {item}" if item else category,
            "checklist_item": item,
            "timestamp": row.get("timestamp"),
            "incident_ref": row.get("incident_ref"),
            "transcript_quote": evidence,
            "what_rep_said": evidence,
            "violation_basis": reason,
            "what_is_correct": correct,
            # aliases
            "why_incident": reason,
            "correct_information": correct,
            "derived_from_checklist": True,
        })

    return incidents


def reconcile(report: dict, config_dir: Path | str | None = None) -> dict:
    """Replace the model's incident list with the derived one, in place.

    Keeps the model's richer prose where it supplied a matching incident, but
    the SET of incidents and their severities come from the checklist. The model
    still decides what happened; it no longer decides what counts.

    This carryover is what fills "Official course data" when the model wrote the
    correct value into its incident object but not onto the checklist row.
    """
    node = report.setdefault("report", {})
    derived = derive_incidents(report, config_dir)
    model_incidents = node.get("incidents") or []

    # Match a derived incident back to the model's own incident two ways.
    #
    # 1. incident_ref. The checklist row carries the id of the incident the
    #    model raised for it — an exact link, so use it first.
    # 2. Word overlap, for rows with no ref. The model labels its incidents
    #    "Fees & Pricing — EMI Options" while the checklist item reads "EMI
    #    options stated correctly", so the previous exact-string match on the
    #    text after the dash never once hit, and nothing was ever carried over.
    by_id = {old.get("id"): old for old in model_incidents if old.get("id") is not None}

    _IGNORE = {"stated", "correctly", "claimed", "correct", "no", "the", "a", "an",
               "and", "of", "per", "this", "information", "in", "data", "course",
               "check", "mentioned", "accurately", "requirement"}

    def _words(text: str) -> set[str]:
        return {w for w in re.findall(r"[a-z0-9%]+", str(text).lower())
                if w not in _IGNORE and len(w) > 1}

    indexed = [(_words(old.get("category", "")), old) for old in model_incidents]

    CARRY = ("transcript_quote", "what_rep_said", "violation_basis",
             "what_is_correct", "timestamp")

    for inc in derived:
        old = by_id.get(inc.get("incident_ref"))
        if old is None:
            target = _words(inc["checklist_item"])
            best, score = None, 0
            for words, cand in indexed:
                overlap = len(target & words)
                if overlap > score:
                    best, score = cand, overlap
            # Two shared content words is a real match ("EMI"+"options");
            # one is a coincidence ("duration" appears in three categories).
            old = best if score >= 2 else None

        if old:
            for field in CARRY:
                if not inc.get(field) and old.get(field):
                    inc[field] = old[field]
            # Keep the aliases in step with whatever was carried over.
            inc["why_incident"] = inc.get("violation_basis") or inc.get("why_incident")
            inc["correct_information"] = inc.get("what_is_correct") or inc.get("correct_information")

    node["incidents"] = derived
    counts = {"L1": 0, "L2": 0, "L3": 0}
    for i in derived:
        counts[i["severity"]] = counts.get(i["severity"], 0) + 1
    node["incident_summary"] = {"total": len(derived), **counts}

    report["incident_count"] = len(derived)
    report["call_flagged"] = len(derived) > 0
    report["highest_severity"] = next(
        (s for s in ("L3", "L2", "L1") if counts.get(s)), "None"
    )
    return report
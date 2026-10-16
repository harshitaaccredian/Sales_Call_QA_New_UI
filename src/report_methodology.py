# # """
# # HTML renderer for the Sales Methodology Adherence section.

# # Self-contained: `methodology_css()` returns a <style> block scoped with an
# # `mth-` prefix so it can be appended to the existing report stylesheet without
# # collisions. Design tokens are taken from the existing report (slate palette,
# # #2563eb accent, 10px card radius) so the new section reads as part of the
# # same document rather than a bolt-on.

# # The signature element is the Trust Journey rail: five sequential stages with
# # the stall point marked. It is the one place the section spends visual weight,
# # because "how far did trust actually get" is the question a sales manager
# # opens the report to answer.

# # Usage
# # -----
# #     from src.report_methodology import methodology_css, render_methodology_section

# #     html = render_methodology_section(score_obj)   # output of compute_overall_score
# # """

# # from __future__ import annotations

# # import html as _html
# # from collections import Counter
# # from typing import Any

# # # =============================================================================
# # # Design tokens — inherited from the existing report
# # # =============================================================================

# # BAND_STYLE = {
# #     "great":   ("#10b981", "#d1fae5", "Great"),
# #     "good":    ("#2563eb", "#dbeafe", "Good"),
# #     "average": ("#f59e0b", "#fef3c7", "Average"),
# #     "missing": ("#ef4444", "#fee2e2", "Missing"),
# # }

# # STATUS_STYLE = {
# #     "answered":            ("#10b981", "#d1fae5", "Answered"),
# #     "partial":             ("#f59e0b", "#fef3c7", "Partial"),
# #     "unanswered":          ("#ef4444", "#fee2e2", "Unanswered"),
# #     "not_applicable":      ("#94a3b8", "#f1f5f9", "N/A"),
# #     "addressed":           ("#10b981", "#d1fae5", "Addressed"),
# #     "partially_addressed": ("#f59e0b", "#fef3c7", "Partial"),
# #     "not_addressed":       ("#ef4444", "#fee2e2", "Not addressed"),
# # }

# # TRUST_STAGES = [
# #     ("hear_me",      "Hear Me",       "You understand what I am saying."),
# #     ("understand_me", "Understand Me", "You understand my situation."),
# #     ("guide_me",     "Guide Me",      "Your recommendation fits my needs."),
# #     ("reassure_me",  "Reassure Me",   "My concerns have been addressed."),
# #     ("i_ll_decide",  "I'll Decide",   "I am ready to move forward."),
# # ]

# # WHY_LABELS = {
# #     "why_change":    "Why Change?",
# #     "why_now":       "Why Now?",
# #     "why_accredian": "Why Accredian?",
# #     "why_you":       "Why You?",
# # }

# # HFTE_LABELS = {"hope": "Hope", "fear": "Fear", "trust": "Trust", "effort": "Effort"}


# # def e(v: Any) -> str:
# #     return _html.escape(str(v if v is not None else ""), quote=True)


# # # =============================================================================
# # # CSS
# # # =============================================================================

# # def methodology_css() -> str:
# #     return """
# #     /* ---- Sales Methodology section ---- */
# #     .mth-scorebar-wrap { display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }
# #     .mth-scorebar-label { font-size: 13px; font-weight: 700; color: #0f172a; min-width: 210px; }
# #     .mth-scorebar-bg { flex-grow: 1; height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; }
# #     .mth-scorebar-fill { height: 100%; border-radius: 5px; }
# #     .mth-scorebar-pts { font-size: 12px; font-weight: 700; color: #475569; min-width: 74px; text-align: right; }

# #     .mth-band { font-family: var(--mono); font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 8px;
# #                 letter-spacing: 0; white-space: nowrap; }

# #     .mth-dim { border: 1px solid #eeeeeb; border-radius: 8px; padding: 18px 22px;
# #                margin-bottom: 14px; background: #fff; }
# #     .mth-dim-head { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 4px; }
# #     .mth-dim-name { font-size: 15px; font-weight: 700; color: #0f172a; }
# #     .mth-dim-chapter { font-size: 11px; color: #94a3b8; font-weight: 600; }
# #     .mth-dim-pts { margin-left: auto; font-size: 12px; font-weight: 800; color: #475569; }
# #     .mth-dim-reason { font-size: 13px; color: #475569; line-height: 1.65; margin: 8px 0 12px; }

# #     .mth-quote { border-left: 3px solid #cbd5e1; background: #f8fafc; padding: 9px 14px;
# #                  margin: 6px 0; border-radius: 0 6px 6px 0; font-size: 12.5px;
# #                  color: #334155; font-style: italic; }
# #     .mth-quote-ts { font-family: var(--mono); font-style: normal; font-weight: 700; color: #2563eb; font-size: 11px;
# #                     background: #eff6ff; padding: 1px 7px; border-radius: 5px; margin-right: 8px; }

# #     .mth-miss { border-left: 3px solid #f59e0b; background: #fffbeb; padding: 12px 16px;
# #                 margin: 8px 0; border-radius: 0 6px 6px 0; }
# #     .mth-miss-head { font-size: 11px; font-weight: 800; color: #b45309;
# #                      letter-spacing: 0; margin-bottom: 6px; }
# #     .mth-miss-row { font-size: 12.5px; color: #475569; line-height: 1.6; margin-bottom: 4px; }
# #     .mth-miss-row b { color: #0f172a; font-weight: 700; }
# #     .mth-miss-better { background: #ecfdf5; border-radius: 6px; padding: 8px 12px; margin-top: 8px;
# #                        font-size: 12.5px; color: #065f46; line-height: 1.6; }

# #     /* ---- Trust Journey rail (signature element) ---- */
# #     .mth-trust { background: var(--ink-950); border-radius: 8px; padding: 26px 28px 22px; margin-bottom: 24px; }
# #     .mth-trust-title { font-size: 11px; font-weight: 800; color: #64748b;
# #                        letter-spacing: 0; margin-bottom: 20px; }
# #     .mth-rail { display: flex; align-items: flex-start; gap: 0; }
# #     .mth-stage { flex: 1; position: relative; text-align: center; padding: 0 4px; }
# #     .mth-stage::before { content: ""; position: absolute; top: 13px; left: -50%;
# #                          width: 100%; height: 2px; background: #1e293b; z-index: 1; }
# #     .mth-stage:first-child::before { display: none; }
# #     .mth-stage.reached::before { background: #10b981; }
# #     .mth-stage-dot { position: relative; z-index: 2; width: 28px; height: 28px; border-radius: 50%;
# #                      margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;
# #                      font-size: 12px; font-weight: 800; background: #1e293b; color: #475569;
# #                      border: 2px solid #1e293b; }
# #     .mth-stage.reached .mth-stage-dot { background: #10b981; color: #052e16; border-color: #10b981; }
# #     .mth-stage.stall .mth-stage-dot { background: #0f172a; color: #f59e0b; border-color: #f59e0b; }
# #     .mth-stage-name { font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 3px; }
# #     .mth-stage.reached .mth-stage-name { color: #f8fafc; }
# #     .mth-stage.stall .mth-stage-name { color: #f59e0b; }
# #     .mth-stage-feel { font-size: 10.5px; color: #475569; line-height: 1.45; }
# #     .mth-stage.reached .mth-stage-feel { color: #94a3b8; }
# #     .mth-stall-note { margin-top: 20px; padding-top: 16px; border-top: 1px solid #1e293b;
# #                       font-size: 12.5px; color: #cbd5e1; line-height: 1.6; }
# #     .mth-stall-note b { color: #f59e0b; font-weight: 700; }

# #     /* ---- Diagnostics grids ---- */
# #     .mth-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
# #     .mth-cell { border: 1px solid #eeeeeb; border-radius: 8px; padding: 13px 16px; background: #fff; }
# #     .mth-cell-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 5px; }
# #     .mth-cell-label { font-size: 13px; font-weight: 700; color: #0f172a; }
# #     .mth-cell-note { font-size: 12px; color: #64748b; line-height: 1.55; }

# #     .mth-hfte { display: flex; align-items: stretch; gap: 14px; flex-wrap: wrap; }
# #     .mth-hfte-side { flex: 1; min-width: 240px; border-radius: 8px; padding: 16px 18px; }
# #     .mth-hfte-side.pos { background: #f0fdf4; border: 1px solid #dcfce7; }
# #     .mth-hfte-side.neg { background: #fef2f2; border: 1px solid #fee2e2; }
# #     .mth-hfte-title { font-size: 11px; font-weight: 800; letter-spacing: 0; margin-bottom: 10px; }
# #     .mth-hfte-side.pos .mth-hfte-title { color: #15803d; }
# #     .mth-hfte-side.neg .mth-hfte-title { color: #b91c1c; }

# #     .mth-na { display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
# #               background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px;
# #               padding: 12px 16px; margin-bottom: 18px; }
# #     .mth-na-label { font-size: 11px; font-weight: 800; color: #64748b;
# #                     letter-spacing: 0; }
# #     .mth-na-chip { font-size: 11.5px; font-weight: 600; color: #475569;
# #                    background: #fff; border: 1px solid #e4e4e0; border-radius: 8px; padding: 3px 11px; }

# #     .mth-coach { background: #eff6ff; border: 1px solid #dbeafe; border-radius: 8px;
# #                  padding: 20px 24px; margin-top: 6px; }
# #     .mth-coach-row { display: flex; gap: 12px; margin-bottom: 12px; align-items: flex-start; }
# #     .mth-coach-row:last-child { margin-bottom: 0; }
# #     .mth-coach-key { font-size: 11px; font-weight: 800; color: #1e40af; letter-spacing: 0; min-width: 128px; padding-top: 2px; }
# #     .mth-coach-val { font-size: 13px; color: #1e3a8a; line-height: 1.65; flex: 1; }

# #     /* ---- Verbose scorecard table ---- */
# #     .mth-sc { width: 100%; border-collapse: collapse; font-size: 13px; }
# #     .mth-sc thead th { font-family: var(--mono);
# #       text-align: left; font-size: 10.5px; font-weight: 800; color: #94a3b8;
# #       letter-spacing: 0;
# #       padding: 0 14px 10px; border-bottom: 1px solid #e2e8f0;
# #     }
# #     .mth-sc tbody td { padding: 15px 14px; border-bottom: 1px solid #eeeeeb; vertical-align: top; }
# #     .mth-sc tbody tr:last-child td { border-bottom: none; }
# #     .mth-sc-name { font-weight: 700; color: #0f172a; white-space: nowrap; }
# #     .mth-sc-ch { font-family: var(--mono); display: block; font-size: 11px; color: #94a3b8; font-weight: 600; margin-top: 3px; }
# #     .mth-sc-pts { font-weight: 800; color: #0f172a; white-space: nowrap; text-align: right; }
# #     /* ---- Measurement strip: raw call facts, no verdicts ---- */
# #     .snap-meta { padding: 0; margin-bottom: 16px; overflow: hidden; }
# #     .snap-row { display: flex; flex-wrap: wrap; }
# #     .snap-grp {
# #       flex: 1; min-width: 150px; padding: 16px 22px;
# #       border-right: 1px solid #eef1f6;
# #       display: flex; flex-direction: column; gap: 3px;
# #     }
# #     .snap-grp:last-child { border-right: none; }
# #     .snap-grp-wide { flex: 1.9; min-width: 230px; }
# #     .snap-lbl { font-family: var(--mono); font-size: 10.5px; font-weight: 700; color: #9aa6b5;
# #                 letter-spacing: 0; }
# #     .snap-val { font-size: 21px; font-weight: 700; color: #0f172a; line-height: 1.2;
# #                 font-variant-numeric: tabular-nums; }
# #     .snap-sub { font-size: 11.5px; color: #8a97a8; font-weight: 500; }
# #     .snap-ratio { display: flex; height: 7px; border-radius: 4px; overflow: hidden;
# #                   margin: 7px 0 5px; background: #eef1f6; }
# #     .snap-ratio-rep  { background: #2563eb; }
# #     .snap-ratio-cust { background: #7dd3fc; }
# #     .snap-tokens {
# #       border-top: 1px solid #eef1f6; padding: 10px 22px;
# #       font-size: 11.5px; color: #9aa6b5; font-weight: 500;
# #       font-variant-numeric: tabular-nums; background: #fcfdfe;
# #     }
# #     @media (max-width: 720px) {
# #       .snap-grp { min-width: 50%; border-bottom: 1px solid #eef1f6; padding: 13px 16px; }
# #       .snap-grp:nth-child(2n) { border-right: none; }
# #       .snap-grp-wide { min-width: 100%; border-right: none; }
# #       .snap-tokens { padding: 10px 16px; line-height: 1.8; }
# #     }

# #     .dial-cap {
# #       width: 100%; font-family: var(--mono); font-size: 10px; line-height: 1.5;
# #       color: var(--warning-deep); background: var(--warning-bg);
# #       border: 1px solid var(--warning-border); border-radius: 6px; padding: 7px 9px;
# #     }
# #     .stall-note {
# #       margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--ink-100);
# #       font-size: 12.5px; color: var(--ink-600); line-height: 1.6;
# #     }
# #     .stall-note b { color: var(--warning-deep); font-weight: 650; }
# #     .mth-exec {
# #       background: #fff; border: 1px solid #e4e8ef; border-left: 3px solid var(--ink-900);
# #       border-radius: 8px; padding: 20px 24px; margin-bottom: 16px;
# #       font-size: 13.5px; line-height: 1.7; color: var(--ink-700);
# #     }
# #     .mth-footnote {
# #       font-size: 12.5px; color: #64748b; line-height: 1.65;
# #       padding: 16px 2px 0; border-top: 1px solid #eef1f6; margin-top: -14px;
# #     }
# #     .mth-stamp { font-family: var(--mono); display: block; font-size: 11px; color: #b6c0cd; margin-top: 7px; }
# #     .mth-sc-pct { font-weight: 800; white-space: nowrap; text-align: right; }
# #     .mth-sc-wt2 { font-weight: 600; color: #94a3b8; white-space: nowrap; text-align: right; }
# #     .mth-ft td { padding: 11px 14px; border: none; }
# #     .mth-ft-top td { border-top: 2px solid #e2e8f0; padding-top: 15px; }
# #     .mth-ft-lbl { text-align: right; font-size: 12.5px; color: #475569; font-weight: 600; }
# #     .mth-ft-sub { display: block; font-size: 10.5px; color: #94a3b8; font-weight: 500; margin-top: 2px; }
# #     .mth-ft-den { font-size: 11px; font-weight: 700; color: #94a3b8; }
# #     .mth-ft-grand td { background: #0f172a; padding: 15px 14px; }
# #     .mth-ft-grand .mth-ft-lbl { color: #94a3b8; font-size: 11px; font-weight: 800;
# #                                 letter-spacing: 0; }
# #     .mth-ft-grand .mth-sc-pts { color: #fff; font-size: 20px; }
# #     .mth-ft-grand .mth-ft-den { color: #64748b; font-size: 12px; }
# #     .mth-ft-grand td:first-child { border-radius: 8px 0 0 8px; }
# #     .mth-ft-grand td:last-child { border-radius: 0 8px 8px 0; }
# #     .mth-ft-grade { font-size: 12px; font-weight: 800; white-space: nowrap; }
# #     .mth-sc-wt { display: block; font-size: 10.5px; font-weight: 700; color: #94a3b8;
# #                  margin-top: 3px; letter-spacing: .2px; }
# #     .mth-sc-obs { color: #475569; line-height: 1.65; }
# #     .mth-sc-na td { background: #f8fafc; color: #94a3b8; }
# #     .mth-sc-count { font-family: var(--mono); font-size: 11px; font-weight: 700; color: #64748b;
# #                     background: #f1f5f9; padding: 3px 11px; border-radius: 8px; }

# #     .mth-warn { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;
# #                 padding: 12px 16px; margin-bottom: 18px; font-size: 12.5px; color: #92400e; line-height: 1.6; }

# #     @media (max-width: 720px) {
# #       .mth-rail { flex-direction: column; gap: 14px; }
# #       .mth-stage { text-align: left; display: flex; gap: 12px; align-items: flex-start; }
# #       .mth-stage::before { display: none; }
# #       .mth-stage-dot { margin: 0; flex-shrink: 0; }
# #       .mth-scorebar-wrap { flex-wrap: wrap; }
# #       .mth-scorebar-label { min-width: 100%; }
# #     }
# #     """


# # # =============================================================================
# # # Fragments
# # # =============================================================================

# # def _band_chip(band: str) -> str:
# #     color, bg, label = BAND_STYLE.get(band, BAND_STYLE["missing"])
# #     return f'<span class="mth-band" style="background:{bg};color:{color}">{e(label)}</span>'


# # def _status_chip(status: str) -> str:
# #     color, bg, label = STATUS_STYLE.get(status, STATUS_STYLE["not_applicable"])
# #     return f'<span class="mth-band" style="background:{bg};color:{color}">{e(label)}</span>'


# # def _score_bar(label: str, score: float, maximum: float, color: str) -> str:
# #     pct = round(100 * score / maximum) if maximum else 0
# #     return f"""
# #       <div class="mth-scorebar-wrap">
# #         <span class="mth-scorebar-label">{e(label)}</span>
# #         <div class="mth-scorebar-bg"><div class="mth-scorebar-fill"
# #              style="width:{pct}%;background:{color}"></div></div>
# #         <span class="mth-scorebar-pts">{score:.0f} / {maximum:.0f}</span>
# #       </div>"""


# # def _trust_rail(tj: dict) -> str:
# #     """Five stage cards rather than a dark rail.

# #     The rail encoded progression but left no room to say WHY each stage was or
# #     wasn't reached. A card per stage carries the evidence beside the verdict,
# #     which is what makes the stall point actionable.
# #     """
# #     stages = {s["id"]: s for s in tj.get("stages", [])}
# #     furthest = tj.get("furthest_stage_reached")
# #     reached = sum(1 for s in tj.get("stages", []) if s.get("reached"))

# #     cells = ""
# #     for idx, (sid, name, feeling) in enumerate(TRUST_STAGES, start=1):
# #         st = stages.get(sid, {})
# #         done = bool(st.get("reached"))
# #         stall = sid == furthest and reached < 5
# #         cls = "stage" + (" done" if done and not stall else "") + (" stall" if stall else "")
# #         mark = _ico("check") if done and not stall else (
# #             _ico("dot") if stall else _ico("minus"))
# #         cells += f"""
# #         <div class="{cls}">
# #           <div class="stage-top"><span>{idx:02d} {e(name.upper())}</span>{mark}</div>
# #           <span class="stage-note">{e(st.get("note") or feeling)}</span>
# #         </div>"""

# #     tone = "ok" if reached == 5 else ("warn" if reached >= 3 else "crit")
# #     stall_txt = tj.get("where_it_stalled")
# #     foot = ""
# #     if stall_txt:
# #         label = next((n for i, n, _ in TRUST_STAGES if i == furthest), "the start")
# #         foot = (f'<div class="stall-note">Stalled at <b>{e(label)}</b> &mdash; '
# #                 f'{e(stall_txt)}</div>')

# #     return f"""
# #     <div class="panel">
# #       <div class="panel-head">
# #         <div>
# #           <div class="panel-title">Trust Journey Progression</div>
# #           <div class="panel-sub">Framework 4 &middot; {reached} of 5 stages reached</div>
# #         </div>
# #         <span class="panel-pill {tone}">{reached} / 5 reached</span>
# #       </div>
# #       <div class="panel-body">
# #         <div class="stage-grid">{cells}</div>
# #         {foot}
# #       </div>
# #     </div>"""


# # _SVG = {
# #     "check": '<path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2.6" '
# #              'stroke-linecap="round" stroke-linejoin="round"/>',
# #     "minus": '<path d="M5 12h14" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
# #     "dot":   '<circle cx="12" cy="12" r="4" fill="currentColor"/>',
# #     "cross": '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
# #     "half":  '<path d="M12 3a9 9 0 0 1 0 18Z" fill="currentColor"/>'
# #              '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>',
# # }


# # def _ico(name, cls="row-ico"):
# #     return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">'
# #             f'{_SVG.get(name, "")}</svg>')


# # def _trust_rail_section(tj: dict) -> str:
# #     return f'<div class="section">{_trust_rail(tj)}</div>' if tj.get("stages") else ""


# # def _dimension(d: dict, chapters: dict[str, str]) -> str:
# #     color = BAND_STYLE.get(d["band"], BAND_STYLE["missing"])[0]

# #     quotes = "".join(
# #         f'<div class="mth-quote"><span class="mth-quote-ts">{e(q.get("timestamp"))}</span>'
# #         f'{e(q.get("quote"))}</div>'
# #         for q in d.get("evidence", [])
# #     )

# #     misses = ""
# #     for m in d.get("missed_opportunities", []) or []:
# #         better = (f'<div class="mth-miss-better"><b>Try:</b> &ldquo;{e(m["better_response"])}&rdquo;</div>'
# #                   if m.get("better_response") else "")
# #         misses += f"""
# #         <div class="mth-miss">
# #           <div class="mth-miss-head">Missed opportunity &middot; {e(m.get('timestamp'))}</div>
# #           <div class="mth-miss-row"><b>What happened:</b> {e(m.get('what_happened'))}</div>
# #           <div class="mth-miss-row"><b>The Bible says:</b> {e(m.get('bible_says'))}</div>
# #           {better}
# #         </div>"""

# #     return f"""
# #     <div class="mth-dim">
# #       <div class="mth-dim-head">
# #         <span class="mth-dim-name">{e(d['name'])}</span>
# #         {_band_chip(d['band'])}
# #         <span class="mth-dim-chapter">{e(chapters.get(d['id'], ''))}</span>
# #         <span class="mth-dim-pts">{d['pct']:.0f}%
# #           <span style="color:#94a3b8;font-weight:600">&middot; weight {d.get('weight', 0):.0f}%
# #           &middot; {d['points']:.1f} pts</span></span>
# #       </div>
# #       <div class="mth-scorebar-bg" style="margin-bottom:10px">
# #         <div class="mth-scorebar-fill" style="width:{d['pct']:.0f}%;background:{color}"></div>
# #       </div>
# #       <div class="mth-dim-reason">{e(d.get('reasoning'))}</div>
# #       {quotes}
# #       {misses}
# #     </div>"""


# # def _apportion(values: list[float], decimals: int = 1) -> list[float]:
# #     """Round a list so the displayed values sum to the displayed total.

# #     Naive per-row rounding breaks the column: 2.52 and 3.15 print as 2.5 and
# #     3.1, which read as 5.6, while the true subtotal 5.67 prints as 5.7. A
# #     manager checking the arithmetic finds it off by 0.1 and stops trusting the
# #     table. Largest-remainder apportionment (the standard fix in financial
# #     reporting) pushes the rounding into whichever rows are closest to rounding
# #     up, so the column always adds up to what the footer says.
# #     """
# #     if not values:
# #         return []
# #     step = 10 ** decimals
# #     target = round(round(sum(values), decimals) * step)
# #     floors = [int(v * step) for v in values]
# #     shortfall = target - sum(floors)
# #     # rank by how close each value was to rounding up
# #     order = sorted(range(len(values)), key=lambda i: (values[i] * step) - floors[i], reverse=True)
# #     for i in order[:max(0, shortfall)]:
# #         floors[i] += 1
# #     return [f / step for f in floors]


# # def _weight_cell(d: dict) -> str:
# #     """Show the weight the points were actually computed from.

# #     With every stage applicable the raw rubric weight is the effective one.
# #     When a stage is N/A the rest are renormalised upward, so showing the raw
# #     weight makes the row's own arithmetic look wrong.
# #     """
# #     if not d.get("renormalized"):
# #         return f"{d.get('weight', 0):.0f}%"
# #     return (f"{d.get('effective_weight', 0):.1f}%"
# #             f"<span class=\"mth-sc-wt\">of {d.get('weight', 0):.0f}% base</span>")


# # def _scorecard(score: dict, chapters: dict[str, str]) -> str:
# #     """Dense criteria table with the full arithmetic shown in the footer.

# #     Percentages, not "x / 10" — seven rows each out of 10 reads as a score out
# #     of 70, which is the wrong mental model. A percentage carries no implied
# #     denominator, so the rows cannot be misread as adding up to anything.

# #     The POINTS column is what actually sums, and the footer runs the whole
# #     calculation to the final score, so a manager can see where the number came
# #     from without being walked through it.
# #     """
# #     meth = score.get("_methodology", {})
# #     dims = meth.get("dimensions", [])
# #     shown = _apportion([d["points"] for d in dims])
# #     rows = ""
# #     for d, pts in zip(dims, shown):
# #         color = BAND_STYLE.get(d["band"], BAND_STYLE["missing"])[0]
# #         rows += f"""
# #         <tr>
# #           <td class="mth-sc-name">{e(d['name'])}
# #             <span class="mth-sc-ch">{e(chapters.get(d['id'], ''))}</span></td>
# #           <td style="width:1%">{_band_chip(d['band'])}</td>
# #           <td class="mth-sc-pct" style="width:1%;color:{color}">{d['pct']:.0f}%</td>
# #           <td class="mth-sc-wt2" style="width:1%">{_weight_cell(d)}</td>
# #           <td class="mth-sc-pts" style="width:1%">{pts:.1f}</td>
# #           <td class="mth-sc-obs">{e(d.get('reasoning'))}</td>
# #         </tr>"""

# #     for na in meth.get("not_applicable", []):
# #         na_weight = na.get("weight", 0)
# #         rows += f"""
# #         <tr class="mth-sc-na">
# #           <td class="mth-sc-name" style="color:#94a3b8">{e(na['name'])}
# #             <span class="mth-sc-ch">{e(chapters.get(na['id'], ''))}</span></td>
# #           <td style="width:1%">{_status_chip('not_applicable')}</td>
# #           <td class="mth-sc-pct" style="color:#cbd5e1">&mdash;</td>
# #           <td class="mth-sc-wt2" style="color:#cbd5e1">&mdash;</td>
# #           <td class="mth-sc-pts" style="color:#cbd5e1">&mdash;</td>
# #           <td class="mth-sc-obs" style="color:#94a3b8">
# #             Stage not reached on this call &mdash; excluded from scoring. Its
# #             {na_weight:.0f}% weight is redistributed across the criteria above,
# #             which is why their effective weights exceed their base weights.</td>
# #         </tr>"""

# #     pens = meth.get("penalties", {})
# #     pen_total = pens.get("total", 0) or 0
# #     subtotal = round(sum(shown), 1)
# #     meth_score = meth.get("score", 0)
# #     meth_max = meth.get("max", 60)
# #     achievable = meth.get("achievable", meth_max)
# #     # When renormalisation is off and a stage was N/A, the ceiling is below the
# #     # full 60. Showing "/ 60" would understate the rep against a target they
# #     # could not have reached.
# #     meth_den = (f"{achievable:.1f} achievable of {meth_max:.0f}"
# #                 if abs(achievable - meth_max) > 0.05 else f"{meth_max:.0f}")
# #     comp_score = score.get("compliance_score", 0)
# #     comp_max = score.get("compliance_max", 40)
# #     total = score.get("total_score", 0)

# #     pen_row = ""
# #     if pen_total:
# #         pen_row = f"""
# #           <tr class="mth-ft">
# #             <td colspan="4" class="mth-ft-lbl">Habit penalties
# #               <span class="mth-ft-sub">capped at 30% of points earned</span></td>
# #             <td class="mth-sc-pts" style="color:#dc2626">&minus;{pen_total:.1f}</td><td></td>
# #           </tr>"""

# #     cap_row = ""
# #     if score.get("cap_applied"):
# #         cap_row = f"""
# #           <tr class="mth-ft">
# #             <td colspan="4" class="mth-ft-lbl" style="color:#b45309">Compliance cap applied
# #               <span class="mth-ft-sub">{e(score.get('cap_reason'))}</span></td>
# #             <td class="mth-sc-pts" style="color:#b45309">{score['cap_applied']}</td><td></td>
# #           </tr>"""

# #     n = len(meth.get("dimensions", []))
# #     return f"""
# #     <div class="section">
# #       <div class="panel">
# #         <div class="panel-head">
# #           <div>
# #             <div class="panel-title">Sales Bible Scorecard</div>
# #             <div class="panel-sub">{n} scored criteria &middot; weights renormalised
# #               where a stage was not reached</div>
# #           </div>
# #           <span class="panel-pill accent">Methodology {meth_score:.1f} / {meth_max:.0f}</span>
# #         </div>
# #         <div style="padding:4px 14px 14px">
# #         <table class="mth-sc">
# #           <thead><tr>
# #             <th>Evaluation Criteria</th>
# #             <th>Band</th>
# #             <th style="text-align:right">Achieved</th>
# #             <th style="text-align:right">Weight</th>
# #             <th style="text-align:right">Points</th>
# #             <th>Key Assessment &amp; Observations</th>
# #           </tr></thead>
# #           <tbody>{rows}</tbody>
# #           <tfoot>
# #             <tr class="mth-ft mth-ft-top">
# #               <td colspan="4" class="mth-ft-lbl">Sales Bible subtotal</td>
# #               <td class="mth-sc-pts">{subtotal:.1f}</td><td></td>
# #             </tr>
# #             {pen_row}
# #             <tr class="mth-ft">
# #               <td colspan="4" class="mth-ft-lbl"><b>Methodology</b></td>
# #               <td class="mth-sc-pts"><b>{meth_score:.1f}</b>
# #                 <span class="mth-ft-den"> / {meth_den}</span></td><td></td>
# #             </tr>
# #             <tr class="mth-ft">
# #               <td colspan="4" class="mth-ft-lbl"><b>Compliance</b>
# #                 <span class="mth-ft-sub">from the Incident Report tab</span></td>
# #               <td class="mth-sc-pts"><b>{comp_score:.1f}</b>
# #                 <span class="mth-ft-den"> / {comp_max:.0f}</span></td><td></td>
# #             </tr>
# #             {cap_row}
# #             <tr class="mth-ft mth-ft-grand">
# #               <td colspan="4" class="mth-ft-lbl">TOTAL CALL SCORE</td>
# #               <td class="mth-sc-pts">{total}<span class="mth-ft-den"> / 100</span></td>
# #               <td class="mth-ft-grade" style="color:{e(score.get('grade_color'))}">
# #                 {e(score.get('grade'))}</td>
# #             </tr>
# #           </tfoot>
# #         </table>
# #         </div>
# #       </div>
# #     </div>"""


# # def _fmt_dur(sec: float | None) -> str:
# #     if not sec:
# #         return "—"
# #     sec = int(sec)
# #     return f"{sec // 60}m {sec % 60:02d}s" if sec >= 60 else f"{sec}s"



# # def _tone(good: bool | None) -> str:
# #     """green / amber / neutral accent for a stat value."""
# #     if good is None:
# #         return "#0f172a"
# #     return "#059669" if good else "#d97706"



# # def _card(label: str, value: str, sub: str, good: bool | None = None,
# #           notability: float = 0.0, pinned: bool = False) -> dict:
# #     """One stat card, plus how noteworthy it is.

# #     `notability` is how far the metric sits from its threshold, in either
# #     direction — a talk ratio of 87% and a talk ratio of 45% are both worth
# #     showing; 61% is not. Cards are ranked by it so the section surfaces what
# #     stood out on THIS call rather than printing the same dashboard every time.
# #     """
# #     return {"label": label, "value": value, "sub": sub, "good": good,
# #             "notability": notability, "pinned": pinned}



# # def _render_card(c: dict) -> str:
# #     return f"""
# #       <div class="stat-card">
# #         <span class="stat-label">{e(c['label'])}</span>
# #         <span class="stat-value" style="color:{_tone(c['good'])}">{c['value']}</span>
# #         <span class="stat-sub">{c['sub']}</span>
# #       </div>"""





# # def _meta_strip(stats: dict, m: dict) -> str:
# #     """Dense measurement bar for the raw call facts.

# #     These are measurements, not assessments — duration, word counts, turns,
# #     tokens. They carry no threshold and no verdict, so giving each one a full
# #     stat card (as the old Call Statistics section did) spends a lot of vertical
# #     space on numbers nobody needs to weigh. A single banded row holds all of
# #     them in roughly the height of two cards, and keeps them visually distinct
# #     from the judged metrics below.
# #     """
# #     if not stats:
# #         return ""

# #     dur = stats.get("duration_seconds")
# #     tw = stats.get("total_words") or 0
# #     rw = stats.get("rep_words") or 0
# #     cw = stats.get("customer_words") or 0
# #     ru = stats.get("sales_rep_utterances") or 0
# #     cu = stats.get("customer_utterances") or 0
# #     ratio = stats.get("rep_talk_ratio_pct")
# #     if ratio is None:
# #         ratio = m.get("rep_talk_ratio_pct") or 0

# #     def grp(label, value, sub=""):
# #         return f"""
# #         <div class="snap-grp">
# #           <span class="snap-lbl">{e(label)}</span>
# #           <span class="snap-val">{value}</span>
# #           {f'<span class="snap-sub">{sub}</span>' if sub else ''}
# #         </div>"""

# #     groups = grp("Duration", _fmt_dur(dur), f"{int(dur)} seconds" if dur else "")
# #     groups += grp("Words", f"{tw:,}", f"rep {rw:,} &middot; customer {cw:,}")
# #     groups += grp("Turns", f"{ru + cu}", f"rep {ru} &middot; customer {cu}")
# #     groups += f"""
# #         <div class="snap-grp snap-grp-wide">
# #           <span class="snap-lbl">Talk ratio</span>
# #           <span class="snap-ratio">
# #             <i class="snap-ratio-rep" style="width:{ratio:.1f}%"></i>
# #             <i class="snap-ratio-cust" style="width:{100 - ratio:.1f}%"></i>
# #           </span>
# #           <span class="snap-sub">rep {ratio:.1f}% &middot; customer {100 - ratio:.1f}%
# #             &middot; target under 60%</span>
# #         </div>"""

# #     tok = []
# #     for lbl, key in (("Transcript", "transcript_tokens"), ("Input", "input_tokens"),
# #                      ("Output", "output_tokens"), ("Total", "total_tokens")):
# #         v = stats.get(key)
# #         if v:
# #             tok.append(f"{e(lbl)} {v:,}")
# #     tok_row = (f'<div class="snap-tokens">Tokens &nbsp;&middot;&nbsp; '
# #                f'{" &nbsp;&middot;&nbsp; ".join(tok)}</div>' if tok else "")

# #     return f'<div class="card snap-meta"><div class="snap-row">{groups}</div>{tok_row}</div>'



# # def render_score_banner(score: dict) -> str:
# #     """Composite score as a dial.

# #     A ring encodes the number and its distance from 100 in one mark, which a
# #     bare figure cannot. The grade chip carries the verdict in words so the
# #     colour is never load-bearing on its own.
# #     """
# #     total = score.get("total_score", 0)
# #     circ = 2 * 3.14159265 * 42
# #     offset = circ * (1 - total / 100)
# #     colour = score.get("grade_color", "#64748b")
# #     grade = score.get("grade", "")

# #     tone = {"#10b981": ("var(--success-bg)", "var(--success-border)", "var(--success-deep)"),
# #             "#3b82f6": ("var(--accent-subtle)", "#bfdbfe", "#1e40af"),
# #             "#f59e0b": ("var(--warning-bg)", "var(--warning-border)", "var(--warning-deep)"),
# #             "#ef4444": ("var(--critical-bg)", "var(--critical-border)", "var(--critical-deep)")}
# #     bg, br, fg = tone.get(colour, ("var(--ink-100)", "var(--ink-200)", "var(--ink-700)"))

# #     def pct(v, mx):
# #         return f"{100 * v / mx:.1f}%" if mx else "—"

# #     cap = ""
# #     if score.get("cap_reason"):
# #         cap = (f'<div class="dial-cap">{e(score["cap_reason"])}</div>')

# #     return f"""
# #       <div class="dial">
# #         <span class="dial-label">Composite Score</span>
# #         <div class="dial-ring">
# #           <svg viewBox="0 0 100 100" aria-hidden="true">
# #             <circle cx="50" cy="50" r="42" fill="transparent"
# #                     stroke="var(--ink-200)" stroke-width="7"/>
# #             <circle cx="50" cy="50" r="42" fill="transparent"
# #                     stroke="{e(colour)}" stroke-width="7" stroke-linecap="round"
# #                     stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"/>
# #           </svg>
# #           <div class="dial-centre">
# #             <span class="dial-num">{total}</span>
# #             <span class="dial-max">/ 100</span>
# #           </div>
# #         </div>
# #         <span class="dial-grade" style="background:{bg};border:1px solid {br};color:{fg}">
# #           <i class="chip-dot" style="background:{e(colour)}"></i>{e(grade)}
# #         </span>
# #         <div class="dial-split">
# #           <div>
# #             <span class="dial-split-k">Compliance</span>
# #             <span class="dial-split-v">{pct(score['compliance_score'], score['compliance_max'])}</span>
# #             <span class="dial-split-r">({score['compliance_score']:.0f}/{score['compliance_max']:.0f})</span>
# #           </div>
# #           <div>
# #             <span class="dial-split-k">Methodology</span>
# #             <span class="dial-split-v">{pct(score['methodology_score'], score['methodology_max'])}</span>
# #             <span class="dial-split-r">({score['methodology_score']:.0f}/{score['methodology_max']:.0f})</span>
# #           </div>
# #         </div>
# #         {cap}
# #       </div>"""



# # def render_verdict(score: dict) -> str:
# #     """Executive summary prose for the record card."""
# #     meth = score.get("_methodology", {})
# #     txt = (score.get("executive_summary") or meth.get("executive_summary")
# #            or _fallback_summary(score))
# #     return e(txt) if txt else ""



# # def render_ribbon(score: dict, stats: dict | None = None) -> str:
# #     """Six measured facts, in mono, under the record.

# #     Mono signals "a machine counted this"; the sans prose above it signals
# #     "a judgement was made". Keeping the two typefaces apart is what stops the
# #     reader from weighing a word count like a verdict.
# #     """
# #     stats = stats or {}
# #     m = score.get("_metrics") or {}
# #     meth = score.get("_methodology", {})
# #     dims = meth.get("dimensions", [])

# #     def cell(k, v, sub="", tone=""):
# #         return f"""
# #       <div class="ribbon-cell">
# #         <span class="ribbon-k">{k}</span>
# #         <span class="ribbon-v {tone}">{v}</span>
# #         <span class="ribbon-s">{sub}</span>
# #       </div>"""

# #     cells = ""
# #     dur = stats.get("duration_seconds")
# #     cells += cell("Duration", _fmt_dur(dur) if dur else "&mdash;",
# #                   f"{int(dur):,}s" if dur else "")

# #     ratio = stats.get("rep_talk_ratio_pct")
# #     if ratio is None:
# #         ratio = m.get("rep_talk_ratio_pct") or 0
# #     cells += cell("Talk ratio &middot; cap 60%", f"{ratio:.1f}% <small>rep</small>",
# #                   f"{stats.get('rep_words', 0):,} rep / {stats.get('customer_words', 0):,} cust",
# #                   "v-crit" if ratio > 60 else "v-ok")

# #     cells += cell("Words", f"{stats.get('total_words', 0):,}",
# #                   f"{stats.get('sales_rep_utterances', 0) + stats.get('customer_utterances', 0)} turns")

# #     if dims:
# #         best = max(dims, key=lambda d: d["pct"])
# #         worst = min(dims, key=lambda d: d["pct"])
# #         cells += cell("Strongest", e(best["name"]),
# #                       f"{best['pct']:.0f}% &middot; {best['points']:.1f} pts", "v-ok")
# #         cells += cell("Weakest", e(worst["name"]),
# #                       f"{worst['pct']:.0f}% &middot; {worst['points']:.1f} pts",
# #                       "v-warn" if worst["pct"] >= 35 else "v-crit")

# #     tj = meth.get("trust_journey", {})
# #     reached = sum(1 for st in tj.get("stages", []) if st.get("reached"))
# #     if tj.get("stages"):
# #         furthest = tj.get("furthest_stage_reached")
# #         name = next((n for i, n, _ in TRUST_STAGES if i == furthest), "&mdash;")
# #         cells += cell("Trust journey", f"{reached} / 5",
# #                       f"reached {e(name)}", "v-ok" if reached >= 4 else "v-warn")

# #     tok = " &nbsp;&middot;&nbsp; ".join(
# #         f"{lbl} <b>{stats[k]:,}</b>" for lbl, k in
# #         (("Transcript", "transcript_tokens"), ("Input", "input_tokens"),
# #          ("Output", "output_tokens"), ("Total", "total_tokens")) if stats.get(k))
# #     refs = " &nbsp;&middot;&nbsp; ".join(x for x in (
# #         f"Call <b>{e(score.get('_call_id') or '')}</b>" if score.get("_call_id") else "",
# #         f"Transcript <b>{e(score.get('_stt') or '')}</b>" if score.get("_stt") else "",
# #         f"Tokens {tok}" if tok else "") if x)

# #     return (f'<div class="ribbon">{cells}</div>'
# #             + (f'<div class="refbar">{refs}</div>' if refs else ""))



# # def render_score_footnote(score: dict) -> str:
# #     """Deduction narrative and version stamp, placed under the scorecard where
# #     the numbers they explain actually are."""
# #     return f"""
# #     <div class="mth-footnote">{e(score.get('deductions_text'))}
# #       <span class="mth-stamp">Rubric v{e(score.get('rubric_version'))}
# #         &middot; Scoring v{e(score.get('scoring_version'))}</span>
# #     </div>"""



# # def _fallback_summary(score: dict) -> str:
# #     """Compose an exec summary from the data when the model omits one.

# #     Deliberately plain and slightly mechanical — it exists so the section is
# #     never blank, not to compete with the model's prose. Kept in the same
# #     vocabulary rule as the prompt: no criterion ids, no scores.
# #     """
# #     meth = score.get("_methodology", {})
# #     m = score.get("_metrics") or {}
# #     dims = meth.get("dimensions", [])
# #     if not dims:
# #         return ""

# #     best = max(dims, key=lambda d: d["pct"])
# #     worst = min(dims, key=lambda d: d["pct"])
# #     plain = {
# #         "customer_profiling": "building rapport",
# #         "need_identification": "uncovering what the customer actually needed",
# #         "vision_setting": "painting the future role",
# #         "program_mapping": "connecting the program to her goals",
# #         "fee_and_urgency": "handling the fee conversation",
# #         "objection_handling": "working through hesitation",
# #         "trust_journey": "earning the customer's confidence",
# #     }

# #     parts = []
# #     strong = sum(1 for d in dims if d["band"] in ("good", "great"))
# #     verdict = ("went well overall" if strong >= len(dims) - 1
# #                else "was mixed" if strong >= len(dims) / 2
# #                else "fell short")
# #     ctype = (score.get("call_type") or "call").replace("_", " ")
# #     parts.append(f"This {ctype} {verdict}.")

# #     if best["pct"] >= 70:
# #         parts.append(f"The rep was strongest at {plain.get(best['id'], best['name'].lower())}.")
# #     if worst["pct"] < 70:
# #         parts.append(f"The clearest gap was {plain.get(worst['id'], worst['name'].lower())}.")

# #     risk = None
# #     sev = (score.get("_compliance") or {}).get("highest_severity")
# #     if sev in ("L2", "L3"):
# #         risk = f"A {sev} compliance issue was raised and caps the score regardless of selling quality."
# #     elif m.get("customer_engagement_trend") == "shutting_down":
# #         risk = "The customer said progressively less as the call went on, which usually signals disengagement."
# #     elif m.get("fee_discussed") and (m.get("rep_words_after_fee_15s") or 0) > 45:
# #         risk = "The rep kept talking straight after stating the fee rather than letting the customer respond."
# #     if risk:
# #         parts.append(risk)

# #     return " ".join(parts)




# # def render_call_snapshot(score: dict, stats: dict | None = None) -> str:
# #     """Rubric-side overview: the handful of numbers that explain the score.

# #     Deliberately not a second Call Statistics. Every metric here is a selling
# #     behaviour with a threshold from the Bible behind it, and each card is
# #     coloured against that threshold so the section reads at a glance.

# #     Cards are RANKED by how far the metric sits from its threshold — in either
# #     direction — and capped, so the section surfaces what actually stood out on
# #     this call instead of printing the same twelve tiles every time.
# #     """
# #     meth = score.get("_methodology", {})
# #     m = score.get("_metrics") or {}
# #     stats = stats or {}
# #     dims = meth.get("dimensions", [])
# #     if not dims:
# #         return ""

# #     cards: list[dict] = []


# #     def add(label, value, sub, good=None, notability=0.0, pinned=False):
# #         cards.append(_card(label, value, sub, good, notability, pinned))
# #     # Conversation facts first. These used to live in a separate Call
# #     # Statistics section on the other tab, which split "what happened on this
# #     # call" across two places. Duration and talk ratio belong next to the
# #     # selling metrics they contextualise.


# #     # --- pinned: the compressed view of the scorecard, always shown ---
# #     counts = Counter(d["band"] for d in dims)
# #     mix = " · ".join(f"{counts[b]} {b}" for b in ("great", "good", "average", "missing")
# #                      if counts.get(b))
# #     na = len(meth.get("not_applicable", []))
# #     add("Rubric Bands", mix or "—",
# #         f"{len(dims)} criteria scored" + (f" · {na} not applicable" if na else ""),
# #         pinned=True)



# #     # --- ranked: shown only when the number is genuinely notable ---


# #     q = m.get("rep_question_count")
# #     if q is not None:
# #         sl = m.get("second_level_question_count", 0)
# #         add("Questions Asked", f"{q}",
# #             f"{sl} second-level &middot; {m.get('open_question_ratio', 0) * 100:.0f}% open",
# #             sl >= 3, abs(sl - 3) / 6)

# #     pc = m.get("personalization_callback_count")
# #     if pc is not None:
# #         add("Personalisation", f"{pc}",
# #             "callbacks to the customer&rsquo;s own words", pc >= 3, abs(pc - 3) / 6)

# #     lm = m.get("longest_rep_monologue_sec")
# #     if lm is not None:
# #         at = m.get("longest_rep_monologue_at")
# #         add("Longest Monologue", _fmt_dur(lm),
# #             (f"at {e(at)} &middot; " if at else "") + "over 3m is a penalty",
# #             lm < 180, abs(lm - 180) / 180)

# #     trend = m.get("customer_engagement_trend")
# #     if trend and trend != "insufficient_data":
# #         label = {"opening_up": "Opening up", "steady": "Steady",
# #                  "shutting_down": "Shutting down"}.get(trend, trend)
# #         a, b = m.get("customer_words_first_half"), m.get("customer_words_second_half")
# #         add("Customer Engagement", label,
# #             (f"{a:.0f} &rarr; {b:.0f} words per turn" if a and b else "across the call"),
# #             trend != "shutting_down", 0.0 if trend == "steady" else 0.9)

# #     whys = meth.get("four_whys", [])
# #     if whys:
# #         ans = sum(1 for w in whys if w.get("status") == "answered")
# #         add("4 WHYs Answered", f"{ans} / {len(whys)}",
# #             " &middot; ".join(WHY_LABELS.get(w["id"], w["id"]).rstrip("?")
# #                               for w in whys if w.get("status") == "answered") or "none answered",
# #             ans >= 3, abs(ans - 3) / 4)

# #     if m.get("fee_discussed"):
# #         w = m.get("rep_words_after_fee_15s")
# #         if w is not None:
# #             add("After Stating Fee", f"{w} words",
# #                 f"in the next 15s &middot; at {e(m.get('fee_first_mention_at'))}",
# #                 w <= 45, abs(w - 45) / 60)

# #     oc = m.get("objection_count")
# #     if oc:
# #         dg = m.get("objections_with_diagnostic_response", 0)
# #         add("Objections Raised", f"{oc}",
# #             f"{dg} met with a diagnostic question", dg == oc, 0.6)

# #     ack = m.get("repetitive_ack_ratio")
# #     if ack is not None and ack >= 0.30:
# #         add("Scripted Acknowledgement", f"{ack * 100:.0f}%",
# #             "of replies opened with Great/Perfect", False, ack)

# #     # Keep pinned cards, then the most notable, capped so the section stays a
# #     # summary rather than becoming a dashboard.
# #     pinned = [c for c in cards if c["pinned"]]
# #     rest = sorted((c for c in cards if not c["pinned"]),
# #                   key=lambda c: c["notability"], reverse=True)
# #     shown = pinned + rest[:max(0, 8 - len(pinned))]


# #     return f"""
# #   <div class="section snapshot">
# #     <div class="section-title">Behavioural Metrics</div>
# #     <div class="stats-grid">{"".join(_render_card(c) for c in shown)}</div>
# #   </div>"""



# # def _four_whys(items: list[dict]) -> str:
# #     if not items:
# #         return ""
# #     tone = {"answered": ("ok", "check", "ANSWERED"),
# #             "partial": ("warn", "half", "PARTIAL"),
# #             "unanswered": ("bad", "cross", "UNANSWERED"),
# #             "not_applicable": ("", "minus", "N/A")}
# #     rows = ""
# #     for w in items:
# #         cls, icon, tag = tone.get(w.get("status", "unanswered"), tone["unanswered"])
# #         rows += f"""
# #         <div class="row-item {cls}">
# #           {_ico(icon)}
# #           <div>
# #             <span class="row-k">{e(WHY_LABELS.get(w.get('id'), w.get('id')))}</span>
# #             <span class="row-tag">[{tag}]</span>
# #             <div class="row-note">{e(w.get('note'))}</div>
# #           </div>
# #         </div>"""
# #     ans = sum(1 for w in items if w.get("status") == "answered")
# #     pill = "ok" if ans == len(items) else ("warn" if ans >= len(items) / 2 else "crit")
# #     return f"""
# #     <div class="panel">
# #       <div class="panel-head">
# #         <div class="panel-title">The 4 WHYs</div>
# #         <span class="panel-pill {pill}">{ans} of {len(items)} answered</span>
# #       </div>
# #       <div class="panel-body"><div class="row-list">{rows}</div></div>
# #     </div>"""


# # def _hfte(items: list[dict]) -> str:
# #     if not items:
# #         return ""
# #     tone = {"addressed": ("ok", "check", "Fully addressed"),
# #             "partially_addressed": ("warn", "half", "Partially addressed"),
# #             "not_addressed": ("bad", "cross", "Not addressed")}
# #     role = {"hope": "Driver", "trust": "Driver", "fear": "Inhibitor", "effort": "Inhibitor"}
# #     by = {i.get("id"): i for i in items}
# #     rows = ""
# #     for k in ("hope", "trust", "fear", "effort"):
# #         it = by.get(k)
# #         if not it:
# #             continue
# #         cls, icon, tag = tone.get(it.get("status", "not_addressed"), tone["not_addressed"])
# #         rows += f"""
# #         <div class="row-item {cls}">
# #           {_ico(icon)}
# #           <div>
# #             <span class="row-k">{e(HFTE_LABELS.get(k, k))} ({role.get(k, '')})</span>
# #             <span class="row-tag">{tag}</span>
# #             <div class="row-note">{e(it.get('note'))}</div>
# #           </div>
# #         </div>"""
# #     return f"""
# #     <div class="panel">
# #       <div class="panel-head">
# #         <div class="panel-title">HFTE Balance</div>
# #         <span class="panel-pill">Drivers vs inhibitors</span>
# #       </div>
# #       <div class="panel-body"><div class="row-list">{rows}</div></div>
# #     </div>"""


# # # =============================================================================
# # # Main renderer
# # # =============================================================================

# # def render_methodology_section(score: dict, chapters: dict[str, str] | None = None) -> str:
# #     """Render the full section from the output of scoring.compute_overall_score."""
# #     meth = score.get("_methodology", {})
# #     comp = score.get("_compliance", {})
# #     chapters = chapters or {}

# #     # --- Score summary -------------------------------------------------------
# #     # Titled "Sales Bible Rubric Score", NOT "Overall Call Score" — the latter
# #     # is the pre-existing sales-pitch section and the two are independent
# #     # measurements. Sharing a title would invite them to be read as one number.
# #     bars = _score_bar("Compliance & Fact Accuracy",
# #                       score["compliance_score"], score["compliance_max"], "#2563eb")
# #     bars += _score_bar("Sales Bible Methodology",
# #                        score["methodology_score"], score["methodology_max"], "#8b5cf6")

# #     warnings = ""
# #     if score.get("cap_reason"):
# #         warnings += (f'<div class="mth-warn"><b>Score capped.</b> {e(score["cap_reason"])}. '
# #                      f'Methodology strength does not offset a compliance breach.</div>')
# #     if score.get("low_confidence"):
# #         warnings += ('<div class="mth-warn"><b>Low confidence.</b> This call was short, '
# #                      'one-sided, or reached too few stages for a reliable methodology read. '
# #                      'Treat the score as indicative and review manually.</div>')

# #     na = ""
# #     if meth.get("not_applicable"):
# #         chips = "".join(f'<span class="mth-na-chip">{e(x["name"])}</span>'
# #                         for x in meth["not_applicable"])
# #         na = (f'<div class="mth-na"><span class="mth-na-label">Stages not reached '
# #               f'&mdash; excluded from scoring</span>{chips}</div>')

# #     # --- Penalties -----------------------------------------------------------
# #     pens = meth.get("penalties", {})
# #     pen = pens.get("applied", [])
# #     pen_html = ""
# #     if pen:
# #         rows = "".join(f'<div class="mth-miss-row">&minus;{p["points"]} &nbsp; {e(p["reason"])}</div>'
# #                        for p in pen)
# #         applied_total = pens.get("total", 0)
# #         raw_total = pens.get("total_uncapped", applied_total)
# #         # When the proportional cap bites, say so — otherwise a header reading
# #         # "-1.2 total" above a list summing to -14 looks like an arithmetic bug.
# #         if pens.get("proportionally_capped"):
# #             head = (f"Behavioural penalties &mdash; &minus;{applied_total:.1f} applied "
# #                     f"(of &minus;{raw_total:.0f} identified)")
# #             note = ('<div class="mth-miss-row" style="margin-top:8px;font-size:11.5px;color:#94a3b8">'
# #                     'Penalties are capped at a share of the points earned, so behaviour already '
# #                     'reflected in the band ratings above is not deducted twice.</div>')
# #         else:
# #             head = f"Behavioural penalties &mdash; &minus;{applied_total:.1f} total"
# #             note = ""
# #         pen_html = f"""
# #         <div class="mth-miss" style="border-left-color:#ef4444;background:#fef2f2">
# #           <div class="mth-miss-head" style="color:#b91c1c">{head}</div>{rows}{note}
# #         </div>"""

# #     dims = "".join(_dimension(d, chapters) for d in meth.get("dimensions", []))

# #     coach = score.get("coaching_summary") or meth.get("coaching_summary") or {}
# #     coach_html = ""
# #     if coach:
# #         rows = ""
# #         for key, label in (("top_strength", "Top strength"),
# #                            ("top_priority", "Highest-leverage fix"),
# #                            ("one_behaviour_to_practice", "Next 10 calls")):
# #             if coach.get(key):
# #                 rows += (f'<div class="mth-coach-row"><span class="mth-coach-key">{e(label)}</span>'
# #                          f'<span class="mth-coach-val">{e(coach[key])}</span></div>')
# #         coach_html = f"""
# #         <div class="section">
# #           <div class="section-title">Coaching Focus</div>
# #           <div class="mth-coach">{rows}</div>
# #         </div>"""

# #     return f"""
# #   {_trust_rail_section(meth.get('trust_journey', {}))}

# #   {_scorecard(score, chapters)}
# #   {render_score_footnote(score)}

# #   <div class="section">
# #     <div class="section-title">Evidence &amp; Coaching Detail</div>
# #     {na}
# #     {pen_html}
# #     {dims}
# #   </div>

# #   <div class="section"><div class="duo">{_four_whys(meth.get('four_whys', []))}{_hfte(meth.get('hfte_balance', []))}</div></div>
# #   {coach_html}
# # """

# """
# HTML renderer for the Sales Methodology Adherence section.

# Self-contained: `methodology_css()` returns a <style> block scoped with an
# `mth-` prefix so it can be appended to the existing report stylesheet without
# collisions. Design tokens are taken from the existing report (slate palette,
# #2563eb accent, 10px card radius) so the new section reads as part of the
# same document rather than a bolt-on.

# The signature element is the Trust Journey rail: five sequential stages with
# the stall point marked. It is the one place the section spends visual weight,
# because "how far did trust actually get" is the question a sales manager
# opens the report to answer.

# Usage
# -----
#     from src.report_methodology import methodology_css, render_methodology_section

#     html = render_methodology_section(score_obj)   # output of compute_overall_score
# """

# from __future__ import annotations

# import html as _html
# from collections import Counter
# from typing import Any

# # =============================================================================
# # Design tokens — inherited from the existing report
# # =============================================================================

# BAND_STYLE = {
#     "great":   ("#10b981", "#d1fae5", "Great"),
#     "good":    ("#2563eb", "#dbeafe", "Good"),
#     "average": ("#f59e0b", "#fef3c7", "Average"),
#     "missing": ("#ef4444", "#fee2e2", "Missing"),
# }

# STATUS_STYLE = {
#     "answered":            ("#10b981", "#d1fae5", "Answered"),
#     "partial":             ("#f59e0b", "#fef3c7", "Partial"),
#     "unanswered":          ("#ef4444", "#fee2e2", "Unanswered"),
#     "not_applicable":      ("#94a3b8", "#f1f5f9", "N/A"),
#     "addressed":           ("#10b981", "#d1fae5", "Addressed"),
#     "partially_addressed": ("#f59e0b", "#fef3c7", "Partial"),
#     "not_addressed":       ("#ef4444", "#fee2e2", "Not addressed"),
# }

# TRUST_STAGES = [
#     ("hear_me",      "Hear Me",       "You understand what I am saying."),
#     ("understand_me", "Understand Me", "You understand my situation."),
#     ("guide_me",     "Guide Me",      "Your recommendation fits my needs."),
#     ("reassure_me",  "Reassure Me",   "My concerns have been addressed."),
#     ("i_ll_decide",  "I'll Decide",   "I am ready to move forward."),
# ]

# WHY_LABELS = {
#     "why_change":    "Why Change?",
#     "why_now":       "Why Now?",
#     "why_accredian": "Why Accredian?",
#     "why_you":       "Why You?",
# }

# HFTE_LABELS = {"hope": "Hope", "fear": "Fear", "trust": "Trust", "effort": "Effort"}


# def e(v: Any) -> str:
#     return _html.escape(str(v if v is not None else ""), quote=True)


# # =============================================================================
# # CSS
# # =============================================================================

# def methodology_css() -> str:
#     return """
#     /* ---- Sales Methodology section ---- */
#     .mth-scorebar-wrap { display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }
#     .mth-scorebar-label { font-size: 13px; font-weight: 700; color: #0f172a; min-width: 210px; }
#     .mth-scorebar-bg { flex-grow: 1; height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; }
#     .mth-scorebar-fill { height: 100%; border-radius: 5px; }
#     .mth-scorebar-pts { font-size: 12px; font-weight: 700; color: #475569; min-width: 74px; text-align: right; }

#     .mth-band { font-family: var(--mono); font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 8px;
#                 letter-spacing: 0; white-space: nowrap; }

#     .mth-dim { border: 1px solid #eeeeeb; border-radius: 8px; padding: 18px 22px;
#                margin-bottom: 14px; background: #fff; }
#     .mth-dim-head { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 4px; }
#     .mth-dim-name { font-size: 15px; font-weight: 700; color: #0f172a; }
#     .mth-dim-chapter { font-size: 11px; color: #94a3b8; font-weight: 600; }
#     .mth-dim-pts { margin-left: auto; font-size: 12px; font-weight: 800; color: #475569; }
#     .mth-dim-reason { font-size: 13px; color: #475569; line-height: 1.65; margin: 8px 0 12px; }

#     .mth-quote { border-left: 3px solid #cbd5e1; background: #f8fafc; padding: 9px 14px;
#                  margin: 6px 0; border-radius: 0 6px 6px 0; font-size: 12.5px;
#                  color: #334155; font-style: italic; }
#     .mth-quote-ts { font-family: var(--mono); font-style: normal; font-weight: 700; color: #2563eb; font-size: 11px;
#                     background: #eff6ff; padding: 1px 7px; border-radius: 5px; margin-right: 8px; }

#     .mth-miss { border-left: 3px solid #f59e0b; background: #fffbeb; padding: 12px 16px;
#                 margin: 8px 0; border-radius: 0 6px 6px 0; }
#     .mth-miss-head { font-size: 11px; font-weight: 800; color: #b45309;
#                      letter-spacing: 0; margin-bottom: 6px; }
#     .mth-miss-row { font-size: 12.5px; color: #475569; line-height: 1.6; margin-bottom: 4px; }
#     .mth-miss-row b { color: #0f172a; font-weight: 700; }
#     .mth-miss-better { background: #ecfdf5; border-radius: 6px; padding: 8px 12px; margin-top: 8px;
#                        font-size: 12.5px; color: #065f46; line-height: 1.6; }

#     /* ---- Trust Journey rail (signature element) ---- */
#     .mth-trust { background: var(--ink-950); border-radius: 8px; padding: 26px 28px 22px; margin-bottom: 24px; }
#     .mth-trust-title { font-size: 11px; font-weight: 800; color: #64748b;
#                        letter-spacing: 0; margin-bottom: 20px; }
#     .mth-rail { display: flex; align-items: flex-start; gap: 0; }
#     .mth-stage { flex: 1; position: relative; text-align: center; padding: 0 4px; }
#     .mth-stage::before { content: ""; position: absolute; top: 13px; left: -50%;
#                          width: 100%; height: 2px; background: #1e293b; z-index: 1; }
#     .mth-stage:first-child::before { display: none; }
#     .mth-stage.reached::before { background: #10b981; }
#     .mth-stage-dot { position: relative; z-index: 2; width: 28px; height: 28px; border-radius: 50%;
#                      margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;
#                      font-size: 12px; font-weight: 800; background: #1e293b; color: #475569;
#                      border: 2px solid #1e293b; }
#     .mth-stage.reached .mth-stage-dot { background: #10b981; color: #052e16; border-color: #10b981; }
#     .mth-stage.stall .mth-stage-dot { background: #0f172a; color: #f59e0b; border-color: #f59e0b; }
#     .mth-stage-name { font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 3px; }
#     .mth-stage.reached .mth-stage-name { color: #f8fafc; }
#     .mth-stage.stall .mth-stage-name { color: #f59e0b; }
#     .mth-stage-feel { font-size: 10.5px; color: #475569; line-height: 1.45; }
#     .mth-stage.reached .mth-stage-feel { color: #94a3b8; }
#     .mth-stall-note { margin-top: 20px; padding-top: 16px; border-top: 1px solid #1e293b;
#                       font-size: 12.5px; color: #cbd5e1; line-height: 1.6; }
#     .mth-stall-note b { color: #f59e0b; font-weight: 700; }

#     /* ---- Diagnostics grids ---- */
#     .mth-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
#     .mth-cell { border: 1px solid #eeeeeb; border-radius: 8px; padding: 13px 16px; background: #fff; }
#     .mth-cell-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 5px; }
#     .mth-cell-label { font-size: 13px; font-weight: 700; color: #0f172a; }
#     .mth-cell-note { font-size: 12px; color: #64748b; line-height: 1.55; }

#     .mth-hfte { display: flex; align-items: stretch; gap: 14px; flex-wrap: wrap; }
#     .mth-hfte-side { flex: 1; min-width: 240px; border-radius: 8px; padding: 16px 18px; }
#     .mth-hfte-side.pos { background: #f0fdf4; border: 1px solid #dcfce7; }
#     .mth-hfte-side.neg { background: #fef2f2; border: 1px solid #fee2e2; }
#     .mth-hfte-title { font-size: 11px; font-weight: 800; letter-spacing: 0; margin-bottom: 10px; }
#     .mth-hfte-side.pos .mth-hfte-title { color: #15803d; }
#     .mth-hfte-side.neg .mth-hfte-title { color: #b91c1c; }

#     .mth-na { display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
#               background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px;
#               padding: 12px 16px; margin-bottom: 18px; }
#     .mth-na-label { font-size: 11px; font-weight: 800; color: #64748b;
#                     letter-spacing: 0; }
#     .mth-na-chip { font-size: 11.5px; font-weight: 600; color: #475569;
#                    background: #fff; border: 1px solid #e4e4e0; border-radius: 8px; padding: 3px 11px; }

#     .mth-coach { background: #eff6ff; border: 1px solid #dbeafe; border-radius: 8px;
#                  padding: 20px 24px; margin-top: 6px; }
#     .mth-coach-row { display: flex; gap: 12px; margin-bottom: 12px; align-items: flex-start; }
#     .mth-coach-row:last-child { margin-bottom: 0; }
#     .mth-coach-key { font-size: 11px; font-weight: 800; color: #1e40af; letter-spacing: 0; min-width: 128px; padding-top: 2px; }
#     .mth-coach-val { font-size: 13px; color: #1e3a8a; line-height: 1.65; flex: 1; }

#     /* ---- Verbose scorecard table ---- */
#     .mth-sc { width: 100%; border-collapse: collapse; font-size: 13px; }
#     .mth-sc thead th { font-family: var(--mono);
#       text-align: left; font-size: 10.5px; font-weight: 800; color: #94a3b8;
#       letter-spacing: 0;
#       padding: 0 14px 10px; border-bottom: 1px solid #e2e8f0;
#     }
#     .mth-sc tbody td { padding: 15px 14px; border-bottom: 1px solid #eeeeeb; vertical-align: top; }
#     .mth-sc tbody tr:last-child td { border-bottom: none; }
#     .mth-sc-name { font-weight: 700; color: #0f172a; white-space: nowrap; }
#     .mth-sc-ch { font-family: var(--mono); display: block; font-size: 11px; color: #94a3b8; font-weight: 600; margin-top: 3px; }
#     .mth-sc-pts { font-weight: 800; color: #0f172a; white-space: nowrap; text-align: right; }
#     /* ---- Measurement strip: raw call facts, no verdicts ---- */
#     .snap-meta { padding: 0; margin-bottom: 16px; overflow: hidden; }
#     .snap-row { display: flex; flex-wrap: wrap; }
#     .snap-grp {
#       flex: 1; min-width: 150px; padding: 16px 22px;
#       border-right: 1px solid #eef1f6;
#       display: flex; flex-direction: column; gap: 3px;
#     }
#     .snap-grp:last-child { border-right: none; }
#     .snap-grp-wide { flex: 1.9; min-width: 230px; }
#     .snap-lbl { font-family: var(--mono); font-size: 10.5px; font-weight: 700; color: #9aa6b5;
#                 letter-spacing: 0; }
#     .snap-val { font-size: 21px; font-weight: 700; color: #0f172a; line-height: 1.2;
#                 font-variant-numeric: tabular-nums; }
#     .snap-sub { font-size: 11.5px; color: #8a97a8; font-weight: 500; }
#     .snap-ratio { display: flex; height: 7px; border-radius: 4px; overflow: hidden;
#                   margin: 7px 0 5px; background: #eef1f6; }
#     .snap-ratio-rep  { background: #2563eb; }
#     .snap-ratio-cust { background: #7dd3fc; }
#     .snap-tokens {
#       border-top: 1px solid #eef1f6; padding: 10px 22px;
#       font-size: 11.5px; color: #9aa6b5; font-weight: 500;
#       font-variant-numeric: tabular-nums; background: #fcfdfe;
#     }
#     @media (max-width: 720px) {
#       .snap-grp { min-width: 50%; border-bottom: 1px solid #eef1f6; padding: 13px 16px; }
#       .snap-grp:nth-child(2n) { border-right: none; }
#       .snap-grp-wide { min-width: 100%; border-right: none; }
#       .snap-tokens { padding: 10px 16px; line-height: 1.8; }
#     }

#     .dial-cap {
#       width: 100%; font-family: var(--mono); font-size: 10px; line-height: 1.5;
#       color: var(--warning-deep); background: var(--warning-bg);
#       border: 1px solid var(--warning-border); border-radius: 6px; padding: 7px 9px;
#     }
#     .stall-note {
#       margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--ink-100);
#       font-size: 12.5px; color: var(--ink-600); line-height: 1.6;
#     }
#     .stall-note b { color: var(--warning-deep); font-weight: 650; }
#     .mth-exec {
#       background: #fff; border: 1px solid #e4e8ef; border-left: 3px solid var(--ink-900);
#       border-radius: 8px; padding: 20px 24px; margin-bottom: 16px;
#       font-size: 13.5px; line-height: 1.7; color: var(--ink-700);
#     }
#     .mth-footnote {
#       font-size: 12.5px; color: #64748b; line-height: 1.65;
#       padding: 16px 2px 0; border-top: 1px solid #eef1f6; margin-top: -14px;
#     }
#     .mth-stamp { font-family: var(--mono); display: block; font-size: 11px; color: #b6c0cd; margin-top: 7px; }
#     .mth-sc-pct { font-weight: 800; white-space: nowrap; text-align: right; }
#     .mth-sc-wt2 { font-weight: 600; color: #94a3b8; white-space: nowrap; text-align: right; }
#     .mth-ft td { padding: 11px 14px; border: none; }
#     .mth-ft-top td { border-top: 2px solid #e2e8f0; padding-top: 15px; }
#     .mth-ft-lbl { text-align: right; font-size: 12.5px; color: #475569; font-weight: 600; }
#     .mth-ft-sub { display: block; font-size: 10.5px; color: #94a3b8; font-weight: 500; margin-top: 2px; }
#     .mth-ft-den { font-size: 11px; font-weight: 700; color: #94a3b8; }
#     .mth-ft-grand td { background: #0f172a; padding: 15px 14px; }
#     .mth-ft-grand .mth-ft-lbl { color: #94a3b8; font-size: 11px; font-weight: 800;
#                                 letter-spacing: 0; }
#     .mth-ft-grand .mth-sc-pts { color: #fff; font-size: 20px; }
#     .mth-ft-grand .mth-ft-den { color: #64748b; font-size: 12px; }
#     .mth-ft-grand td:first-child { border-radius: 8px 0 0 8px; }
#     .mth-ft-grand td:last-child { border-radius: 0 8px 8px 0; }
#     .mth-ft-grade { font-size: 12px; font-weight: 800; white-space: nowrap; }
#     .mth-sc-wt { display: block; font-size: 10.5px; font-weight: 700; color: #94a3b8;
#                  margin-top: 3px; letter-spacing: .2px; }
#     .mth-sc-obs { color: #475569; line-height: 1.65; }
#     .mth-sc-na td { background: #f8fafc; color: #94a3b8; }
#     .mth-sc-count { font-family: var(--mono); font-size: 11px; font-weight: 700; color: #64748b;
#                     background: #f1f5f9; padding: 3px 11px; border-radius: 8px; }

#     .mth-warn { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;
#                 padding: 12px 16px; margin-bottom: 18px; font-size: 12.5px; color: #92400e; line-height: 1.6; }

#     @media (max-width: 720px) {
#       .mth-rail { flex-direction: column; gap: 14px; }
#       .mth-stage { text-align: left; display: flex; gap: 12px; align-items: flex-start; }
#       .mth-stage::before { display: none; }
#       .mth-stage-dot { margin: 0; flex-shrink: 0; }
#       .mth-scorebar-wrap { flex-wrap: wrap; }
#       .mth-scorebar-label { min-width: 100%; }
#     }
#     """


# # =============================================================================
# # Fragments
# # =============================================================================

# def _band_chip(band: str) -> str:
#     color, bg, label = BAND_STYLE.get(band, BAND_STYLE["missing"])
#     return f'<span class="mth-band" style="background:{bg};color:{color}">{e(label)}</span>'


# def _status_chip(status: str) -> str:
#     color, bg, label = STATUS_STYLE.get(status, STATUS_STYLE["not_applicable"])
#     return f'<span class="mth-band" style="background:{bg};color:{color}">{e(label)}</span>'


# def _score_bar(label: str, score: float, maximum: float, color: str) -> str:
#     pct = round(100 * score / maximum) if maximum else 0
#     return f"""
#       <div class="mth-scorebar-wrap">
#         <span class="mth-scorebar-label">{e(label)}</span>
#         <div class="mth-scorebar-bg"><div class="mth-scorebar-fill"
#              style="width:{pct}%;background:{color}"></div></div>
#         <span class="mth-scorebar-pts">{score:.0f} / {maximum:.0f}</span>
#       </div>"""


# def _trust_rail(tj: dict) -> str:
#     """Five stage cards rather than a dark rail.

#     The rail encoded progression but left no room to say WHY each stage was or
#     wasn't reached. A card per stage carries the evidence beside the verdict,
#     which is what makes the stall point actionable.
#     """
#     stages = {s["id"]: s for s in tj.get("stages", [])}
#     furthest = tj.get("furthest_stage_reached")
#     reached = sum(1 for s in tj.get("stages", []) if s.get("reached"))

#     cells = ""
#     for idx, (sid, name, feeling) in enumerate(TRUST_STAGES, start=1):
#         st = stages.get(sid, {})
#         done = bool(st.get("reached"))
#         stall = sid == furthest and reached < 5
#         cls = "stage" + (" done" if done and not stall else "") + (" stall" if stall else "")
#         mark = _ico("check") if done and not stall else (
#             _ico("dot") if stall else _ico("minus"))
#         cells += f"""
#         <div class="{cls}">
#           <div class="stage-top"><span>{idx:02d} {e(name.upper())}</span>{mark}</div>
#           <span class="stage-note">{e(st.get("note") or feeling)}</span>
#         </div>"""

#     tone = "ok" if reached == 5 else ("warn" if reached >= 3 else "crit")
#     stall_txt = tj.get("where_it_stalled")
#     foot = ""
#     if stall_txt:
#         label = next((n for i, n, _ in TRUST_STAGES if i == furthest), "the start")
#         foot = (f'<div class="stall-note">Stalled at <b>{e(label)}</b> &mdash; '
#                 f'{e(stall_txt)}</div>')

#     return f"""
#     <div class="panel">
#       <div class="panel-head">
#         <div>
#           <div class="panel-title">Trust Journey Progression</div>
#           <div class="panel-sub">Framework 4 &middot; {reached} of 5 stages reached</div>
#         </div>
#         <span class="panel-pill {tone}">{reached} / 5 reached</span>
#       </div>
#       <div class="panel-body">
#         <div class="stage-grid">{cells}</div>
#         {foot}
#       </div>
#     </div>"""


# _SVG = {
#     "check": '<path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2.6" '
#              'stroke-linecap="round" stroke-linejoin="round"/>',
#     "minus": '<path d="M5 12h14" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
#     "dot":   '<circle cx="12" cy="12" r="4" fill="currentColor"/>',
#     "cross": '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
#     "half":  '<path d="M12 3a9 9 0 0 1 0 18Z" fill="currentColor"/>'
#              '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>',
# }


# def _ico(name, cls="row-ico"):
#     return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">'
#             f'{_SVG.get(name, "")}</svg>')


# def _trust_rail_section(tj: dict) -> str:
#     return f'<div class="section">{_trust_rail(tj)}</div>' if tj.get("stages") else ""


# def _dimension(d: dict, chapters: dict[str, str]) -> str:
#     color = BAND_STYLE.get(d["band"], BAND_STYLE["missing"])[0]

#     quotes = "".join(
#         f'<div class="mth-quote"><span class="mth-quote-ts">{e(q.get("timestamp"))}</span>'
#         f'{e(q.get("quote"))}</div>'
#         for q in d.get("evidence", [])
#     )

#     misses = ""
#     for m in d.get("missed_opportunities", []) or []:
#         better = (f'<div class="mth-miss-better"><b>Try:</b> &ldquo;{e(m["better_response"])}&rdquo;</div>'
#                   if m.get("better_response") else "")
#         misses += f"""
#         <div class="mth-miss">
#           <div class="mth-miss-head">Missed opportunity &middot; {e(m.get('timestamp'))}</div>
#           <div class="mth-miss-row"><b>What happened:</b> {e(m.get('what_happened'))}</div>
#           <div class="mth-miss-row"><b>The Bible says:</b> {e(m.get('bible_says'))}</div>
#           {better}
#         </div>"""

#     return f"""
#     <div class="mth-dim">
#       <div class="mth-dim-head">
#         <span class="mth-dim-name">{e(d['name'])}</span>
#         {_band_chip(d['band'])}
#         <span class="mth-dim-chapter">{e(chapters.get(d['id'], ''))}</span>
#         <span class="mth-dim-pts">{d['pct']:.0f}%
#           <span style="color:#94a3b8;font-weight:600">&middot; weight {d.get('weight', 0):.0f}%
#           &middot; {d['points']:.1f} pts</span></span>
#       </div>
#       <div class="mth-scorebar-bg" style="margin-bottom:10px">
#         <div class="mth-scorebar-fill" style="width:{d['pct']:.0f}%;background:{color}"></div>
#       </div>
#       <div class="mth-dim-reason">{e(d.get('reasoning'))}</div>
#       {quotes}
#       {misses}
#     </div>"""


# def _apportion(values: list[float], decimals: int = 1) -> list[float]:
#     """Round a list so the displayed values sum to the displayed total.

#     Naive per-row rounding breaks the column: 2.52 and 3.15 print as 2.5 and
#     3.1, which read as 5.6, while the true subtotal 5.67 prints as 5.7. A
#     manager checking the arithmetic finds it off by 0.1 and stops trusting the
#     table. Largest-remainder apportionment (the standard fix in financial
#     reporting) pushes the rounding into whichever rows are closest to rounding
#     up, so the column always adds up to what the footer says.
#     """
#     if not values:
#         return []
#     step = 10 ** decimals
#     target = round(round(sum(values), decimals) * step)
#     floors = [int(v * step) for v in values]
#     shortfall = target - sum(floors)
#     # rank by how close each value was to rounding up
#     order = sorted(range(len(values)), key=lambda i: (values[i] * step) - floors[i], reverse=True)
#     for i in order[:max(0, shortfall)]:
#         floors[i] += 1
#     return [f / step for f in floors]


# def _weight_cell(d: dict) -> str:
#     """Show the weight the points were actually computed from.

#     With every stage applicable the raw rubric weight is the effective one.
#     When a stage is N/A the rest are renormalised upward, so showing the raw
#     weight makes the row's own arithmetic look wrong.
#     """
#     if not d.get("renormalized"):
#         return f"{d.get('weight', 0):.0f}%"
#     return (f"{d.get('effective_weight', 0):.1f}%"
#             f"<span class=\"mth-sc-wt\">of {d.get('weight', 0):.0f}% base</span>")


# def _scorecard(score: dict, chapters: dict[str, str]) -> str:
#     """Dense criteria table with the full arithmetic shown in the footer.

#     Percentages, not "x / 10" — seven rows each out of 10 reads as a score out
#     of 70, which is the wrong mental model. A percentage carries no implied
#     denominator, so the rows cannot be misread as adding up to anything.

#     The POINTS column is what actually sums, and the footer runs the whole
#     calculation to the final score, so a manager can see where the number came
#     from without being walked through it.
#     """
#     meth = score.get("_methodology", {})
#     dims = meth.get("dimensions", [])
#     shown = _apportion([d["points"] for d in dims])
#     rows = ""
#     for d, pts in zip(dims, shown):
#         color = BAND_STYLE.get(d["band"], BAND_STYLE["missing"])[0]
#         rows += f"""
#         <tr>
#           <td class="mth-sc-name">{e(d['name'])}
#             <span class="mth-sc-ch">{e(chapters.get(d['id'], ''))}</span></td>
#           <td style="width:1%">{_band_chip(d['band'])}</td>
#           <td class="mth-sc-pct" style="width:1%;color:{color}">{d['pct']:.0f}%</td>
#           <td class="mth-sc-wt2" style="width:1%">{_weight_cell(d)}</td>
#           <td class="mth-sc-pts" style="width:1%">{pts:.1f}</td>
#           <td class="mth-sc-obs">{e(d.get('reasoning'))}</td>
#         </tr>"""

#     for na in meth.get("not_applicable", []):
#         na_weight = na.get("weight", 0)
#         rows += f"""
#         <tr class="mth-sc-na">
#           <td class="mth-sc-name" style="color:#94a3b8">{e(na['name'])}
#             <span class="mth-sc-ch">{e(chapters.get(na['id'], ''))}</span></td>
#           <td style="width:1%">{_status_chip('not_applicable')}</td>
#           <td class="mth-sc-pct" style="color:#cbd5e1">&mdash;</td>
#           <td class="mth-sc-wt2" style="color:#cbd5e1">&mdash;</td>
#           <td class="mth-sc-pts" style="color:#cbd5e1">&mdash;</td>
#           <td class="mth-sc-obs" style="color:#94a3b8">
#             Stage not reached on this call &mdash; excluded from scoring. Its
#             {na_weight:.0f}% weight is redistributed across the criteria above,
#             which is why their effective weights exceed their base weights.</td>
#         </tr>"""

#     pens = meth.get("penalties", {})
#     pen_total = pens.get("total", 0) or 0
#     subtotal = round(sum(shown), 1)
#     meth_score = meth.get("score", 0)
#     meth_max = meth.get("max", 60)
#     achievable = meth.get("achievable", meth_max)
#     # When renormalisation is off and a stage was N/A, the ceiling is below the
#     # full 60. Showing "/ 60" would understate the rep against a target they
#     # could not have reached.
#     meth_den = (f"{achievable:.1f} achievable of {meth_max:.0f}"
#                 if abs(achievable - meth_max) > 0.05 else f"{meth_max:.0f}")
#     comp_score = score.get("compliance_score", 0)
#     comp_max = score.get("compliance_max", 40)
#     total = score.get("total_score", 0)

#     pen_row = ""
#     if pen_total:
#         pen_row = f"""
#           <tr class="mth-ft">
#             <td colspan="4" class="mth-ft-lbl">Habit penalties
#               <span class="mth-ft-sub">capped at 30% of points earned</span></td>
#             <td class="mth-sc-pts" style="color:#dc2626">&minus;{pen_total:.1f}</td><td></td>
#           </tr>"""

#     cap_row = ""
#     if score.get("cap_applied"):
#         cap_row = f"""
#           <tr class="mth-ft">
#             <td colspan="4" class="mth-ft-lbl" style="color:#b45309">Compliance cap applied
#               <span class="mth-ft-sub">{e(score.get('cap_reason'))}</span></td>
#             <td class="mth-sc-pts" style="color:#b45309">{score['cap_applied']}</td><td></td>
#           </tr>"""

#     n = len(meth.get("dimensions", []))
#     return f"""
#     <div class="section">
#       <div class="panel">
#         <div class="panel-head">
#           <div>
#             <div class="panel-title">Sales Bible Scorecard</div>
#             <div class="panel-sub">{n} scored criteria &middot; weights renormalised
#               where a stage was not reached</div>
#           </div>
#           <span class="panel-pill accent">Methodology {meth_score:.1f} / {meth_max:.0f}</span>
#         </div>
#         <div style="padding:4px 14px 14px">
#         <table class="mth-sc">
#           <thead><tr>
#             <th>Evaluation Criteria</th>
#             <th>Band</th>
#             <th style="text-align:right">Achieved</th>
#             <th style="text-align:right">Weight</th>
#             <th style="text-align:right">Points</th>
#             <th>Key Assessment &amp; Observations</th>
#           </tr></thead>
#           <tbody>{rows}</tbody>
#           <tfoot>
#             <tr class="mth-ft mth-ft-top">
#               <td colspan="4" class="mth-ft-lbl">Sales Bible subtotal</td>
#               <td class="mth-sc-pts">{subtotal:.1f}</td><td></td>
#             </tr>
#             {pen_row}
#             <tr class="mth-ft">
#               <td colspan="4" class="mth-ft-lbl"><b>Methodology</b></td>
#               <td class="mth-sc-pts"><b>{meth_score:.1f}</b>
#                 <span class="mth-ft-den"> / {meth_den}</span></td><td></td>
#             </tr>
#             <tr class="mth-ft">
#               <td colspan="4" class="mth-ft-lbl"><b>Compliance</b>
#                 <span class="mth-ft-sub">from the Incident Report tab</span></td>
#               <td class="mth-sc-pts"><b>{comp_score:.1f}</b>
#                 <span class="mth-ft-den"> / {comp_max:.0f}</span></td><td></td>
#             </tr>
#             {cap_row}
#             <tr class="mth-ft mth-ft-grand">
#               <td colspan="4" class="mth-ft-lbl">TOTAL CALL SCORE</td>
#               <td class="mth-sc-pts">{total}<span class="mth-ft-den"> / 100</span></td>
#               <td class="mth-ft-grade" style="color:{e(score.get('grade_color'))}">
#                 {e(score.get('grade'))}</td>
#             </tr>
#           </tfoot>
#         </table>
#         </div>
#       </div>
#     </div>"""


# def _fmt_dur(sec: float | None) -> str:
#     if not sec:
#         return "—"
#     sec = int(sec)
#     return f"{sec // 60}m {sec % 60:02d}s" if sec >= 60 else f"{sec}s"



# def _tone(good: bool | None) -> str:
#     """green / amber / neutral accent for a stat value."""
#     if good is None:
#         return "#0f172a"
#     return "#059669" if good else "#d97706"



# def _card(label: str, value: str, sub: str, good: bool | None = None,
#           notability: float = 0.0, pinned: bool = False) -> dict:
#     """One stat card, plus how noteworthy it is.

#     `notability` is how far the metric sits from its threshold, in either
#     direction — a talk ratio of 87% and a talk ratio of 45% are both worth
#     showing; 61% is not. Cards are ranked by it so the section surfaces what
#     stood out on THIS call rather than printing the same dashboard every time.
#     """
#     return {"label": label, "value": value, "sub": sub, "good": good,
#             "notability": notability, "pinned": pinned}



# def _render_card(c: dict) -> str:
#     return f"""
#       <div class="stat-card">
#         <span class="stat-label">{e(c['label'])}</span>
#         <span class="stat-value" style="color:{_tone(c['good'])}">{c['value']}</span>
#         <span class="stat-sub">{c['sub']}</span>
#       </div>"""





# def _meta_strip(stats: dict, m: dict) -> str:
#     """Dense measurement bar for the raw call facts.

#     These are measurements, not assessments — duration, word counts, turns,
#     tokens. They carry no threshold and no verdict, so giving each one a full
#     stat card (as the old Call Statistics section did) spends a lot of vertical
#     space on numbers nobody needs to weigh. A single banded row holds all of
#     them in roughly the height of two cards, and keeps them visually distinct
#     from the judged metrics below.
#     """
#     if not stats:
#         return ""

#     dur = stats.get("duration_seconds")
#     tw = stats.get("total_words") or 0
#     rw = stats.get("rep_words") or 0
#     cw = stats.get("customer_words") or 0
#     ru = stats.get("sales_rep_utterances") or 0
#     cu = stats.get("customer_utterances") or 0
#     ratio = stats.get("rep_talk_ratio_pct")
#     if ratio is None:
#         ratio = m.get("rep_talk_ratio_pct") or 0

#     def grp(label, value, sub=""):
#         return f"""
#         <div class="snap-grp">
#           <span class="snap-lbl">{e(label)}</span>
#           <span class="snap-val">{value}</span>
#           {f'<span class="snap-sub">{sub}</span>' if sub else ''}
#         </div>"""

#     groups = grp("Duration", _fmt_dur(dur), f"{int(dur)} seconds" if dur else "")
#     groups += grp("Words", f"{tw:,}", f"rep {rw:,} &middot; customer {cw:,}")
#     groups += grp("Turns", f"{ru + cu}", f"rep {ru} &middot; customer {cu}")
#     groups += f"""
#         <div class="snap-grp snap-grp-wide">
#           <span class="snap-lbl">Talk ratio</span>
#           <span class="snap-ratio">
#             <i class="snap-ratio-rep" style="width:{ratio:.1f}%"></i>
#             <i class="snap-ratio-cust" style="width:{100 - ratio:.1f}%"></i>
#           </span>
#           <span class="snap-sub">rep {ratio:.1f}% &middot; customer {100 - ratio:.1f}%
#             &middot; target under 60%</span>
#         </div>"""

#     tok = []
#     for lbl, key in (("Transcript", "transcript_tokens"), ("Input", "input_tokens"),
#                      ("Output", "output_tokens"), ("Total", "total_tokens")):
#         v = stats.get(key)
#         if v:
#             tok.append(f"{e(lbl)} {v:,}")
#     tok_row = (f'<div class="snap-tokens">Tokens &nbsp;&middot;&nbsp; '
#                f'{" &nbsp;&middot;&nbsp; ".join(tok)}</div>' if tok else "")

#     return f'<div class="card snap-meta"><div class="snap-row">{groups}</div>{tok_row}</div>'



# def render_score_banner(score: dict) -> str:
#     """Composite score as a dial.

#     A ring encodes the number and its distance from 100 in one mark, which a
#     bare figure cannot. The grade chip carries the verdict in words so the
#     colour is never load-bearing on its own.
#     """
#     total = score.get("total_score", 0)
#     circ = 2 * 3.14159265 * 42
#     offset = circ * (1 - total / 100)
#     colour = score.get("grade_color", "#64748b")
#     grade = score.get("grade", "")

#     tone = {"#10b981": ("var(--success-bg)", "var(--success-border)", "var(--success-deep)"),
#             "#3b82f6": ("var(--accent-subtle)", "#bfdbfe", "#1e40af"),
#             "#f59e0b": ("var(--warning-bg)", "var(--warning-border)", "var(--warning-deep)"),
#             "#ef4444": ("var(--critical-bg)", "var(--critical-border)", "var(--critical-deep)")}
#     bg, br, fg = tone.get(colour, ("var(--ink-100)", "var(--ink-200)", "var(--ink-700)"))

#     def pct(v, mx):
#         return f"{100 * v / mx:.1f}%" if mx else "—"

#     cap = ""
#     if score.get("cap_reason"):
#         cap = (f'<div class="dial-cap">{e(score["cap_reason"])}</div>')

#     return f"""
#       <div class="dial">
#         <span class="dial-label">Composite Score</span>
#         <div class="dial-ring">
#           <svg viewBox="0 0 100 100" aria-hidden="true">
#             <circle cx="50" cy="50" r="42" fill="transparent"
#                     stroke="var(--ink-200)" stroke-width="7"/>
#             <circle cx="50" cy="50" r="42" fill="transparent"
#                     stroke="{e(colour)}" stroke-width="7" stroke-linecap="round"
#                     stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"/>
#           </svg>
#           <div class="dial-centre">
#             <span class="dial-num">{total}</span>
#             <span class="dial-max">/ 100</span>
#           </div>
#         </div>
#         <span class="dial-grade" style="background:{bg};border:1px solid {br};color:{fg}">
#           <i class="chip-dot" style="background:{e(colour)}"></i>{e(grade)}
#         </span>
#         <div class="dial-split">
#           <div>
#             <span class="dial-split-k">Compliance</span>
#             <span class="dial-split-v">{pct(score['compliance_score'], score['compliance_max'])}</span>
#             <span class="dial-split-r">({score['compliance_score']:.0f}/{score['compliance_max']:.0f})</span>
#           </div>
#           <div>
#             <span class="dial-split-k">Methodology</span>
#             <span class="dial-split-v">{pct(score['methodology_score'], score['methodology_max'])}</span>
#             <span class="dial-split-r">({score['methodology_score']:.0f}/{score['methodology_max']:.0f})</span>
#           </div>
#         </div>
#         {cap}
#       </div>"""



# def render_verdict(score: dict) -> str:
#     """Executive summary prose for the record card."""
#     meth = score.get("_methodology", {})
#     txt = (score.get("executive_summary") or meth.get("executive_summary")
#            or _fallback_summary(score))
#     return e(txt) if txt else ""



# def render_ribbon(score: dict, stats: dict | None = None) -> str:
#     """Six measured facts, in mono, under the record.

#     Mono signals "a machine counted this"; the sans prose above it signals
#     "a judgement was made". Keeping the two typefaces apart is what stops the
#     reader from weighing a word count like a verdict.
#     """
#     stats = stats or {}
#     m = score.get("_metrics") or {}
#     meth = score.get("_methodology", {})
#     dims = meth.get("dimensions", [])

#     def cell(k, v, sub="", tone=""):
#         return f"""
#       <div class="ribbon-cell">
#         <span class="ribbon-k">{k}</span>
#         <span class="ribbon-v {tone}">{v}</span>
#         <span class="ribbon-s">{sub}</span>
#       </div>"""

#     cells = ""
#     dur = stats.get("duration_seconds")
#     cells += cell("Duration", _fmt_dur(dur) if dur else "&mdash;",
#                   f"{int(dur):,}s" if dur else "")

#     ratio = stats.get("rep_talk_ratio_pct")
#     if ratio is None:
#         ratio = m.get("rep_talk_ratio_pct") or 0
#     cells += cell("Talk ratio &middot; cap 60%", f"{ratio:.1f}% <small>rep</small>",
#                   f"{stats.get('rep_words', 0):,} rep / {stats.get('customer_words', 0):,} cust",
#                   "v-crit" if ratio > 60 else "v-ok")

#     cells += cell("Words", f"{stats.get('total_words', 0):,}",
#                   f"{stats.get('sales_rep_utterances', 0) + stats.get('customer_utterances', 0)} turns")

#     if dims:
#         best = max(dims, key=lambda d: d["pct"])
#         worst = min(dims, key=lambda d: d["pct"])
#         cells += cell("Strongest", e(best["name"]),
#                       f"{best['pct']:.0f}% &middot; {best['points']:.1f} pts", "v-ok")
#         cells += cell("Weakest", e(worst["name"]),
#                       f"{worst['pct']:.0f}% &middot; {worst['points']:.1f} pts",
#                       "v-warn" if worst["pct"] >= 35 else "v-crit")

#     tj = meth.get("trust_journey", {})
#     reached = sum(1 for st in tj.get("stages", []) if st.get("reached"))
#     if tj.get("stages"):
#         furthest = tj.get("furthest_stage_reached")
#         name = next((n for i, n, _ in TRUST_STAGES if i == furthest), "&mdash;")
#         cells += cell("Trust journey", f"{reached} / 5",
#                       f"reached {e(name)}", "v-ok" if reached >= 4 else "v-warn")

#     tok = " &nbsp;&middot;&nbsp; ".join(
#         f"{lbl} <b>{stats[k]:,}</b>" for lbl, k in
#         (("Transcript", "transcript_tokens"), ("Input", "input_tokens"),
#          ("Output", "output_tokens"), ("Total", "total_tokens")) if stats.get(k))
#     refs = " &nbsp;&middot;&nbsp; ".join(x for x in (
#         f"Call <b>{e(score.get('_call_id') or '')}</b>" if score.get("_call_id") else "",
#         f"Transcript <b>{e(score.get('_stt') or '')}</b>" if score.get("_stt") else "",
#         f"Tokens {tok}" if tok else "") if x)

#     return (f'<div class="ribbon">{cells}</div>'
#             + (f'<div class="refbar">{refs}</div>' if refs else ""))



# def render_score_footnote(score: dict) -> str:
#     """Deduction narrative and version stamp, placed under the scorecard where
#     the numbers they explain actually are."""
#     return f"""
#     <div class="mth-footnote">{e(score.get('deductions_text'))}
#       <span class="mth-stamp">Rubric v{e(score.get('rubric_version'))}
#         &middot; Scoring v{e(score.get('scoring_version'))}</span>
#     </div>"""



# def _fallback_summary(score: dict) -> str:
#     """Compose an exec summary from the data when the model omits one.

#     Deliberately plain and slightly mechanical — it exists so the section is
#     never blank, not to compete with the model's prose. Kept in the same
#     vocabulary rule as the prompt: no criterion ids, no scores.
#     """
#     meth = score.get("_methodology", {})
#     m = score.get("_metrics") or {}
#     dims = meth.get("dimensions", [])
#     if not dims:
#         return ""

#     best = max(dims, key=lambda d: d["pct"])
#     worst = min(dims, key=lambda d: d["pct"])
#     plain = {
#         "customer_profiling": "building rapport",
#         "need_identification": "uncovering what the customer actually needed",
#         "vision_setting": "painting the future role",
#         "program_mapping": "connecting the program to her goals",
#         "fee_and_urgency": "handling the fee conversation",
#         "objection_handling": "working through hesitation",
#         "trust_journey": "earning the customer's confidence",
#     }

#     parts = []
#     strong = sum(1 for d in dims if d["band"] in ("good", "great"))
#     verdict = ("went well overall" if strong >= len(dims) - 1
#                else "was mixed" if strong >= len(dims) / 2
#                else "fell short")
#     ctype = (score.get("call_type") or "call").replace("_", " ")
#     parts.append(f"This {ctype} {verdict}.")

#     if best["pct"] >= 70:
#         parts.append(f"The rep was strongest at {plain.get(best['id'], best['name'].lower())}.")
#     if worst["pct"] < 70:
#         parts.append(f"The clearest gap was {plain.get(worst['id'], worst['name'].lower())}.")

#     risk = None
#     sev = (score.get("_compliance") or {}).get("highest_severity")
#     if sev in ("L2", "L3"):
#         risk = f"A {sev} compliance issue was raised and caps the score regardless of selling quality."
#     elif m.get("customer_engagement_trend") == "shutting_down":
#         risk = "The customer said progressively less as the call went on, which usually signals disengagement."
#     elif m.get("fee_discussed") and (m.get("rep_words_after_fee_15s") or 0) > 45:
#         risk = "The rep kept talking straight after stating the fee rather than letting the customer respond."
#     if risk:
#         parts.append(risk)

#     return " ".join(parts)




# def render_call_snapshot(score: dict, stats: dict | None = None) -> str:
#     """Rubric-side overview: the handful of numbers that explain the score.

#     Deliberately not a second Call Statistics. Every metric here is a selling
#     behaviour with a threshold from the Bible behind it, and each card is
#     coloured against that threshold so the section reads at a glance.

#     Cards are RANKED by how far the metric sits from its threshold — in either
#     direction — and capped, so the section surfaces what actually stood out on
#     this call instead of printing the same twelve tiles every time.
#     """
#     meth = score.get("_methodology", {})
#     m = score.get("_metrics") or {}
#     stats = stats or {}
#     dims = meth.get("dimensions", [])
#     if not dims:
#         return ""

#     cards: list[dict] = []


#     def add(label, value, sub, good=None, notability=0.0, pinned=False):
#         cards.append(_card(label, value, sub, good, notability, pinned))
#     # Conversation facts first. These used to live in a separate Call
#     # Statistics section on the other tab, which split "what happened on this
#     # call" across two places. Duration and talk ratio belong next to the
#     # selling metrics they contextualise.


#     # --- pinned: the compressed view of the scorecard, always shown ---
#     counts = Counter(d["band"] for d in dims)
#     mix = " · ".join(f"{counts[b]} {b}" for b in ("great", "good", "average", "missing")
#                      if counts.get(b))
#     na = len(meth.get("not_applicable", []))
#     add("Rubric Bands", mix or "—",
#         f"{len(dims)} criteria scored" + (f" · {na} not applicable" if na else ""),
#         pinned=True)



#     # --- ranked: shown only when the number is genuinely notable ---


#     q = m.get("rep_question_count")
#     if q is not None:
#         sl = m.get("second_level_question_count", 0)
#         add("Questions Asked", f"{q}",
#             f"{sl} second-level &middot; {m.get('open_question_ratio', 0) * 100:.0f}% open",
#             sl >= 3, abs(sl - 3) / 6)

#     pc = m.get("personalization_callback_count")
#     if pc is not None:
#         add("Personalisation", f"{pc}",
#             "callbacks to the customer&rsquo;s own words", pc >= 3, abs(pc - 3) / 6)

#     lm = m.get("longest_rep_monologue_sec")
#     if lm is not None:
#         at = m.get("longest_rep_monologue_at")
#         add("Longest Monologue", _fmt_dur(lm),
#             (f"at {e(at)} &middot; " if at else "") + "over 3m is a penalty",
#             lm < 180, abs(lm - 180) / 180)

#     trend = m.get("customer_engagement_trend")
#     if trend and trend != "insufficient_data":
#         label = {"opening_up": "Opening up", "steady": "Steady",
#                  "shutting_down": "Shutting down"}.get(trend, trend)
#         a, b = m.get("customer_words_first_half"), m.get("customer_words_second_half")
#         add("Customer Engagement", label,
#             (f"{a:.0f} &rarr; {b:.0f} words per turn" if a and b else "across the call"),
#             trend != "shutting_down", 0.0 if trend == "steady" else 0.9)

#     whys = meth.get("four_whys", [])
#     if whys:
#         ans = sum(1 for w in whys if w.get("status") == "answered")
#         add("4 WHYs Answered", f"{ans} / {len(whys)}",
#             " &middot; ".join(WHY_LABELS.get(w["id"], w["id"]).rstrip("?")
#                               for w in whys if w.get("status") == "answered") or "none answered",
#             ans >= 3, abs(ans - 3) / 4)

#     if m.get("fee_discussed"):
#         w = m.get("rep_words_after_fee_15s")
#         if w is not None:
#             add("After Stating Fee", f"{w} words",
#                 f"in the next 15s &middot; at {e(m.get('fee_first_mention_at'))}",
#                 w <= 45, abs(w - 45) / 60)

#     oc = m.get("objection_count")
#     if oc:
#         dg = m.get("objections_with_diagnostic_response", 0)
#         add("Objections Raised", f"{oc}",
#             f"{dg} met with a diagnostic question", dg == oc, 0.6)

#     ack = m.get("repetitive_ack_ratio")
#     if ack is not None and ack >= 0.30:
#         add("Scripted Acknowledgement", f"{ack * 100:.0f}%",
#             "of replies opened with Great/Perfect", False, ack)

#     # Keep pinned cards, then the most notable, capped so the section stays a
#     # summary rather than becoming a dashboard.
#     pinned = [c for c in cards if c["pinned"]]
#     rest = sorted((c for c in cards if not c["pinned"]),
#                   key=lambda c: c["notability"], reverse=True)
#     shown = pinned + rest[:max(0, 8 - len(pinned))]


#     return f"""
#   <div class="section snapshot">
#     <div class="section-title">Behavioural Metrics</div>
#     <div class="stats-grid">{"".join(_render_card(c) for c in shown)}</div>
#   </div>"""



# def _four_whys(items: list[dict]) -> str:
#     if not items:
#         return ""
#     tone = {"answered": ("ok", "check", "ANSWERED"),
#             "partial": ("warn", "half", "PARTIAL"),
#             "unanswered": ("bad", "cross", "UNANSWERED"),
#             "not_applicable": ("", "minus", "N/A")}
#     rows = ""
#     for w in items:
#         cls, icon, tag = tone.get(w.get("status", "unanswered"), tone["unanswered"])
#         rows += f"""
#         <div class="row-item {cls}">
#           {_ico(icon)}
#           <div>
#             <span class="row-k">{e(WHY_LABELS.get(w.get('id'), w.get('id')))}</span>
#             <span class="row-tag">[{tag}]</span>
#             <div class="row-note">{e(w.get('note'))}</div>
#           </div>
#         </div>"""
#     ans = sum(1 for w in items if w.get("status") == "answered")
#     pill = "ok" if ans == len(items) else ("warn" if ans >= len(items) / 2 else "crit")
#     return f"""
#     <div class="panel">
#       <div class="panel-head">
#         <div class="panel-title">The 4 WHYs</div>
#         <span class="panel-pill {pill}">{ans} of {len(items)} answered</span>
#       </div>
#       <div class="panel-body"><div class="row-list">{rows}</div></div>
#     </div>"""


# def _hfte(items: list[dict]) -> str:
#     if not items:
#         return ""
#     tone = {"addressed": ("ok", "check", "Fully addressed"),
#             "partially_addressed": ("warn", "half", "Partially addressed"),
#             "not_addressed": ("bad", "cross", "Not addressed")}
#     role = {"hope": "Driver", "trust": "Driver", "fear": "Inhibitor", "effort": "Inhibitor"}
#     by = {i.get("id"): i for i in items}
#     rows = ""
#     for k in ("hope", "trust", "fear", "effort"):
#         it = by.get(k)
#         if not it:
#             continue
#         cls, icon, tag = tone.get(it.get("status", "not_addressed"), tone["not_addressed"])
#         rows += f"""
#         <div class="row-item {cls}">
#           {_ico(icon)}
#           <div>
#             <span class="row-k">{e(HFTE_LABELS.get(k, k))} ({role.get(k, '')})</span>
#             <span class="row-tag">{tag}</span>
#             <div class="row-note">{e(it.get('note'))}</div>
#           </div>
#         </div>"""
#     return f"""
#     <div class="panel">
#       <div class="panel-head">
#         <div class="panel-title">HFTE Balance</div>
#         <span class="panel-pill">Drivers vs inhibitors</span>
#       </div>
#       <div class="panel-body"><div class="row-list">{rows}</div></div>
#     </div>"""


# # =============================================================================
# # Main renderer
# # =============================================================================

# def render_diagnostics(score: dict) -> str:
#     """The 4 WHYs and HFTE pair, rendered for the Sales Intelligence tab."""
#     meth = (score or {}).get("_methodology", {})
#     whys = _four_whys(meth.get("four_whys", []))
#     hfte = _hfte(meth.get("hfte_balance", []))
#     if not (whys or hfte):
#         return ""
#     return f'<div class="duo">{whys}{hfte}</div>'


# def render_methodology_section(score: dict, chapters: dict[str, str] | None = None) -> str:
#     """Render the full section from the output of scoring.compute_overall_score."""
#     meth = score.get("_methodology", {})
#     comp = score.get("_compliance", {})
#     chapters = chapters or {}

#     # --- Score summary -------------------------------------------------------
#     # Titled "Sales Bible Rubric Score", NOT "Overall Call Score" — the latter
#     # is the pre-existing sales-pitch section and the two are independent
#     # measurements. Sharing a title would invite them to be read as one number.
#     bars = _score_bar("Compliance & Fact Accuracy",
#                       score["compliance_score"], score["compliance_max"], "#2563eb")
#     bars += _score_bar("Sales Bible Methodology",
#                        score["methodology_score"], score["methodology_max"], "#8b5cf6")

#     warnings = ""
#     if score.get("cap_reason"):
#         warnings += (f'<div class="mth-warn"><b>Score capped.</b> {e(score["cap_reason"])}. '
#                      f'Methodology strength does not offset a compliance breach.</div>')
#     if score.get("low_confidence"):
#         warnings += ('<div class="mth-warn"><b>Low confidence.</b> This call was short, '
#                      'one-sided, or reached too few stages for a reliable methodology read. '
#                      'Treat the score as indicative and review manually.</div>')

#     na = ""
#     if meth.get("not_applicable"):
#         chips = "".join(f'<span class="mth-na-chip">{e(x["name"])}</span>'
#                         for x in meth["not_applicable"])
#         na = (f'<div class="mth-na"><span class="mth-na-label">Stages not reached '
#               f'&mdash; excluded from scoring</span>{chips}</div>')

#     # --- Penalties -----------------------------------------------------------
#     pens = meth.get("penalties", {})
#     pen = pens.get("applied", [])
#     pen_html = ""
#     if pen:
#         rows = "".join(f'<div class="mth-miss-row">&minus;{p["points"]} &nbsp; {e(p["reason"])}</div>'
#                        for p in pen)
#         applied_total = pens.get("total", 0)
#         raw_total = pens.get("total_uncapped", applied_total)
#         # When the proportional cap bites, say so — otherwise a header reading
#         # "-1.2 total" above a list summing to -14 looks like an arithmetic bug.
#         if pens.get("proportionally_capped"):
#             head = (f"Behavioural penalties &mdash; &minus;{applied_total:.1f} applied "
#                     f"(of &minus;{raw_total:.0f} identified)")
#             note = ('<div class="mth-miss-row" style="margin-top:8px;font-size:11.5px;color:#94a3b8">'
#                     'Penalties are capped at a share of the points earned, so behaviour already '
#                     'reflected in the band ratings above is not deducted twice.</div>')
#         else:
#             head = f"Behavioural penalties &mdash; &minus;{applied_total:.1f} total"
#             note = ""
#         pen_html = f"""
#         <div class="mth-miss" style="border-left-color:#ef4444;background:#fef2f2">
#           <div class="mth-miss-head" style="color:#b91c1c">{head}</div>{rows}{note}
#         </div>"""

#     dims = "".join(_dimension(d, chapters) for d in meth.get("dimensions", []))

#     coach = score.get("coaching_summary") or meth.get("coaching_summary") or {}
#     coach_html = ""
#     if coach:
#         rows = ""
#         for key, label in (("top_strength", "Top strength"),
#                            ("top_priority", "Highest-leverage fix"),
#                            ("one_behaviour_to_practice", "Next 10 calls")):
#             if coach.get(key):
#                 rows += (f'<div class="mth-coach-row"><span class="mth-coach-key">{e(label)}</span>'
#                          f'<span class="mth-coach-val">{e(coach[key])}</span></div>')
#         coach_html = f"""
#         <div class="section">
#           <div class="section-title">Coaching Focus</div>
#           <div class="mth-coach">{rows}</div>
#         </div>"""

#     return f"""
#   {_trust_rail_section(meth.get('trust_journey', {}))}

#   {_scorecard(score, chapters)}
#   {render_score_footnote(score)}

#   <div class="section">
#     <div class="section-title">Evidence &amp; Coaching Detail</div>
#     {na}
#     {pen_html}
#     {dims}
#   </div>


#   {coach_html}
# """

"""
HTML renderer for the rubric & methodology sections.

All styling lives in src/report_css.py; this module emits markup only, using
that shared class vocabulary. Two typefaces by role: sans for prose a person
wrote, mono for anything a machine measured.
"""

from __future__ import annotations

import html as _html
from collections import Counter
from typing import Any

TRUST_STAGES = [
    ("hear_me",       "Hear Me",       "You understand what I am saying."),
    ("understand_me", "Understand Me", "You understand my situation."),
    ("guide_me",      "Guide Me",      "Your recommendation fits my needs."),
    ("reassure_me",   "Reassure Me",   "My concerns have been addressed."),
    ("i_ll_decide",   "I'll Decide",   "I am ready to move forward."),
]

WHY_LABELS = {
    "why_change":    "Why Change?",
    "why_now":       "Why Now?",
    "why_accredian": "Why Accredian?",
    "why_you":       "Why You?",
}

HFTE_LABELS = {"hope": "Hope", "fear": "Fear", "trust": "Trust", "effort": "Effort"}

PLAIN_DIM = {
    "customer_profiling": "building rapport",
    "need_identification": "uncovering what the customer actually needed",
    "vision_setting": "painting the future role",
    "program_mapping": "connecting the program to their goals",
    "fee_and_urgency": "handling the fee conversation",
    "objection_handling": "working through hesitation",
    "trust_journey": "earning the customer's confidence",
}

_SVG = {
    "check": '<path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2.6" '
             'stroke-linecap="round" stroke-linejoin="round"/>',
    "cross": '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" '
             'stroke-width="2.6" stroke-linecap="round"/>',
    "minus": '<path d="M5 12h14" fill="none" stroke="currentColor" stroke-width="2.6" '
             'stroke-linecap="round"/>',
    "dot":   '<circle cx="12" cy="12" r="4.5" fill="currentColor"/>',
    "half":  '<path d="M12 3a9 9 0 0 1 0 18Z" fill="currentColor"/>'
             '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>',
    "chev":  '<path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.4" '
             'stroke-linecap="round" stroke-linejoin="round"/>',
    "gavel": '<path d="m14 4 6 6-3 3-6-6 3-3ZM4 20h10M9.5 11.5 4 17" fill="none" '
             'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
             'stroke-linejoin="round"/>',
}


def e(v: Any) -> str:
    return _html.escape(str(v if v is not None else ""), quote=True)


def _ico(name: str, cls: str = "row-ico") -> str:
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">'
            f'{_SVG.get(name, "")}</svg>')


def methodology_css() -> str:
    """Styling now lives in report_css.CSS; kept so callers need no change."""
    return ""


def _fmt_dur(sec) -> str:
    if not sec:
        return "&mdash;"
    sec = int(sec)
    return f"{sec // 60}m {sec % 60:02d}s" if sec >= 60 else f"{sec}s"


def _apportion(values: list[float], decimals: int = 1) -> list[float]:
    """Round a list so the displayed values sum to the displayed total.

    Naive per-row rounding breaks the column: 2.52 and 3.15 print as 2.5 and
    3.1, reading as 5.6, while the true subtotal 5.67 prints as 5.7. A manager
    checking the arithmetic finds it off by 0.1 and stops trusting the table.
    Largest-remainder apportionment pushes the rounding into whichever rows sat
    closest to rounding up, so the column always adds to what the footer says.
    """
    if not values:
        return []
    step = 10 ** decimals
    target = round(round(sum(values), decimals) * step)
    floors = [int(v * step) for v in values]
    shortfall = target - sum(floors)
    order = sorted(range(len(values)),
                   key=lambda i: (values[i] * step) - floors[i], reverse=True)
    for i in order[:max(0, shortfall)]:
        floors[i] += 1
    return [f / step for f in floors]


# =============================================================================
# Hero pieces
# =============================================================================

def render_gauge(score: dict) -> str:
    """Composite score as a ring: encodes the number and its distance from 100
    in one mark, which a bare figure cannot."""
    total = score.get("total_score", 0)
    circ = 2 * 3.14159265 * 40
    offset = circ * (1 - total / 100)
    colour = score.get("grade_color", "#64748b")

    tone = {
        "#10b981": ("var(--emer-bg)", "var(--emer-br)", "var(--emer-d)"),
        "#3b82f6": ("var(--blue-bg)", "var(--blue-br)", "var(--blue-d)"),
        "#f59e0b": ("var(--amber-bg)", "var(--amber-br)", "var(--amber-d)"),
        "#ef4444": ("var(--rose-bg)", "var(--rose-br)", "var(--rose-d)"),
    }
    bg, br, fg = tone.get(colour, ("var(--s100)", "var(--s200)", "var(--s700)"))

    def pct(v, mx):
        return f"{100 * v / mx:.1f}%" if mx else "&mdash;"

    cap = f'<div class="gauge-cap">{e(score["cap_reason"])}</div>' if score.get("cap_reason") else ""

    return f"""
    <div class="gauge">
      <span class="gauge-label">Composite Quality Score</span>
      <div class="gauge-ring">
        <svg viewBox="0 0 100 100" aria-hidden="true">
          <circle cx="50" cy="50" r="40" fill="transparent" stroke="var(--s200)" stroke-width="7"/>
          <circle cx="50" cy="50" r="40" fill="transparent" stroke="{e(colour)}"
                  stroke-width="7" stroke-linecap="round"
                  stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"/>
        </svg>
        <div class="gauge-c">
          <span class="gauge-num">{total}</span>
          <span class="gauge-max">/ 100 PTS</span>
        </div>
      </div>
      <span class="gauge-grade" style="background:{bg};border:1px solid {br};color:{fg}">
        <i class="tb-dot" style="background:{e(colour)}"></i>{e(score.get('grade', ''))}
      </span>
      <div class="gauge-split">
        <div class="gsp">
          <span class="gsp-k">Compliance</span>
          <span class="gsp-v">{pct(score['compliance_score'], score['compliance_max'])}</span>
          <span class="gsp-r">({score['compliance_score']:.0f}/{score['compliance_max']:.0f})</span>
        </div>
        <div class="gsp">
          <span class="gsp-k">Methodology</span>
          <span class="gsp-v">{pct(score['methodology_score'], score['methodology_max'])}</span>
          <span class="gsp-r">({score['methodology_score']:.0f}/{score['methodology_max']:.0f})</span>
        </div>
      </div>
      {cap}
    </div>"""


def render_verdict(score: dict) -> str:
    meth = score.get("_methodology", {})
    txt = (score.get("executive_summary") or meth.get("executive_summary")
           or _fallback_summary(score))
    return e(txt) if txt else ""


def _fallback_summary(score: dict) -> str:
    """Compose an exec summary from the data when the model omits one.

    Deliberately plain — it exists so the card is never blank, not to compete
    with the model's prose. Same vocabulary rule as the prompt: no criterion
    ids, no scores.
    """
    meth = score.get("_methodology", {})
    m = score.get("_metrics") or {}
    dims = meth.get("dimensions", [])
    if not dims:
        return ""

    best = max(dims, key=lambda d: d["pct"])
    worst = min(dims, key=lambda d: d["pct"])
    parts: list[str] = []
    strong = sum(1 for d in dims if d["band"] in ("good", "great"))
    verdict = ("went well overall" if strong >= len(dims) - 1
               else "was mixed" if strong >= len(dims) / 2 else "fell short")
    parts.append(f"This {(score.get('call_type') or 'call').replace('_', ' ')} {verdict}.")

    if best["pct"] >= 70:
        parts.append(f"The rep was strongest at {PLAIN_DIM.get(best['id'], best['name'].lower())}.")
    if worst["pct"] < 70:
        parts.append(f"The clearest gap was {PLAIN_DIM.get(worst['id'], worst['name'].lower())}.")

    sev = (score.get("_compliance") or {}).get("highest_severity")
    if sev in ("L2", "L3"):
        parts.append(f"An {sev} compliance issue was raised and caps the score "
                     f"regardless of selling quality.")
    elif m.get("customer_engagement_trend") == "shutting_down":
        parts.append("The customer said progressively less as the call went on, "
                     "which usually signals disengagement.")
    elif m.get("fee_discussed") and (m.get("rep_words_after_fee_15s") or 0) > 45:
        parts.append("The rep kept talking straight after stating the fee rather than "
                     "letting the customer respond.")
    return " ".join(parts)


def render_vitals(score: dict, stats: dict | None = None) -> str:
    """Six status-coloured cards. Each metric carries a threshold from the
    Bible, and the card takes its colour from whether that threshold held."""
    stats = stats or {}
    m = score.get("_metrics") or {}
    meth = score.get("_methodology", {})
    dims = meth.get("dimensions", [])

    def card(k, v, sub, cls="", cap="", small=False):
        return f"""
      <div class="vital {cls}">
        <div class="vital-top">
          <span class="vital-k">{k}</span>
          {f'<span class="vital-cap">{cap}</span>' if cap else ''}
        </div>
        <span class="vital-v{' sm' if small else ''}">{v}</span>
        <span class="vital-s">{sub}</span>
      </div>"""

    out = ""
    dur = stats.get("duration_seconds")
    out += card("Duration", _fmt_dur(dur), f"{int(dur):,}s elapsed" if dur else "&mdash;")

    ratio = stats.get("rep_talk_ratio_pct")
    if ratio is None:
        ratio = m.get("rep_talk_ratio_pct") or 0
    out += card("Talk Ratio", f"{ratio:.1f}%<small>rep</small>",
                f"{stats.get('rep_words', 0):,} rep / {stats.get('customer_words', 0):,} cust",
                "rose" if ratio > 60 else "emer", "Cap 60%")

    turns = (stats.get("sales_rep_utterances", 0) or 0) + (stats.get("customer_utterances", 0) or 0)
    out += card("Words &amp; Turns", f"{stats.get('total_words', 0):,}", f"{turns} turns total")

    if dims:
        best = max(dims, key=lambda d: d["pct"])
        worst = min(dims, key=lambda d: d["pct"])
        out += card("Strongest Pillar", e(best["name"]),
                    f"{best['pct']:.0f}% &middot; {best['points']:.1f} pts", "emer", small=True)
        out += card("Weakest Area", e(worst["name"]),
                    f"{worst['pct']:.0f}% &middot; {worst['points']:.1f} pts",
                    "amber" if worst["pct"] >= 35 else "rose", small=True)

    tj = meth.get("trust_journey", {})
    if tj.get("stages"):
        reached = sum(1 for s in tj["stages"] if s.get("reached"))
        name = next((n for i, n, _ in TRUST_STAGES
                     if i == tj.get("furthest_stage_reached")), "&mdash;")
        out += card("Trust Journey", f"{reached} / 5", f"reached {e(name)}",
                    "emer" if reached >= 4 else "amber")

    return f'<div class="vitals">{out}</div>'


# =============================================================================
# Rubric tab
# =============================================================================

def _accounting(score: dict) -> str:
    """Three cards showing exactly how the methodology total was reached."""
    meth = score.get("_methodology", {})
    pens = meth.get("penalties", {}) or {}
    pen_total = pens.get("total", 0) or 0
    n_pen = len(pens.get("applied", []))
    final = meth.get("score", 0)
    subtotal = final + pen_total
    n_dims = len(meth.get("dimensions", []))

    def card(k, sub, v, cls=""):
        return f"""
      <div class="cat {cls}" style="flex-direction:row;align-items:center;
           justify-content:space-between;gap:12px">
        <div>
          <span class="stat-k">{k}</span>
          <span class="cat-note" style="display:block">{sub}</span>
        </div>
        <span class="vital-v" style="font-size:16px;white-space:nowrap">{v}</span>
      </div>"""

    return f"""
    <div class="g3" style="margin-bottom:16px">
      {card("Methodology subtotal", f"{n_dims} scored chapters, normalised",
            f"{subtotal:.1f} pts")}
      {card("Habit deductions", f"{n_pen} behavioural {'penalty' if n_pen == 1 else 'penalties'}",
            f"&minus;{pen_total:.1f} pts", "fail")}
      {card("Final chapter total", f"Contribution to composite {score.get('total_score', 0)}",
            f"{final:.1f} / {meth.get('max', 60):.0f}")}
    </div>"""


def _behavioural(score: dict) -> str:
    """The measured behaviours behind the bands, as a seven-up grid."""
    m = score.get("_metrics") or {}
    meth = score.get("_methodology", {})
    dims = meth.get("dimensions", [])
    if not m and not dims:
        return ""

    def box(k, v, sub, tone=""):
        return f"""
        <div class="stat-box">
          <span class="stat-k">{k}</span>
          <span class="stat-v {tone}">{v}</span>
          <span class="stat-s">{sub}</span>
        </div>"""

    out = ""
    if dims:
        counts = Counter(d["band"] for d in dims)
        mix = " &middot; ".join(f"{counts[b]} {b}" for b in
                                ("great", "good", "average", "missing") if counts.get(b))
        na = len(meth.get("not_applicable", []))
        out += box("Rubric bands", mix or "&mdash;",
                   f"{len(dims)} scored" + (f" &middot; {na} n/a" if na else ""))

    pc = m.get("personalization_callback_count")
    if pc is not None:
        out += box("Personalisation", f"{pc}", "callbacks to their own words",
                   "ok" if pc >= 3 else "warn")

    q = m.get("rep_question_count")
    if q is not None:
        sl = m.get("second_level_question_count", 0)
        out += box("Questions asked", f"{q}", f"{sl} second-level",
                   "ok" if sl >= 3 else "warn")

    lm = m.get("longest_rep_monologue_sec")
    if lm is not None:
        out += box("Longest monologue", _fmt_dur(lm),
                   f"at {e(m.get('longest_rep_monologue_at') or '')} &middot; 3m is a penalty",
                   "crit" if lm > 180 else "ok")

    if m.get("fee_discussed"):
        w = m.get("rep_words_after_fee_15s")
        if w is not None:
            out += box("After stating fee", f"{w} words",
                       f"in the next 15s &middot; at {e(m.get('fee_first_mention_at') or '')}",
                       "crit" if w > 45 else "ok")

    oc = m.get("objection_count")
    if oc:
        dg = m.get("objections_with_diagnostic_response", 0)
        out += box("Objections raised", f"{oc}", f"{dg} met with a diagnostic question",
                   "ok" if dg == oc else "crit")

    trend = m.get("customer_engagement_trend")
    if trend and trend != "insufficient_data":
        label = {"opening_up": "Opening up", "steady": "Steady",
                 "shutting_down": "Shutting down"}.get(trend, trend)
        a, b = m.get("customer_words_first_half"), m.get("customer_words_second_half")
        out += box("Customer engagement", label,
                   f"{a:.0f} &rarr; {b:.0f} words per turn" if a and b else "across the call",
                   "crit" if trend == "shutting_down" else "ok")

    if not out:
        return ""
    return f"""
    <div class="panel">
      <div class="panel-head">
        <div class="panel-title">Behavioural Metrics</div>
        <span class="pill">Counted from the transcript</span>
      </div>
      <div class="panel-body"><div class="g4">{out}</div></div>
    </div>"""


def _trust_track(tj: dict) -> str:
    """Five stage cards. The earlier rail encoded progression but left no room
    to say why a stage was or was not reached, which is what makes the stall
    point actionable."""
    if not tj.get("stages"):
        return ""
    stages = {s["id"]: s for s in tj["stages"]}
    furthest = tj.get("furthest_stage_reached")
    reached = sum(1 for s in tj["stages"] if s.get("reached"))

    cells = ""
    for idx, (sid, name, feeling) in enumerate(TRUST_STAGES, start=1):
        st = stages.get(sid, {})
        done = bool(st.get("reached"))
        stall = sid == furthest and reached < 5
        cls = "tr" + (" done" if done and not stall else "") + (" stall" if stall else "")
        mark = _ico("check", "tr-ico") if done and not stall else (
            _ico("dot", "tr-ico") if stall else _ico("minus", "tr-ico"))
        cells += f"""
        <div class="{cls}">
          <div class="tr-top"><span>{idx:02d} {e(name.upper())}</span>{mark}</div>
          <span class="tr-note">{e(st.get("note") or feeling)}</span>
        </div>"""

    foot = ""
    if tj.get("where_it_stalled"):
        label = next((n for i, n, _ in TRUST_STAGES if i == furthest), "the start")
        foot = (f'<div class="stall-note">Stalled at <b>{e(label)}</b> &mdash; '
                f'{e(tj["where_it_stalled"])}</div>')

    tone = "ok" if reached == 5 else ("warn" if reached >= 3 else "crit")
    return f"""
    <div class="panel">
      <div class="panel-head">
        <div>
          <div class="panel-title">Trust Journey Progression</div>
          <div class="panel-sub">Framework 4 &middot; {reached} of 5 stages reached</div>
        </div>
        <span class="pill {tone}">{reached} / 5 reached</span>
      </div>
      <div class="panel-body">
        <div class="track">{cells}</div>
        {foot}
      </div>
    </div>"""


def _scorecard_table(score: dict, chapters: dict) -> str:
    meth = score.get("_methodology", {})
    dims = meth.get("dimensions", [])
    shown = _apportion([d["points"] for d in dims])

    rows = ""
    for d, pts in zip(dims, shown):
        rows += f"""
        <tr>
          <td class="sc-name">{e(d['name'])}<span class="sc-ch">{e(chapters.get(d['id'], ''))}</span></td>
          <td><span class="band {e(d['band'])}">{e(d['band'])}</span></td>
          <td class="sc-num">{d['pct']:.0f}%</td>
          <td class="sc-wt">{d.get('effective_weight', d.get('weight', 0)):.1f}%</td>
          <td class="sc-num">{pts:.1f}</td>
          <td class="sc-obs">{e(d.get('reasoning'))}</td>
        </tr>"""

    for na in meth.get("not_applicable", []):
        rows += f"""
        <tr>
          <td class="sc-name" style="color:var(--s400)">{e(na['name'])}
            <span class="sc-ch">{e(chapters.get(na['id'], ''))}</span></td>
          <td><span class="band na">N/A</span></td>
          <td class="sc-num" style="color:var(--s300)">&mdash;</td>
          <td class="sc-wt" style="color:var(--s300)">&mdash;</td>
          <td class="sc-num" style="color:var(--s300)">&mdash;</td>
          <td class="sc-obs" style="color:var(--s500)">Stage not reached &mdash; excluded from
            scoring. Its {na.get('weight', 0):.0f}% weight is redistributed across the criteria
            above, which is why their effective weights exceed their base weights.</td>
        </tr>"""

    pens = meth.get("penalties", {}) or {}
    pen_total = pens.get("total", 0) or 0
    subtotal = round(sum(shown), 1)
    final = meth.get("score", 0)

    pen_row = ""
    if pen_total:
        pen_row = f"""
          <tr class="sum">
            <td colspan="4" style="text-align:right">Habit deductions</td>
            <td class="sc-num" style="color:var(--rose)">&minus;{pen_total:.1f}</td><td></td>
          </tr>"""

    return f"""
      <table class="sc">
        <thead>
          <tr>
            <th>Chapter &amp; Evaluation Dimension</th><th>Band</th>
            <th style="text-align:right">Achieved</th><th style="text-align:right">Weight</th>
            <th style="text-align:right">Points</th><th>Coaching Observations</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
        <tfoot>
          <tr class="sum">
            <td colspan="4" style="text-align:right">Sales Bible subtotal</td>
            <td class="sc-num">{subtotal:.1f}</td><td></td>
          </tr>
          {pen_row}
          <tr class="tot">
            <td colspan="4" style="text-align:right">Methodology total</td>
            <td class="sc-num">{final:.1f} / {meth.get('max', 60):.0f}</td><td></td>
          </tr>
        </tfoot>
      </table>"""


def _drilldowns(score: dict, chapters: dict) -> str:
    """Per-dimension evidence: what happened, the Bible's standard, and a
    speakable alternative line."""
    meth = score.get("_methodology", {})
    out = ""
    for i, d in enumerate(meth.get("dimensions", []), start=1):
        quotes = "".join(
            f'<div class="dim-quote"><span class="dim-quote-k">Transcript '
            f'&middot; {e(q.get("timestamp"))}</span>{e(q.get("quote"))}</div>'
            for q in (d.get("evidence") or [])[:1])

        misses = ""
        for mo in (d.get("missed_opportunities") or [])[:2]:
            better = (f'<p class="dim-p dim-try"><b>Try instead:</b> &ldquo;'
                      f'{e(mo["better_response"])}&rdquo;</p>'
                      if mo.get("better_response") else "")
            misses += f"""
          <div class="dim-quote" style="background:var(--amber-bg);border-color:var(--amber-br)">
            <span class="dim-quote-k" style="color:var(--amber-d)">Missed opportunity
              &middot; {e(mo.get('timestamp'))}</span>
            <span style="font-style:normal">{e(mo.get('what_happened'))}</span>
          </div>
          <p class="dim-p"><b>The Bible says:</b> {e(mo.get('bible_says'))}</p>
          {better}"""

        ts = ""
        ev = d.get("evidence") or []
        if ev and ev[0].get("timestamp"):
            ts = e(ev[0]["timestamp"])

        out += f"""
      <div class="dim">
        <div class="dim-top">
          <div class="dim-l">
            <i class="dim-dot"></i>
            <span class="dim-name">{i}. {e(d['name'])} ({e(chapters.get(d['id'], ''))})</span>
            <span class="band {e(d['band'])}">{e(d['band'])} &middot; {d['pct']:.0f}%</span>
          </div>
          {f'<span class="dim-ts">{ts}</span>' if ts else ''}
        </div>
        <p class="dim-p"><b>What happened:</b> {e(d.get('reasoning'))}</p>
        {quotes}{misses}
      </div>"""
    return out


def _penalties_panel(score: dict) -> str:
    meth = score.get("_methodology", {})
    pens = meth.get("penalties", {}) or {}
    applied = pens.get("applied", [])
    if not applied:
        return ""

    rows = ""
    for p in applied:
        label = str(p.get("signal", "")).replace("_", " ").capitalize()
        rows += f"""
        <div class="pen">
          <div class="pen-top">
            <span class="pen-k">{e(label)}</span>
            <span class="pen-v">&minus;{p.get('points', 0)} pts</span>
          </div>
          <p class="pen-note">{e(p.get('reason'))}</p>
        </div>"""

    note = ""
    if pens.get("proportionally_capped"):
        note = ('<p class="pen-note" style="margin-top:10px">Penalties are capped at a share of '
                'the points earned, so behaviour already reflected in the band ratings is not '
                'deducted twice.</p>')

    return f"""
      <div class="pen-wrap">
        <div class="pen-h">{_ico("gavel", "row-ico")}Behavioural penalties explained
          (&minus;{pens.get('total', 0):.1f} pts)</div>
        {rows}{note}
      </div>"""


def _coaching(score: dict) -> str:
    c = score.get("coaching_summary") or {}
    if not c:
        return ""
    rows = ""
    for key, label in (("top_strength", "Top strength"),
                       ("top_priority", "Highest-leverage fix"),
                       ("one_behaviour_to_practice", "Next 10 calls")):
        if c.get(key):
            rows += (f'<div class="coach-row"><span class="coach-k">{label}</span>'
                     f'<span class="coach-v">{e(c[key])}</span></div>')
    return f'<div class="coach">{rows}</div>' if rows else ""


def _four_whys(items: list[dict]) -> str:
    if not items:
        return ""
    tone = {"answered": ("ok", "check", "ANSWERED"),
            "partial": ("warn", "half", "PARTIAL"),
            "unanswered": ("bad", "cross", "UNANSWERED"),
            "not_applicable": ("", "minus", "N/A")}
    rows = ""
    for w in items:
        cls, icon, tag = tone.get(w.get("status", "unanswered"), tone["unanswered"])
        rows += f"""
        <div class="row {cls}">
          {_ico(icon)}
          <div>
            <span class="row-k">{e(WHY_LABELS.get(w.get('id'), w.get('id')))}</span>
            <span class="row-tag">[{tag}]</span>
            <div class="row-note">{e(w.get('note'))}</div>
          </div>
        </div>"""
    ans = sum(1 for w in items if w.get("status") == "answered")
    pill = "ok" if ans == len(items) else ("warn" if ans >= len(items) / 2 else "crit")
    return f"""
    <div class="panel">
      <div class="panel-head">
        <div class="panel-title">The 4 WHYs Strategic Alignment</div>
        <span class="pill {pill}">{ans} of {len(items)} answered</span>
      </div>
      <div class="panel-body"><div class="rows">{rows}</div></div>
    </div>"""


def _hfte(items: list[dict]) -> str:
    if not items:
        return ""
    tone = {"addressed": ("ok", "check", "Fully addressed"),
            "partially_addressed": ("warn", "half", "Partially addressed"),
            "not_addressed": ("bad", "cross", "Not addressed")}
    role = {"hope": "Driver", "trust": "Driver", "fear": "Inhibitor", "effort": "Inhibitor"}
    by = {i.get("id"): i for i in items}
    rows = ""
    for k in ("hope", "trust", "fear", "effort"):
        it = by.get(k)
        if not it:
            continue
        cls, icon, tag = tone.get(it.get("status", "not_addressed"), tone["not_addressed"])
        rows += f"""
        <div class="row {cls}">
          {_ico(icon)}
          <div>
            <span class="row-k">{e(HFTE_LABELS.get(k, k))} ({role.get(k, '')})</span>
            <span class="row-tag">{tag}</span>
            <div class="row-note">{e(it.get('note'))}</div>
          </div>
        </div>"""
    return f"""
    <div class="panel">
      <div class="panel-head">
        <div class="panel-title">HFTE Psychological Balance</div>
        <span class="pill">Drivers vs inhibitors</span>
      </div>
      <div class="panel-body"><div class="rows">{rows}</div></div>
    </div>"""


def render_diagnostics(score: dict) -> str:
    """The 4 WHYs and HFTE pair, rendered for the Sales Intelligence tab."""
    meth = (score or {}).get("_methodology", {})
    whys = _four_whys(meth.get("four_whys", []))
    hfte = _hfte(meth.get("hfte_balance", []))
    if not (whys or hfte):
        return ""
    return f'<div class="duo">{whys}{hfte}</div>'


def render_methodology_section(score: dict, chapters: dict[str, str] | None = None) -> str:
    """The Rubric & Methodology tab.

    Detail lives in <details> accordions so the tab opens as a summary a
    manager can read, and expands into the full audit trail when someone needs
    to defend a number. Accordions work with no JavaScript and print expanded.
    """
    chapters = chapters or {}
    meth = score.get("_methodology", {})
    if not meth:
        return ""

    warn = ""
    if score.get("low_confidence"):
        warn = """
    <div class="panel" style="border-color:var(--amber-br);background:var(--amber-bg)">
      <div class="panel-body" style="font-size:12.5px;color:var(--amber-d);padding:14px 18px">
        <b>Low confidence.</b> This call was short, one-sided, or reached too few stages for a
        reliable methodology read. Treat the score as indicative and review manually.
      </div>
    </div>"""

    n_dims = len(meth.get("dimensions", []))
    na = len(meth.get("not_applicable", []))

    return f"""
  {warn}
  {_accounting(score)}
  {_behavioural(score)}
  {_trust_track(meth.get('trust_journey', {}))}

  <div class="acc-bar">
    <span class="acc-bar-k">Methodology drilldowns &amp; transcript evidence</span>
    <button type="button" class="acc-btn" data-expand-all hidden>Expand all details</button>
  </div>

  <details class="acc" open>
    <summary>
      <div class="acc-head-l">
        {_ico("chev", "acc-chev")}
        <div>
          <div class="panel-title">Full Sales Bible Scorecard</div>
          <div class="panel-sub">{n_dims} chapters scored
            {f'&middot; {na} excluded, weights normalised' if na else ''}</div>
        </div>
      </div>
      <span class="pill blue">{meth.get('score', 0):.1f} / {meth.get('max', 60):.0f} pts</span>
    </summary>
    <div class="acc-body" style="padding:0">{_scorecard_table(score, chapters)}</div>
  </details>

  <details class="acc">
    <summary>
      <div class="acc-head-l">
        {_ico("chev", "acc-chev")}
        <div>
          <div class="panel-title">Chapter-by-Chapter Evidence</div>
          <div class="panel-sub">What happened, the standard, and what to say instead</div>
        </div>
      </div>
      <span class="pill">{n_dims} dimensions</span>
    </summary>
    <div class="acc-body">{_drilldowns(score, chapters)}</div>
  </details>

  {f'<div class="section">{_penalties_panel(score)}</div>' if _penalties_panel(score) else ''}
  {f'<div class="section">{_coaching(score)}</div>' if _coaching(score) else ''}
"""
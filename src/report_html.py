# # """Generate a self-contained HTML report from a call-quality report JSON file.

# # Usage:
# #     python src/report_html.py output/0.report.json
# #     # writes output/0.report.html
# # """

# # import json
# # import os
# # import sys
# # from html import escape as html_escape
# # from src.report_methodology import (methodology_css, render_methodology_section,
# #                                     render_score_banner, render_call_snapshot,
# #                                     render_ribbon, render_verdict)
# # from src.report_tabs import tabs_css, render_tabs

# # CHAPTERS = {
# #     "customer_profiling": "Ch 5", "need_identification": "Ch 6",
# #     "vision_setting": "Ch 7",     "program_mapping": "Ch 8",
# #     "fee_and_urgency": "Ch 9",    "objection_handling": "Ch 10",
# #     "trust_journey": "Framework 4",
# # }

# # def escape(s):
# #     if s is None:
# #         return ""
# #     return html_escape(str(s))


# # SEV_LABELS = {"L1": "Minor", "L2": "Major", "L3": "Critical", "None": "Clean"}
# # SEV_BADGE_CLASS = {"L1": "sev-L1", "L2": "sev-L2", "L3": "sev-L3", "None": "sev-None"}
# # PRIORITY_CLASS = {"Immediate": "immediate", "Short-term": "short-term", "Follow-up": "follow-up"}

# # CSS = """
# #     /* =====================================================================
# #        Accredian Call Quality — design system

# #        Audit-record language: mono for anything a machine measured, sans for
# #        anything a person wrote. Tabular numerals throughout. Colour is reserved
# #        for status; the accent marks interaction only.

# #        No webfonts and no CDN: these reports are emailed and opened from disk,
# #        so a network dependency means a broken document offline. The stacks
# #        below resolve to Inter-class and SF-Mono-class faces natively on macOS,
# #        Windows and most Linux desktops.
# #        ===================================================================== */
# #     *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

# #     :root {
# #       --ink-950:#090d16; --ink-900:#0f172a; --ink-800:#1e293b; --ink-700:#334155;
# #       --ink-600:#475569; --ink-500:#64748b; --ink-400:#94a3b8; --ink-300:#cbd5e1;
# #       --ink-200:#e2e8f0; --ink-100:#f1f5f9; --ink-50:#f8fafc;

# #       --accent:#2563eb; --accent-hover:#1d4ed8; --accent-subtle:#eff6ff;
# #       --critical:#dc2626; --critical-bg:#fef2f2; --critical-border:#fee2e2; --critical-deep:#991b1b;
# #       --warning:#d97706; --warning-bg:#fffbeb; --warning-border:#fef3c7; --warning-deep:#92400e;
# #       --success:#059669; --success-bg:#ecfdf5; --success-border:#d1fae5; --success-deep:#065f46;

# #       --sans: -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI",
# #               Inter, Roboto, "Helvetica Neue", Arial, sans-serif;
# #       --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
# #               "Liberation Mono", "Courier New", monospace;

# #       --r: 12px;
# #       --shadow-subtle: 0 1px 2px 0 rgba(15,23,42,.04), 0 1px 3px 0 rgba(15,23,42,.02);
# #       --shadow-card: 0 0 0 1px rgba(15,23,42,.06), 0 1px 2px 0 rgba(15,23,42,.03);
# #     }

# #     body {
# #       font-family: var(--sans);
# #       font-size: 14px; line-height: 1.6;
# #       color: var(--ink-900); background: var(--ink-50);
# #       font-variant-numeric: tabular-nums;
# #       -webkit-font-smoothing: antialiased;
# #       -moz-osx-font-smoothing: grayscale;
# #     }
# #     .tabular, .mono { font-variant-numeric: tabular-nums; }
# #     .mono { font-family: var(--mono); }

# #     .page { max-width: 1180px; margin: 0 auto; padding: 0 24px 88px; }

# #     /* ---- Sticky identity bar ---- */
# #     .topbar {
# #       position: sticky; top: 0; z-index: 50;
# #       background: var(--ink-950); color: #fff;
# #       border-bottom: 1px solid var(--ink-800);
# #       margin-bottom: 28px;
# #     }
# #     .topbar-inner {
# #       max-width: 1180px; margin: 0 auto; padding: 0 24px;
# #       height: 56px; display: flex; align-items: center;
# #       justify-content: space-between; gap: 16px;
# #     }
# #     .brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
# #     .brand-mark {
# #       width: 28px; height: 28px; border-radius: 6px; flex: none;
# #       background: #fff; color: var(--ink-950);
# #       display: flex; align-items: center; justify-content: center;
# #       font-family: var(--mono); font-weight: 700; font-size: 11px; letter-spacing: -0.5px;
# #     }
# #     .brand-name {
# #       font-family: var(--mono); font-size: 11.5px; font-weight: 600;
# #       text-transform: uppercase; letter-spacing: .04em; color: #fff;
# #     }
# #     .brand-sep { color: var(--ink-600); font-size: 12px; }
# #     .brand-sub {
# #       font-family: var(--mono); font-size: 11px; color: var(--ink-400);
# #       white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
# #     }
# #     .topbar-status { display: flex; align-items: center; gap: 8px; flex: none; }
# #     .chip {
# #       display: inline-flex; align-items: center; gap: 6px;
# #       padding: 3px 10px; border-radius: 5px;
# #       font-family: var(--mono); font-size: 10.5px; font-weight: 500;
# #       white-space: nowrap;
# #     }
# #     .chip-dot { width: 6px; height: 6px; border-radius: 50%; flex: none; }
# #     .chip-critical { background: rgba(220,38,38,.18); color: #fca5a5;
# #                      border: 1px solid rgba(220,38,38,.35); }
# #     .chip-critical .chip-dot { background: #f87171; }
# #     .chip-ok { background: rgba(5,150,105,.18); color: #6ee7b7;
# #                border: 1px solid rgba(5,150,105,.35); }
# #     .chip-ok .chip-dot { background: #34d399; }
# #     .chip-muted { background: rgba(255,255,255,.07); color: var(--ink-300);
# #                   border: 1px solid rgba(255,255,255,.13); }

# #     /* ---- Hero record card ---- */
# #     .record {
# #       background: #fff; border: 1px solid var(--ink-200);
# #       border-radius: var(--r); box-shadow: var(--shadow-subtle);
# #       overflow: hidden; margin-bottom: 22px;
# #     }
# #     .record-body {
# #       display: grid; grid-template-columns: minmax(0,1fr) 300px;
# #       gap: 32px; padding: 28px 30px;
# #     }
# #     .eyebrow {
# #       font-family: var(--mono); font-size: 11px; color: var(--ink-500);
# #       letter-spacing: .02em; margin-bottom: 12px;
# #     }
# #     .eyebrow b { color: var(--ink-700); font-weight: 600; }
# #     .record h1 {
# #       font-size: 27px; font-weight: 700; letter-spacing: -0.6px;
# #       color: var(--ink-950); line-height: 1.18;
# #     }
# #     .parties {
# #       display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
# #       margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--ink-100);
# #     }
# #     .party-name { font-size: 14.5px; font-weight: 650; color: var(--ink-900); }
# #     .party-role { font-size: 12px; color: var(--ink-500); font-family: var(--mono); }
# #     .party-arrow { color: var(--ink-300); font-size: 15px; }
# #     .verdict {
# #       margin-top: 16px; font-size: 14px; line-height: 1.68; color: var(--ink-700);
# #     }
# #     .verdict strong { color: var(--ink-950); font-weight: 600; }

# #     /* ---- Composite score dial ---- */
# #     .dial {
# #       background: var(--ink-50); border: 1px solid var(--ink-200);
# #       border-radius: var(--r); padding: 22px 20px;
# #       display: flex; flex-direction: column; align-items: center; gap: 14px;
# #     }
# #     .dial-label {
# #       font-family: var(--mono); font-size: 10.5px; font-weight: 600;
# #       text-transform: uppercase; letter-spacing: .06em; color: var(--ink-500);
# #     }
# #     .dial-ring { position: relative; width: 116px; height: 116px; }
# #     .dial-ring svg { transform: rotate(-90deg); width: 116px; height: 116px; }
# #     .dial-centre {
# #       position: absolute; inset: 0;
# #       display: flex; flex-direction: column; align-items: center; justify-content: center;
# #     }
# #     .dial-num { font-size: 32px; font-weight: 700; color: var(--ink-950);
# #                 letter-spacing: -1px; line-height: 1; }
# #     .dial-max { font-family: var(--mono); font-size: 9.5px; color: var(--ink-400);
# #                 text-transform: uppercase; margin-top: 3px; letter-spacing: .04em; }
# #     .dial-grade {
# #       display: inline-flex; align-items: center; gap: 7px;
# #       padding: 5px 12px; border-radius: 6px;
# #       font-family: var(--mono); font-size: 11.5px; font-weight: 600;
# #     }
# #     .dial-split {
# #       width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
# #       padding-top: 13px; border-top: 1px solid var(--ink-200);
# #       font-family: var(--mono); font-size: 10px;
# #     }
# #     .dial-split-k { display: block; color: var(--ink-500); margin-bottom: 2px; }
# #     .dial-split-v { font-size: 12.5px; font-weight: 700; color: var(--ink-900); }
# #     .dial-split-r { color: var(--ink-400); }

# #     /* ---- Telemetry ribbon ---- */
# #     .ribbon {
# #       background: var(--ink-100); border-top: 1px solid var(--ink-200);
# #       padding: 14px 30px;
# #       display: grid; grid-template-columns: repeat(6, 1fr); gap: 0;
# #       font-family: var(--mono);
# #     }
# #     .ribbon-cell { padding: 0 16px; border-left: 1px solid var(--ink-200); min-width: 0; }
# #     .ribbon-cell:first-child { border-left: none; padding-left: 0; }
# #     .ribbon-k {
# #       display: block; font-size: 9.5px; color: var(--ink-500); font-weight: 500;
# #       text-transform: uppercase; letter-spacing: .05em; margin-bottom: 3px;
# #     }
# #     .ribbon-v {
# #       display: block; font-size: 13.5px; font-weight: 700; color: var(--ink-900);
# #       line-height: 1.25; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
# #     }
# #     .ribbon-v small { font-size: 10.5px; font-weight: 400; color: var(--ink-600); }
# #     .ribbon-s { display: block; font-size: 9.5px; color: var(--ink-500); margin-top: 2px; }
# #     .v-crit { color: var(--critical) !important; }
# #     .v-warn { color: var(--warning-deep) !important; }
# #     .v-ok   { color: var(--success-deep) !important; }

# #     .refbar {
# #       background: var(--ink-50); border-top: 1px solid var(--ink-200);
# #       padding: 10px 30px; font-family: var(--mono); font-size: 10.5px;
# #       color: var(--ink-500); display: flex; flex-wrap: wrap; gap: 6px 20px;
# #     }
# #     .refbar b { color: var(--ink-700); font-weight: 600; }

# #     /* ---- Sections ---- */
# #     .section { margin-bottom: 26px; }
# #     .section-title {
# #       font-family: var(--mono); font-size: 11.5px; font-weight: 700;
# #       text-transform: uppercase; letter-spacing: .07em; color: var(--ink-950);
# #       padding-bottom: 10px; margin-bottom: 14px;
# #       border-bottom: 1px solid var(--ink-200);
# #       display: flex; align-items: center; justify-content: space-between; gap: 12px;
# #     }
# #     .section-title .count {
# #       font-size: 10.5px; font-weight: 500; color: var(--ink-500);
# #       text-transform: none; letter-spacing: 0;
# #     }

# #     .card {
# #       background: #fff; border: 1px solid var(--ink-200);
# #       border-radius: var(--r); box-shadow: var(--shadow-subtle);
# #       padding: 22px 24px;
# #     }

# #     /* ---- Stat grid ---- */
# #     .stats-grid {
# #       display: grid; grid-template-columns: repeat(4, 1fr); gap: 0;
# #       background: #fff; border: 1px solid var(--ink-200);
# #       border-radius: var(--r); box-shadow: var(--shadow-subtle); overflow: hidden;
# #     }
# #     .stat-card {
# #       padding: 15px 18px; display: flex; flex-direction: column; gap: 4px;
# #       border-right: 1px solid var(--ink-100); border-bottom: 1px solid var(--ink-100);
# #       min-height: 86px;
# #     }
# #     .stat-card:nth-child(4n) { border-right: none; }
# #     .stat-card:nth-last-child(-n+4) { border-bottom: none; }
# #     .stat-label {
# #       font-family: var(--mono); font-size: 9.5px; font-weight: 500; color: var(--ink-500);
# #       text-transform: uppercase; letter-spacing: .05em;
# #     }
# #     .stat-value { font-size: 19px; font-weight: 700; color: var(--ink-950);
# #                   letter-spacing: -0.4px; line-height: 1.22; }
# #     .stat-sub { font-size: 11px; color: var(--ink-500); font-family: var(--mono); }

# #     @media (max-width: 1060px) {
# #       .record-body { grid-template-columns: minmax(0,1fr); }
# #       .ribbon { grid-template-columns: repeat(3, 1fr); gap: 14px 0; }
# #       .ribbon-cell:nth-child(3n+1) { border-left: none; padding-left: 0; }
# #     }
# #     @media (max-width: 720px) {
# #       .page { padding: 0 14px 64px; }
# #       .topbar-inner { padding: 0 14px; height: auto; min-height: 52px;
# #                       flex-wrap: wrap; gap: 8px; padding-top: 9px; padding-bottom: 9px; }
# #       .brand-sub { display: none; }
# #       .record-body { padding: 22px 18px; gap: 22px; }
# #       .record h1 { font-size: 21px; }
# #       .ribbon { grid-template-columns: repeat(2, 1fr); padding: 14px 18px; }
# #       .ribbon-cell:nth-child(3n+1) { border-left: 1px solid var(--ink-200); padding-left: 16px; }
# #       .ribbon-cell:nth-child(2n+1) { border-left: none; padding-left: 0; }
# #       .refbar { padding: 10px 18px; }
# #       .stats-grid { grid-template-columns: repeat(2, 1fr); }
# #       .stat-card:nth-child(4n) { border-right: 1px solid var(--ink-100); }
# #       .stat-card:nth-child(2n) { border-right: none; }
# #       .stat-card:nth-last-child(-n+4) { border-bottom: 1px solid var(--ink-100); }
# #       .stat-card:nth-last-child(-n+2) { border-bottom: none; }
# #     }



# #     /* ---- Panel: the repeating container for every content block ----
# #        White card, header strip carrying a title, an optional data sub-line and
# #        a mono status pill on the right, then the body. Every section uses it, so
# #        a reader learns the shape once and can then scan straight to the pill. */
# #     .panel {
# #       background: #fff; border: 1px solid var(--ink-200); border-radius: var(--r);
# #       box-shadow: var(--shadow-subtle); overflow: hidden; margin-bottom: 16px;
# #     }
# #     .panel-head {
# #       display: flex; align-items: flex-start; justify-content: space-between;
# #       gap: 14px; flex-wrap: wrap;
# #       padding: 16px 20px; border-bottom: 1px solid var(--ink-100);
# #     }
# #     .panel-title { font-size: 13.5px; font-weight: 700; color: var(--ink-950); }
# #     .panel-sub { font-size: 11.5px; color: var(--ink-500); margin-top: 3px; font-family: var(--mono); }
# #     .panel-pill {
# #       font-family: var(--mono); font-size: 11px; font-weight: 600;
# #       padding: 5px 11px; border-radius: 6px; white-space: nowrap;
# #       background: var(--ink-100); color: var(--ink-700); border: 1px solid var(--ink-200);
# #     }
# #     .panel-pill.ok   { background: var(--success-bg); color: var(--success-deep); border-color: var(--success-border); }
# #     .panel-pill.warn { background: var(--warning-bg); color: var(--warning-deep); border-color: var(--warning-border); }
# #     .panel-pill.crit { background: var(--critical-bg); color: var(--critical-deep); border-color: var(--critical-border); }
# #     .panel-pill.accent { background: var(--accent-subtle); color: #1e40af; border-color: #bfdbfe; }
# #     .panel-body { padding: 18px 20px; }

# #     .tally { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; }
# #     .tally-item {
# #       display: inline-flex; align-items: center; gap: 6px;
# #       font-family: var(--mono); font-size: 11px; font-weight: 500;
# #       padding: 4px 10px; border-radius: 5px;
# #       background: var(--ink-100); color: var(--ink-600); border: 1px solid var(--ink-200);
# #     }
# #     .tally-item i { width: 6px; height: 6px; border-radius: 50%; flex: none; }
# #     .tally-item.crit { background: var(--critical-bg); color: var(--critical-deep); border-color: var(--critical-border); }
# #     .tally-item.crit i { background: var(--critical); }
# #     .tally-item.warn { background: var(--warning-bg); color: var(--warning-deep); border-color: var(--warning-border); }
# #     .tally-item.warn i { background: var(--warning); }
# #     .tally-item.ok { background: var(--success-bg); color: var(--success-deep); border-color: var(--success-border); }
# #     .tally-item.ok i { background: var(--success); }

# #     /* Paired evidence: what was said beside what is true. Reading them
# #        side by side is the whole point of the finding. */
# #     .evidence-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
# #     .ev {
# #       padding: 13px 15px; border-radius: 9px; display: flex;
# #       flex-direction: column; gap: 6px;
# #     }
# #     .ev-said { background: var(--ink-50); border: 1px solid var(--ink-200); }
# #     .ev-true { background: var(--success-bg); border: 1px solid var(--success-border); }
# #     .ev-k {
# #       font-family: var(--mono); font-size: 9.5px; font-weight: 700;
# #       text-transform: uppercase; letter-spacing: .06em;
# #     }
# #     .ev-said .ev-k { color: var(--critical-deep); }
# #     .ev-true .ev-k { color: var(--success-deep); }
# #     .ev-v { font-size: 12.5px; line-height: 1.6; color: var(--ink-900); }
# #     .ev-said .ev-v {
# #       font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
# #       font-style: italic;
# #     }
# #     .grounds { font-size: 12.5px; line-height: 1.65; color: var(--ink-700); margin-bottom: 14px; }
# #     .grounds b { color: var(--ink-950); font-weight: 650; }
# #     .incident-foot {
# #       display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
# #       margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--ink-100);
# #       font-family: var(--mono); font-size: 10.5px; color: var(--ink-500);
# #     }
# #     .incident-foot b { color: var(--ink-900); font-weight: 600; }

# #     /* ---- Category grid: checklist, trust stages, why/hfte rows ---- */
# #     .cat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
# #     .cat {
# #       padding: 13px 15px; border-radius: 9px;
# #       border: 1px solid var(--ink-200); background: #fff;
# #       display: flex; flex-direction: column; gap: 6px;
# #     }
# #     .cat.fail { border-color: var(--critical-border); background: #fffafa; }
# #     .cat-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
# #     .cat-name { font-size: 12.5px; font-weight: 700; color: var(--ink-950); }
# #     .cat.fail .cat-name { color: var(--critical-deep); }
# #     .cat-count {
# #       font-family: var(--mono); font-size: 9.5px; font-weight: 500;
# #       padding: 2px 8px; border-radius: 4px; white-space: nowrap;
# #       background: var(--success-bg); color: var(--success-deep); border: 1px solid var(--success-border);
# #     }
# #     .cat-count.fail { background: var(--critical-bg); color: var(--critical-deep); border-color: var(--critical-border); }
# #     .cat-count.nd { background: var(--ink-100); color: var(--ink-600); border-color: var(--ink-200); }
# #     .cat-note { font-size: 11.5px; line-height: 1.55; color: var(--ink-600); }
# #     .cat-note .f { color: var(--critical); font-weight: 650; }

# #     .stage-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
# #     .stage {
# #       padding: 12px 13px; border-radius: 9px;
# #       border: 1px solid var(--ink-200); background: var(--ink-50);
# #       display: flex; flex-direction: column; gap: 6px;
# #     }
# #     .stage.done { background: var(--success-bg); border-color: var(--success-border); }
# #     .stage.stall { background: var(--warning-bg); border-color: var(--warning-border); }
# #     .stage-top {
# #       display: flex; align-items: center; justify-content: space-between; gap: 6px;
# #       font-family: var(--mono); font-size: 9.5px; font-weight: 700;
# #       letter-spacing: .04em; color: var(--ink-500);
# #     }
# #     .stage.done .stage-top { color: var(--success-deep); }
# #     .stage.stall .stage-top { color: var(--warning-deep); }
# #     .stage-note { font-size: 11px; line-height: 1.5; color: var(--ink-700); }

# #     .row-list { display: flex; flex-direction: column; gap: 9px; }
# #     .row-item {
# #       display: flex; align-items: flex-start; gap: 10px;
# #       padding: 11px 13px; border-radius: 9px;
# #       border: 1px solid var(--ink-200); background: var(--ink-50);
# #     }
# #     .row-item.ok   { background: var(--success-bg); border-color: var(--success-border); }
# #     .row-item.warn { background: var(--warning-bg); border-color: var(--warning-border); }
# #     .row-item.bad  { background: var(--critical-bg); border-color: var(--critical-border); }
# #     .row-ico { width: 16px; height: 16px; flex: none; margin-top: 1px; }
# #     .row-k { font-size: 12.5px; font-weight: 700; color: var(--ink-950); }
# #     .row-tag { font-family: var(--mono); font-size: 10px; font-weight: 600; margin-left: 5px; }
# #     .row-item.ok .row-tag { color: var(--success-deep); }
# #     .row-item.warn .row-tag { color: var(--warning-deep); }
# #     .row-item.bad .row-tag { color: var(--critical-deep); }
# #     .row-note { font-size: 11.5px; line-height: 1.55; color: var(--ink-600); margin-top: 3px; }

# #     .duo { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

# #     @media (max-width: 1000px) {
# #       .cat-grid { grid-template-columns: repeat(2, 1fr); }
# #       .stage-grid { grid-template-columns: repeat(3, 1fr); }
# #     }
# #     @media (max-width: 760px) {
# #       .evidence-pair, .duo { grid-template-columns: 1fr; }
# #       .cat-grid, .stage-grid { grid-template-columns: 1fr; }
# #     }

# #     /* ---- Incident summary pills ---- */
# #     .summary-pills { display: flex; flex-wrap: wrap; gap: 10px; }
# #     .pill {
# #       flex: 1 1 130px; display: flex; flex-direction: column; gap: 3px;
# #       padding: 13px 16px; border-radius: 9px; border: 1px solid var(--ink-200);
# #       background: #fff;
# #     }
# #     .pill-count { font-size: 24px; font-weight: 700; line-height: 1.1; letter-spacing: -0.6px; }
# #     .pill-label {
# #       font-family: var(--mono); font-size: 10px; font-weight: 500;
# #       text-transform: uppercase; letter-spacing: .05em; color: var(--ink-500);
# #     }
# #     .pill.l1 { background: var(--warning-bg); border-color: var(--warning-border); }
# #     .pill.l1 .pill-count { color: var(--warning-deep); }
# #     .pill.l2 { background: #fff7ed; border-color: #fed7aa; }
# #     .pill.l2 .pill-count { color: #c2410c; }
# #     .pill.l3 { background: var(--critical-bg); border-color: var(--critical-border); }
# #     .pill.l3 .pill-count { color: var(--critical-deep); }
# #     .pill.total { background: var(--ink-950); border-color: var(--ink-950); }
# #     .pill.total .pill-count { color: #fff; }
# #     .pill.total .pill-label { color: var(--ink-400); }

# #     /* ---- Incident cards ---- */
# #     .incident-card {
# #       border: 1px solid var(--ink-200); border-radius: var(--r);
# #       background: #fff; box-shadow: var(--shadow-subtle);
# #       margin-bottom: 14px; overflow: hidden;
# #     }
# #     .incident-header {
# #       display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
# #       padding: 13px 18px; background: var(--ink-50);
# #       border-bottom: 1px solid var(--ink-200);
# #     }
# #     .incident-id {
# #       font-family: var(--mono); font-size: 10.5px; font-weight: 700;
# #       padding: 3px 9px; border-radius: 5px;
# #       background: var(--ink-950); color: #fff;
# #     }
# #     .incident-category { font-size: 13px; font-weight: 650; color: var(--ink-950); flex: 1; }
# #     .incident-ts {
# #       font-family: var(--mono); font-size: 11px; color: var(--ink-500);
# #       background: var(--ink-100); padding: 2px 8px; border-radius: 4px;
# #     }
# #     .incident-grid { padding: 16px 18px; display: flex; flex-direction: column; gap: 13px; }
# #     .incident-field { display: flex; flex-direction: column; gap: 4px; }
# #     .field-label {
# #       font-family: var(--mono); font-size: 9.5px; font-weight: 600;
# #       text-transform: uppercase; letter-spacing: .06em; color: var(--ink-500);
# #     }
# #     .field-value { font-size: 13px; color: var(--ink-700); line-height: 1.62; }
# #     .transcript-quote {
# #       border-left: 3px solid var(--critical); background: var(--critical-bg);
# #       padding: 9px 14px; border-radius: 0 6px 6px 0;
# #       font-size: 12.5px; color: var(--critical-deep); font-style: italic;
# #     }
# #     .violation-basis { font-size: 12.5px; color: var(--ink-600); padding: 0 18px 16px; }
# #     .transcript-quote:empty, .violation-basis:empty, .field-value:empty { display: none; }
# #     .incident-card .transcript-quote { margin: 0 18px 12px; }
# #     .correct {
# #       border-left: 3px solid var(--success); background: var(--success-bg);
# #       padding: 9px 14px; border-radius: 0 6px 6px 0;
# #       font-size: 12.5px; color: var(--success-deep);
# #     }

# #     .severity-badge {
# #       display: inline-flex; align-items: center; gap: 5px;
# #       font-family: var(--mono); font-size: 10px; font-weight: 600;
# #       padding: 3px 9px; border-radius: 5px;
# #       background: var(--ink-100); color: var(--ink-600); border: 1px solid var(--ink-200);
# #     }
# #     .severity-badge.sev-L1 { background: var(--warning-bg); color: var(--warning-deep);
# #                              border-color: var(--warning-border); }
# #     .severity-badge.sev-L2 { background: #fff7ed; color: #c2410c; border-color: #fed7aa; }
# #     .severity-badge.sev-L3 { background: var(--critical-bg); color: var(--critical-deep);
# #                              border-color: var(--critical-border); }

# #     /* Severity colours the card's edge, never its field. A tinted body makes
# #        the rep's quote hard to read and shouts louder than the finding. */
# #     .incident-card.sev-L1 { border-left: 3px solid var(--warning); }
# #     .incident-card.sev-L2 { border-left: 3px solid #ea580c; }
# #     .incident-card.sev-L3 { border-left: 3px solid var(--critical); }

# #     .snapshot { margin-bottom: 24px; }
# #     .footer {
# #       font-family: var(--mono); font-size: 10.5px; color: var(--ink-400);
# #       text-align: center; padding-top: 26px; margin-top: 10px;
# #       border-top: 1px solid var(--ink-200);
# #     }

# #     /* ---- QA checklist: coverage, not a 47-row table ---- */
# #     .ck-legend { display: inline-flex; align-items: center; gap: 6px;
# #                  font-family: var(--mono); font-size: 10.5px; font-weight: 500; color: var(--muted);
# #                  text-transform: none; letter-spacing: 0; }
# #     .ck-legend .ck-dot { margin-left: 6px; }

# #     .ck-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%;
# #               flex: none; }
# #     .ck-pass { background: #34d399; }
# #     .ck-fail { background: #f87171; }
# #     .ck-nd   { background: #d7dde6; }

# #     .ck-cat { border-bottom: 1px solid var(--rule-soft); }
# #     .ck-cat:last-child { border-bottom: none; }
# #     .ck-cat > summary {
# #       display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
# #       padding: 13px 20px; cursor: pointer; list-style: none;
# #       transition: background .12s ease;
# #     }
# #     .ck-cat > summary::-webkit-details-marker { display: none; }
# #     .ck-cat > summary:hover { background: #fafbfc; }
# #     .ck-cat > summary:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
# #     .ck-cat-name { font-size: 12.5px; font-weight: 650; color: var(--strong); min-width: 176px; }
# #     .ck-dots { display: inline-flex; gap: 4px; align-items: center; min-width: 76px; }
# #     .ck-counts { margin-left: auto; display: inline-flex; gap: 5px; align-items: center; }
# #     .ck-n { font-family: var(--mono); font-size: 11px; color: #8a97a8; font-weight: 500; }
# #     .ck-fail-t { color: #dc2626; font-weight: 650; }
# #     .ck-nd-t { color: #a6b0bd; }

# #     .ck-list { list-style: none; padding: 2px 20px 14px 20px; margin: 0; }
# #     .ck-item { display: flex; align-items: center; gap: 10px; padding: 5px 0;
# #                font-size: 12.5px; color: #55637a; }
# #     .ck-text { flex: 1; }
# #     .ck-ref { font-family: var(--mono); font-size: 10.5px; font-weight: 650; color: #b45309;
# #               background: #fef3c7; border-radius: 4px; padding: 1px 7px; }
# #     .ck-total { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-top: 10px; padding-left: 2px; }

# #     .status-pass { color: #16a34a; font-weight: 700; }
# #     .status-fail { color: #dc2626; font-weight: 700; }
# #     .status-nd   { color: #94a3b8; font-weight: 500; }

# #     @media print {
# #       /* A collapsed <details> prints collapsed, which would silently drop
# #          30-odd verified checks from a printed or PDF'd report. Force them open. */
# #       .ck-cat > summary { cursor: default; }
# #       .ck-list { display: block !important; }
# #       .ck-cat { break-inside: avoid; }
# #     }
# #     .inc-ref-link {
# #       display: inline-block;
# #       font-size: 11px; font-weight: 700;
# #       background: #ffedd5; color: #ea580c;
# #       padding: 2px 8px; border-radius: var(--r);
# #     }

# #     .assessment-text { font-size: 14px; line-height: 1.8; color: #334155; font-weight: 500; }

# #     .rule-box {
# #       background: #fef2f2;
# #       border: 1px solid #fee2e2;
# #       border-radius: 8px;
# #       padding: 14px 18px;
# #       font-weight: 700; font-size: 14px; color: #991b1b;
# #       margin-bottom: 20px;
# #     }
# #     .action-list { display: flex; flex-direction: column; gap: 10px; }
# #     .action-item {
# #       display: flex; align-items: center; gap: 14px;
# #       padding: 12px 18px; border-radius: 8px;
# #     }
# #     .action-item.immediate  { background: #fff1f2; border: 1px solid #fecdd3; }
# #     .action-item.short-term { background: #fffbeb; border: 1px solid #fef3c7; }
# #     .action-item.follow-up  { background: #f0f9ff; border: 1px solid #bae6fd; }
    
# #     .action-priority {
# #       font-size: 10px; font-weight: 800; letter-spacing: 0; white-space: nowrap;
# #       padding: 3px 10px; border-radius: var(--r);
# #     }
# #     .action-item.immediate  .action-priority { background: #e11d48; color: #fff; }
# #     .action-item.short-term .action-priority { background: #d97706; color: #fff; }
# #     .action-item.follow-up  .action-priority { background: #0284c7; color: #fff; }
# #     .action-text { font-size: 13px; color: #1e293b; font-weight: 600; }

# #     .footer {
# #       text-align: center; font-size: 12px; color: #94a3b8;
# #       margin-top: 60px; padding-top: 24px; border-top: 1px solid #e2e8f0; font-weight: 500;
# #     }

# #     /* Sales Intelligence Styles */
# #     .si-grid {
# #       display: grid;
# #       grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
# #       gap: 24px;
# #     }
# #     .si-card {
# #       background: #ffffff;
# #       border-radius: var(--r);
# #       border: 1px solid #e2e8f0;
# #       padding: 24px;
# #       box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
# #     }
# #     .si-card-title {
# #       font-size: 13px; font-weight: 700; color: #0f172a;
# #       margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
# #       letter-spacing: 0;
# #       border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;
# #     }
# #     .si-item { margin-bottom: 14px; }
# #     .si-item:last-child { margin-bottom: 0; }
# #     .si-label { font-size: 11px; font-weight: 700; color: #64748b;  margin-bottom: 4px; display: block; }
# #     .si-value { font-size: 13px; color: #334155; line-height: 1.5; font-weight: 500; }
# #     .si-ts {
# #       font-size: 10px; font-weight: 700; color: #1e3a8a;
# #       background: #eff6ff; padding: 2px 6px; border-radius: 4px;
# #       margin-left: 6px; vertical-align: middle;
# #     }

# #     /* Overall Score & Pitch Coverage Dashboard Fixes */
# #     .overall-score-grid {
# #       display: flex; gap: 48px; align-items: center; flex-wrap: wrap;
# #     }
# #     @media (max-width: 768px) { .overall-score-grid { gap: 28px; } }

# #     .donut-wrapper { flex-shrink: 0; display: flex; justify-content: center; width: 140px; }
# #     .donut-chart {
# #       width: 130px; height: 130px; border-radius: 50%;
# #       display: flex; align-items: center; justify-content: center;
# #       box-shadow: inset 0 0 0 2px #f1f5f9;
# #     }
# #     .donut-inner {
# #       width: 104px; height: 104px; background: #fff; border-radius: 50%;
# #       display: flex; flex-direction: column; align-items: center; justify-content: center;
# #       box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
# #     }
# #     .donut-score { font-size: 36px; font-weight: 800; color: #0f172a; line-height: 1; letter-spacing: -1px; }
# #     .donut-max { font-size: 12px; color: #94a3b8; font-weight: 700; margin-top: 2px; }
    
# #     .score-breakdown { flex-grow: 1; min-width: 300px; display: flex; flex-direction: column; gap: 14px; }
# #     .breakdown-title { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0; margin-bottom: 2px; }
# #     .breakdown-row { display: flex; align-items: center; gap: 16px; }
# #     .breakdown-label { width: 160px; font-size: 13px; color: #475569; font-weight: 600; }
# #     .breakdown-bar-bg { flex-grow: 1; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
# #     .breakdown-bar-fill { height: 100%; border-radius: 4px; }
# #     .fill-compliance { background: #10b981; }
# #     .fill-pitch { background: #f59e0b; }
# #     .fill-sales { background: #3b82f6; }
# #     .breakdown-val { width: 60px; text-align: right; font-size: 13px; font-weight: 700; color: #0f172a; }
    
# #     .grade-badge {
# #       display: inline-block; padding: 6px 16px; border-radius: var(--r);
# #       font-size: 12px; font-weight: 700; color: #b45309; background: #fef3c7;
# #       margin-top: 12px; margin-bottom: 8px; letter-spacing: 0;
# #     }
# #     .deductions-text { font-size: 13px; color: #64748b; line-height: 1.6; font-weight: 500; margin-top: 4px; }

# #     .pitch-map-header { margin-bottom: 32px; background: #f8fafc; padding: 20px 24px; border-radius: var(--r); border: 1px solid #f1f5f9; }
# #     .pitch-map-title { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0; margin-bottom: 10px; }
# #     .pitch-overall-bar-bg { width: 100%; height: 12px; background: #e2e8f0; border-radius: 4px; overflow: hidden; margin-bottom: 8px; }
# #     .pitch-overall-bar-fill { height: 100%; background: #1e3a8a; border-radius: 4px; }
# #     .pitch-overall-stats { display: flex; justify-content: space-between; font-size: 12px; color: #475569; font-weight: 700; }
    
# #     .pitch-steps-container { position: relative; padding-left: 8px; }
# #     /* Modern vertical timeline guide line */
# #     .pitch-steps-container::before {
# #       content: ''; position: absolute; left: 23px; top: 16px; bottom: 16px;
# #       width: 2px; background: #e2e8f0; z-index: 1;
# #     }
    
# #     .pitch-step { display: flex; gap: 20px; margin-bottom: 24px; position: relative; z-index: 2; }
# #     .pitch-step:last-child { margin-bottom: 0; }
# #     .pitch-step-icon {
# #       width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
# #       display: flex; align-items: center; justify-content: center;
# #       font-size: 14px; font-weight: 700; color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
# #     }
# #     .icon-covered { background: #10b981; }
# #     .icon-partial { background: #f59e0b; }
# #     .icon-skipped { background: #ef4444; }
    
# #     .pitch-step-content { flex-grow: 1; background: #f8fafc; padding: 14px 20px; border-radius: 8px; border: 1px solid #f1f5f9; }
# #     .pitch-step-title-row { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; flex-wrap: wrap; }
# #     .pitch-step-name { font-size: 14px; font-weight: 700; color: #0f172a; }
# #     .pitch-step-badge { font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: var(--r); letter-spacing: 0; }
# #     .badge-covered { background: #dcfce7; color: #15803d; }
# #     .badge-partial { background: #fef3c7; color: #b45309; }
# #     .badge-skipped { background: #fee2e2; color: #b91c1c; }
# #     .pitch-step-ts { font-size: 11px; color: #2563eb; font-weight: 700; background: #eff6ff; padding: 2px 8px; border-radius: 4px; }
# #     .pitch-step-reason { font-size: 13px; color: #475569; line-height: 1.6; font-weight: 500; }
# # """


# # def fmt_null(value, fallback="—"):
# #     if value is None:
# #         return f'<span class="meta-value null-val">{fallback}</span>'
# #     return f'<span class="meta-value">{escape(str(value))}</span>'


# # def render_topbar(d):
# #     """Sticky identity bar: who this is about and whether it needs attention.

# #     No action buttons — this is a generated static file, and a Share button
# #     that cannot share is worse than no button.
# #     """
# #     flagged = d.get("call_flagged", False)
# #     sev = d.get("highest_severity", "None") or "None"
# #     call = escape(str(d.get("call_recording_file") or d.get("call_id") or ""))

# #     status = (f'<span class="chip chip-critical"><i class="chip-dot"></i>'
# #               f'{escape(sev)} Escalation</span>' if flagged else
# #               '<span class="chip chip-ok"><i class="chip-dot"></i>No Incidents</span>')
# #     dur = escape(str(d.get("call_duration") or ""))

# #     return f"""
# #   <div class="topbar">
# #     <div class="topbar-inner">
# #       <div class="brand">
# #         <span class="brand-mark">AQ</span>
# #         <span class="brand-name">Accredian QA</span>
# #         <span class="brand-sep">/</span>
# #         <span class="brand-sub">{call}</span>
# #       </div>
# #       <div class="topbar-status">
# #         {status}
# #         {f'<span class="chip chip-muted">{dur}</span>' if dur else ''}
# #       </div>
# #     </div>
# #   </div>"""


# # def render_record(d, report, dial="", ribbon="", verdict=""):
# #     """The audit record header: identity, verdict and composite score together.

# #     One card rather than a stack of sections, because a reader answers "who,
# #     how bad, why" in a single glance before deciding which tab to open.
# #     """
# #     rep = escape(d.get("sales_rep_name") or "Unknown rep")
# #     cust = escape(d.get("customer_name") or "Unknown customer")
# #     rep_id = escape(str(d.get("sales_rep_id") or ""))
# #     course = escape(d.get("course_name") or "")
# #     institute = escape(d.get("course_institute") or "")

# #     eyebrow_bits = [x for x in (institute, escape(str(report.get("analysis_date") or ""))) if x]
# #     eyebrow = " &nbsp;&middot;&nbsp; ".join(eyebrow_bits)

# #     verdict_html = f'<p class="verdict">{verdict}</p>' if verdict else ""

# #     return f"""
# #   <div class="record">
# #     <div class="record-body">
# #       <div>
# #         <div class="eyebrow">{eyebrow}</div>
# #         <h1>{course or "Call Quality Report"}</h1>
# #         <div class="parties">
# #           <span class="party-name">{rep}</span>
# #           {f'<span class="party-role">{rep_id}</span>' if rep_id else ''}
# #           <span class="party-arrow">&rarr;</span>
# #           <span class="party-name">{cust}</span>
# #         </div>
# #         {verdict_html}
# #       </div>
# #       {dial}
# #     </div>
# #     {ribbon}
# #   </div>"""


# # def render_statistics(d, stats):
# #     rep_ratio = stats.get("rep_talk_ratio_pct", 0)
# #     cust_ratio = round(100 - rep_ratio, 1)
# #     total_utterances = stats.get("sales_rep_utterances", 0) + stats.get("customer_utterances", 0)

# #     def fmt_num(n):
# #         return f"{n:,}" if isinstance(n, int) else str(n)

# #     return f"""
# #   <div class="section">
# #     <div class="section-title">Call Statistics</div>
# #     <div class="stats-grid">
# #       <div class="stat-card">
# #         <span class="stat-label">Duration</span>
# #         <span class="stat-value">{escape(d.get("call_duration", ""))}</span>
# #         <span class="stat-sub">{stats.get("duration_seconds", 0)} seconds</span>
# #       </div>
# #       <div class="stat-card">
# #         <span class="stat-label">Total Words</span>
# #         <span class="stat-value">{fmt_num(stats.get("total_words", 0))}</span>
# #         <span class="stat-sub">Rep: {fmt_num(stats.get("rep_words", 0))} &nbsp;/&nbsp; Cust: {fmt_num(stats.get("customer_words", 0))}</span>
# #         <div class="ratio-bar-wrap">
# #           <div class="ratio-bar">
# #             <div class="ratio-rep" style="width:{rep_ratio}%"></div>
# #             <div class="ratio-cust" style="width:{cust_ratio}%"></div>
# #           </div>
# #           <div class="ratio-legend">
# #             <span><span class="legend-dot" style="background:#1e3a8a"></span>Rep {rep_ratio}%</span>
# #             <span><span class="legend-dot" style="background:#38bdf8"></span>Cust {cust_ratio}%</span>
# #           </div>
# #         </div>
# #       </div>
# #       <div class="stat-card">
# #         <span class="stat-label">Utterances</span>
# #         <span class="stat-value">{total_utterances}</span>
# #         <span class="stat-sub">Rep: {stats.get("sales_rep_utterances", 0)} &nbsp;/&nbsp; Cust: {stats.get("customer_utterances", 0)}</span>
# #       </div>
# #       <div class="stat-card">
# #         <span class="stat-label">Transcript Tokens</span>
# #         <span class="stat-value">{fmt_num(stats.get("transcript_tokens", stats.get("est_transcript_tokens", 0)))}</span>
# #         <span class="stat-sub">chars &divide; 4 estimate</span>
# #       </div>
# #       <div class="stat-card">
# #         <span class="stat-label">Input Tokens</span>
# #         <span class="stat-value">{fmt_num(stats.get("input_tokens", stats.get("est_input_tokens", 0)))}</span>
# #         <span class="stat-sub">actual prompt tokens</span>
# #       </div>
# #       <div class="stat-card">
# #         <span class="stat-label">Output Tokens</span>
# #         <span class="stat-value">{fmt_num(stats.get("output_tokens", stats.get("est_output_tokens", 0)))}</span>
# #         <span class="stat-sub">actual completion tokens</span>
# #       </div>
# #       <div class="stat-card">
# #         <span class="stat-label">Total Tokens</span>
# #         <span class="stat-value">{fmt_num(stats.get("total_tokens", stats.get("est_total_tokens", 0)))}</span>
# #         <span class="stat-sub">input + output</span>
# #       </div>
# #     </div>
# #   </div>"""


# # ICO = {
# #     "check": '<path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" '
# #              'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>',
# #     "cross": '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" '
# #              'stroke-width="2.5" stroke-linecap="round"/>',
# #     "minus": '<path d="M5 12h14" fill="none" stroke="currentColor" '
# #              'stroke-width="2.5" stroke-linecap="round"/>',
# #     "up":    '<path d="m4 15 6-6 4 4 6-7" fill="none" stroke="currentColor" '
# #              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
# #     "down":  '<path d="m4 9 6 6 4-4 6 7" fill="none" stroke="currentColor" '
# #              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
# # }


# # def ico(name, cls="row-ico"):
# #     return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">'
# #             f'{ICO.get(name, "")}</svg>')


# # def render_incident_summary(summary):
# #     """Severity tally as a single header strip rather than four large pills."""
# #     if not summary:
# #         return ""
# #     l1, l2, l3 = summary.get("L1", 0), summary.get("L2", 0), summary.get("L3", 0)
# #     total = summary.get("total", l1 + l2 + l3)

# #     items = ""
# #     for n, label, cls in ((l3, "L3 Critical", "crit"), (l2, "L2 Major", "warn"),
# #                           (l1, "L1 Minor", "warn")):
# #         tone = cls if n else ""
# #         items += f'<span class="tally-item {tone}"><i></i>{n} {label}</span>'

# #     return f"""
# #   <div class="panel">
# #     <div class="panel-head">
# #       <div>
# #         <div class="panel-title">Compliance Incident Log</div>
# #         <div class="panel-sub">{total} flagged &middot; verbatim claims checked against course data</div>
# #       </div>
# #       <div class="tally">{items}</div>
# #     </div>
# #   </div>"""


# # def render_incidents(incidents):
# #     """Each finding as a panel: what was said beside what is true.

# #     Stacking the two made the reader hold the quote in their head while
# #     scrolling to the correction; side by side, the discrepancy is the layout.
# #     """
# #     if not incidents:
# #         return """
# #   <div class="panel">
# #     <div class="panel-body" style="color:var(--ink-500);font-size:13px">
# #       No incidents detected.
# #     </div>
# #   </div>"""

# #     out = ""
# #     for inc in incidents:
# #         sev = inc.get("severity", "L1")
# #         sev_label = SEV_LABELS.get(sev, sev)
# #         sev_cls = SEV_BADGE_CLASS.get(sev, "sev-L1")
# #         ts = escape(inc.get("timestamp", "") or "")
# #         basis = escape(inc.get("violation_basis", "") or "")
# #         said = escape(inc.get("what_rep_said", "") or "")
# #         quote = escape(inc.get("transcript_quote", "") or "")
# #         correct = escape(inc.get("what_is_correct", "") or "")
# #         category = escape(inc.get("category", "") or "")

# #         grounds = (f'<div class="grounds"><b>Violation grounds:</b> {basis}</div>'
# #                    if basis else "")
# #         pair = ""
# #         if said or quote or correct:
# #             pair = f"""
# #         <div class="evidence-pair">
# #           <div class="ev ev-said">
# #             <span class="ev-k">Rep stated</span>
# #             <span class="ev-v">{quote or said}</span>
# #           </div>
# #           <div class="ev ev-true">
# #             <span class="ev-k">Course data says</span>
# #             <span class="ev-v">{correct or "&mdash;"}</span>
# #           </div>
# #         </div>"""

# #         out += f"""
# #   <div class="panel incident-card {sev_cls}">
# #     <div class="panel-head">
# #       <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
# #         <span class="severity-badge {sev_cls}">{sev} &mdash; {sev_label}</span>
# #         <span class="panel-title">Incident #{inc.get("id")} &middot; {category}</span>
# #       </div>
# #       {f'<span class="panel-pill">{ts}</span>' if ts else ''}
# #     </div>
# #     <div class="panel-body">
# #       {grounds}
# #       {pair}
# #       <div class="incident-foot">
# #         <span>Category <b>{category.split("&mdash;")[0].strip() or "&mdash;"}</b></span>
# #         <span>Severity <b>{sev} &mdash; {sev_label}</b></span>
# #       </div>
# #     </div>
# #   </div>"""

# #     return f'<div class="section"><div class="section-title">Incidents</div>{out}</div>'


# # def render_checklist(checklist):
# #     """Coverage as a category grid.

# #     36 individual rows buried the sections below it; a card per category with
# #     its tally and a one-line summary of what actually failed keeps the whole
# #     audit on one screen. Failed categories carry a red edge so they are found
# #     without reading.
# #     """
# #     if not checklist:
# #         return ""

# #     cats = {}
# #     for item in checklist:
# #         cats.setdefault(item.get("category", "Other"), []).append(item)

# #     def state(it):
# #         st = str(it.get("status", "")).upper()
# #         return "pass" if st == "PASS" else ("fail" if st in ("FAIL", "VIOLATION", "INCORRECT") else "nd")

# #     tot = {"pass": 0, "fail": 0, "nd": 0}
# #     cards = ""
# #     for cat, items in cats.items():
# #         c = {"pass": 0, "fail": 0, "nd": 0}
# #         for it in items:
# #             c[state(it)] += 1
# #             tot[state(it)] += 1

# #         bits = []
# #         if c["fail"]:
# #             bits.append(f'{c["fail"]} failed')
# #         if c["pass"]:
# #             bits.append(f'{c["pass"]} passed')
# #         if c["nd"]:
# #             bits.append(f'{c["nd"]} n/d')
# #         cls = "fail" if c["fail"] else ("nd" if not c["pass"] else "")

# #         failed = [escape(it.get("check", "")) for it in items if state(it) == "fail"]
# #         nd = [escape(it.get("check", "")) for it in items if state(it) == "nd"]
# #         note = ""
# #         if failed:
# #             note += f'<span class="f">Failed:</span> {"; ".join(failed)}. '
# #         if nd:
# #             note += f'Not discussed: {"; ".join(nd)}.'
# #         if not note:
# #             note = "All checks in this category passed."

# #         cards += f"""
# #       <div class="cat {'fail' if c['fail'] else ''}">
# #         <div class="cat-top">
# #           <span class="cat-name">{escape(cat)}</span>
# #           <span class="cat-count {cls}">{' &middot; '.join(bits)}</span>
# #         </div>
# #         <span class="cat-note">{note}</span>
# #       </div>"""

# #     n = sum(tot.values())
# #     pct = f"{100 * tot['pass'] / n:.1f}%" if n else "—"
# #     return f"""
# #   <div class="section">
# #     <div class="panel">
# #       <div class="panel-head">
# #         <div>
# #           <div class="panel-title">Quality Assurance Checklist</div>
# #           <div class="panel-sub">{len(cats)} categories &middot; {n} checks &middot;
# #             {tot['pass']} passed &middot; {tot['fail']} failed &middot; {tot['nd']} not discussed</div>
# #         </div>
# #         <span class="panel-pill {'crit' if tot['fail'] else 'ok'}">Pass rate {pct}</span>
# #       </div>
# #       <div class="panel-body">
# #         <div class="cat-grid">{cards}</div>
# #       </div>
# #     </div>
# #   </div>"""


# # def render_assessment(text):
# #     return f"""
# #   <div class="section">
# #     <div class="section-title">Overall Assessment</div>
# #     <div class="card">
# #       <p class="assessment-text">{escape(text or "")}</p>
# #     </div>
# #   </div>"""


# # def render_recommended_action(rec_action):
# #     rule = rec_action.get("rule", "")
# #     actions = rec_action.get("actions", [])

# #     action_items = ""
# #     for act in actions:
# #         priority = act.get("priority", "Follow-up")
# #         cls = PRIORITY_CLASS.get(priority, "follow-up")
# #         action_items += f"""
# #         <div class="action-item {cls}">
# #           <span class="action-priority">{escape(priority)}</span>
# #           <span class="action-text">{escape(act.get("action", ""))}</span>
# #         </div>"""

# #     return f"""
# #   <div class="section">
# #     <div class="section-title">Recommended Action</div>
# #     <div class="card">
# #       <div class="rule-box">{escape(rule)}</div>
# #       <div class="action-list">{action_items}
# #       </div>
# #     </div>
# #   </div>"""


# # def render_sales_intelligence(si):
# #     if not si:
# #         return ""

# #     def get_val_ts(obj, key):
# #         item = obj.get(key, {})
# #         if isinstance(item, dict):
# #             val = item.get("value", "—")
# #             ts = item.get("timestamp")
# #         else:
# #             val = item or "—"
# #             ts = None
# #         ts_html = f'<span class="si-ts">{escape(ts)}</span>' if ts else ""
# #         return f"{escape(str(val))}{ts_html}"

# #     persona = si.get("customer_persona", {})
# #     psych = si.get("sales_psychology", {})
# #     lost = si.get("lost_opportunity", {})

# #     return f"""
# #   <div class="section">
# #     <div class="section-title">Sales Intelligence & Lost Opportunity Audit</div>
# #     <div class="si-grid">
# #       <div class="si-card">
# #         <div class="si-card-title">Customer Persona</div>
# #         <div class="si-item">
# #           <span class="si-label">Professional Context</span>
# #           <span class="si-value">{get_val_ts(persona, "professional_context")}</span>
# #         </div>
# #         <div class="si-item">
# #           <span class="si-label">Financial Baseline</span>
# #           <span class="si-value">{get_val_ts(persona, "financial_baseline")}</span>
# #         </div>
# #         <div class="si-item">
# #           <span class="si-label">Core Motivation</span>
# #           <span class="si-value">{get_val_ts(persona, "core_motivation")}</span>
# #         </div>
# #       </div>

# #       <div class="si-card">
# #         <div class="si-card-title">Sales Psychology</div>
# #         <div class="si-item">
# #           <span class="si-label">Consultative vs. Product-Push</span>
# #           <span class="si-value">{get_val_ts(psych, "consultative_vs_product_push")}</span>
# #         </div>
# #         <div class="si-item">
# #           <span class="si-label">Hype Authenticity</span>
# #           <span class="si-value">{get_val_ts(psych, "hype_authenticity")}</span>
# #         </div>
# #         <div class="si-item">
# #           <span class="si-label">Tone/Energy</span>
# #           <span class="si-value">{get_val_ts(psych, "tone_energy")}</span>
# #         </div>
# #       </div>

# #       <div class="si-card">
# #         <div class="si-card-title">Lost Opportunity Analysis</div>
# #         <div class="si-item">
# #           <span class="si-label">Objection Handling</span>
# #           <span class="si-value">{get_val_ts(lost, "objection_handling")}</span>
# #         </div>
# #         <div class="si-item">
# #           <span class="si-label">The "Drop" Reason</span>
# #           <span class="si-value">{get_val_ts(lost, "drop_reason")}</span>
# #         </div>
# #       </div>
# #     </div>
# #   </div>"""


# # def render_overall_call_score(overall_call_score: dict) -> str:
# #     if not overall_call_score:
# #         return ""

# #     total = overall_call_score.get("total_score", 0)
# #     c_score = overall_call_score.get("compliance_score", 0)
# #     p_score = overall_call_score.get("pitch_coverage_score", 0)
# #     s_score = overall_call_score.get("sales_quality_score", 0)
# #     grade = overall_call_score.get("grade", "")
# #     deductions = overall_call_score.get("deductions_text", "")

# #     # Calculate percentages for the bars
# #     c_pct = min(100, (c_score / 35) * 100) if c_score else 0
# #     p_pct = min(100, (p_score / 30) * 100) if p_score else 0
# #     s_pct = min(100, (s_score / 35) * 100) if s_score else 0

# #     return f"""
# #   <div class="section">
# #     <div class="section-title">Overall Call Score</div>
# #     <div class="card">
# #       <div class="overall-score-grid">
# #         <div class="donut-wrapper">
# #           <div class="donut-chart" style="background: conic-gradient(#f59e0b 0% {total}%, #f1f5f9 {total}% 100%);">
# #             <div class="donut-inner">
# #               <span class="donut-score">{total}</span>
# #               <span class="donut-max">/100</span>
# #             </div>
# #           </div>
# #         </div>
# #         <div class="score-breakdown">
# #           <div class="breakdown-title">Score Breakdown</div>
          
# #           <div class="breakdown-row">
# #             <span class="breakdown-label">Compliance (&times;35)</span>
# #             <div class="breakdown-bar-bg">
# #               <div class="breakdown-bar-fill fill-compliance" style="width: {c_pct}%;"></div>
# #             </div>
# #             <span class="breakdown-val">{c_score} / 35</span>
# #           </div>

# #           <div class="breakdown-row">
# #             <span class="breakdown-label">Pitch Coverage (&times;30)</span>
# #             <div class="breakdown-bar-bg">
# #               <div class="breakdown-bar-fill fill-pitch" style="width: {p_pct}%;"></div>
# #             </div>
# #             <span class="breakdown-val">{p_score} / 30</span>
# #           </div>

# #           <div class="breakdown-row">
# #             <span class="breakdown-label">Sales Quality (&times;35)</span>
# #             <div class="breakdown-bar-bg">
# #               <div class="breakdown-bar-fill fill-sales" style="width: {s_pct}%;"></div>
# #             </div>
# #             <span class="breakdown-val">{s_score} / 35</span>
# #           </div>
          
# #           <div style="margin-top: 4px;">
# #             <span class="grade-badge">{escape(grade)}</span>
# #             <div class="deductions-text">{escape(deductions)}</div>
# #           </div>
# #         </div>
# #       </div>
# #     </div>
# #   </div>"""


# # def render_sales_pitch_coverage(pitch_coverage: dict) -> str:
# #     if not pitch_coverage:
# #         return ""

# #     overall_pct = pitch_coverage.get("overall_coverage_pct", 0)
# #     steps_covered = pitch_coverage.get("steps_covered", 0)
# #     total_steps = pitch_coverage.get("total_steps", 0)
# #     steps = pitch_coverage.get("steps", [])

# #     step_html = ""
# #     for s in steps:
# #         status = s.get("status", "SKIPPED").upper()
# #         if status == "COVERED":
# #             icon = "&#10003;"
# #             icon_cls = "icon-covered"
# #             badge_cls = "badge-covered"
# #         elif status == "PARTIAL":
# #             icon = "~"
# #             icon_cls = "icon-partial"
# #             badge_cls = "badge-partial"
# #         else:
# #             icon = "&#10007;"
# #             icon_cls = "icon-skipped"
# #             badge_cls = "badge-skipped"

# #         ts = s.get("timestamp_range")
# #         ts_html = f'<span class="pitch-step-ts">{escape(ts)}</span>' if ts else ""

# #         step_html += f"""
# #         <div class="pitch-step">
# #           <div class="pitch-step-icon {icon_cls}">{icon}</div>
# #           <div class="pitch-step-content">
# #             <div class="pitch-step-title-row">
# #               <span class="pitch-step-name">{escape(s.get("step_title", ""))}</span>
# #               <span class="pitch-step-badge {badge_cls}">{status}</span>
# #               {ts_html}
# #             </div>
# #             <div class="pitch-step-reason">{escape(s.get("reasoning", ""))}</div>
# #           </div>
# #         </div>"""

# #     return f"""
# #   <div class="section">
# #     <div class="section-title">Sales Pitch Coverage Map</div>
# #     <div class="card">
# #       <div class="pitch-map-header">
# #         <div class="pitch-map-title">Overall Pitch Coverage Score</div>
# #         <div class="pitch-overall-bar-bg">
# #           <div class="pitch-overall-bar-fill" style="width: {overall_pct}%;"></div>
# #         </div>
# #         <div class="pitch-overall-stats">
# #           <span>0%</span>
# #           <span>{overall_pct}% ({steps_covered} / {total_steps} steps)</span>
# #           <span>100%</span>
# #         </div>
# #       </div>
# #       <div class="pitch-steps-container">
# #         {step_html}
# #       </div>
# #     </div>
# #   </div>"""


# # def generate_html(data: dict) -> str:
# #     report = data.get("report", {})
# #     stats = report.get("call_statistics", {})
# #     rep_name = data.get("sales_rep_name", "Rep")
# #     customer = data.get("customer_name", "Customer")
# #     title = f"Call Quality Report &mdash; {escape(rep_name)} / {escape(customer)}"
# #     rubric = report.get("rubric_assessment")
# #     has_rubric = bool(rubric and rubric.get("_methodology"))

# #     if has_rubric:
# #         rubric["_call_id"] = data.get("call_id")
# #         rubric["_stt"] = os.path.basename(data["call_stt_file"]) if data.get("call_stt_file") else None

# #     # ---- Tab 1: compliance findings ----
# #     incidents = report.get("incidents") or []
# #     incident_html = "\n".join(filter(None, [
# #         render_incident_summary(report.get("incident_summary", {})),
# #         render_incidents(incidents),
# #         render_checklist(report.get("checklist", [])),
# #         render_assessment(report.get("overall_assessment", "")),
# #         render_recommended_action(report["recommended_action"])
# #         if report.get("recommended_action") else "",
# #     ]))

# #     # ---- Tab 2: rubric ----
# #     rubric_html = ""
# #     if has_rubric:
# #         rubric_html = (render_call_snapshot(rubric, stats)
# #                        + render_methodology_section(rubric, CHAPTERS))

# #     # ---- Tab 3: sales intelligence ----
# #     intel_html = render_sales_intelligence(report.get("sales_intelligence"))

# #     panels, badges = [], {}
# #     panels.append(("incident", "Incidents & Compliance", incident_html))
# #     checklist = report.get("checklist") or []
# #     passed = sum(1 for c in checklist if str(c.get("status", "")).upper() == "PASS")
# #     badges["incident"] = (f"{len(incidents)} flagged · {passed}/{len(checklist)} pass"
# #                           if checklist else f"{len(incidents)} flagged")

# #     if rubric_html:
# #         panels.append(("rubric", "Rubric Scorecard & Methodology", rubric_html))
# #         badges["rubric"] = (f"{rubric['methodology_score']:.0f} / "
# #                             f"{rubric['methodology_max']:.0f} pts")
# #     if intel_html:
# #         panels.append(("intel", "Sales Intelligence", intel_html))

# #     dial = render_score_banner(rubric) if has_rubric else ""
# #     ribbon = render_ribbon(rubric, stats) if has_rubric else ""
# #     verdict = render_verdict(rubric) if has_rubric else ""

# #     body = "\n".join([
# #         render_record(data, report, dial=dial, ribbon=ribbon, verdict=verdict),
# #         render_tabs(panels, badges=badges),
# #         '  <div class="footer">Generated by Call Quality Agent '
# #         '&nbsp;&middot;&nbsp; Accredian</div>',
# #     ])

# #     return f"""<!DOCTYPE html>
# # <html lang="en">
# # <head>
# #   <meta charset="UTF-8" />
# #   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
# #   <title>{title}</title>
# #   <style>{CSS}
# # {tabs_css()}
# # {methodology_css()}
# #   </style>
# # </head>
# # <body>
# # {render_topbar(data)}
# # <div class="page">
# # {body}
# # </div>
# # </body>
# # </html>
# # """

# """Generate a self-contained HTML report from a call-quality report JSON file.

# Usage:
#     python src/report_html.py output/0.report.json
#     # writes output/0.report.html
# """

# import json
# import os
# import sys
# from html import escape as html_escape
# from src.report_methodology import (methodology_css, render_methodology_section,
#                                     render_score_banner, render_call_snapshot,
#                                     render_ribbon, render_verdict,
#                                     render_diagnostics)
# from src.report_tabs import tabs_css, render_tabs

# CHAPTERS = {
#     "customer_profiling": "Ch 5", "need_identification": "Ch 6",
#     "vision_setting": "Ch 7",     "program_mapping": "Ch 8",
#     "fee_and_urgency": "Ch 9",    "objection_handling": "Ch 10",
#     "trust_journey": "Framework 4",
# }

# def escape(s):
#     if s is None:
#         return ""
#     return html_escape(str(s))


# SEV_LABELS = {"L1": "Minor", "L2": "Major", "L3": "Critical", "None": "Clean"}
# SEV_BADGE_CLASS = {"L1": "sev-L1", "L2": "sev-L2", "L3": "sev-L3", "None": "sev-None"}
# PRIORITY_CLASS = {"Immediate": "immediate", "Short-term": "short-term", "Follow-up": "follow-up"}

# CSS = """
#     /* =====================================================================
#        Accredian Call Quality — design system

#        Audit-record language: mono for anything a machine measured, sans for
#        anything a person wrote. Tabular numerals throughout. Colour is reserved
#        for status; the accent marks interaction only.

#        No webfonts and no CDN: these reports are emailed and opened from disk,
#        so a network dependency means a broken document offline. The stacks
#        below resolve to Inter-class and SF-Mono-class faces natively on macOS,
#        Windows and most Linux desktops.
#        ===================================================================== */
#     *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

#     :root {
#       --ink-950:#090d16; --ink-900:#0f172a; --ink-800:#1e293b; --ink-700:#334155;
#       --ink-600:#475569; --ink-500:#64748b; --ink-400:#94a3b8; --ink-300:#cbd5e1;
#       --ink-200:#e2e8f0; --ink-100:#f1f5f9; --ink-50:#f8fafc;

#       --accent:#2563eb; --accent-hover:#1d4ed8; --accent-subtle:#eff6ff;
#       --critical:#dc2626; --critical-bg:#fef2f2; --critical-border:#fee2e2; --critical-deep:#991b1b;
#       --warning:#d97706; --warning-bg:#fffbeb; --warning-border:#fef3c7; --warning-deep:#92400e;
#       --success:#059669; --success-bg:#ecfdf5; --success-border:#d1fae5; --success-deep:#065f46;

#       --sans: -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI",
#               Inter, Roboto, "Helvetica Neue", Arial, sans-serif;
#       --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
#               "Liberation Mono", "Courier New", monospace;

#       --r: 12px;
#       --shadow-subtle: 0 1px 2px 0 rgba(15,23,42,.04), 0 1px 3px 0 rgba(15,23,42,.02);
#       --shadow-card: 0 0 0 1px rgba(15,23,42,.06), 0 1px 2px 0 rgba(15,23,42,.03);
#     }

#     body {
#       font-family: var(--sans);
#       font-size: 14px; line-height: 1.6;
#       color: var(--ink-900); background: var(--ink-50);
#       font-variant-numeric: tabular-nums;
#       -webkit-font-smoothing: antialiased;
#       -moz-osx-font-smoothing: grayscale;
#     }
#     .tabular, .mono { font-variant-numeric: tabular-nums; }
#     .mono { font-family: var(--mono); }

#     .page { max-width: 1180px; margin: 0 auto; padding: 0 24px 88px; }

#     /* ---- Sticky identity bar ---- */
#     .topbar {
#       position: sticky; top: 0; z-index: 50;
#       background: var(--ink-950); color: #fff;
#       border-bottom: 1px solid var(--ink-800);
#       margin-bottom: 28px;
#     }
#     .topbar-inner {
#       max-width: 1180px; margin: 0 auto; padding: 0 24px;
#       height: 56px; display: flex; align-items: center;
#       justify-content: space-between; gap: 16px;
#     }
#     .brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
#     .brand-mark {
#       width: 28px; height: 28px; border-radius: 6px; flex: none;
#       background: #fff; color: var(--ink-950);
#       display: flex; align-items: center; justify-content: center;
#       font-family: var(--mono); font-weight: 700; font-size: 11px; letter-spacing: -0.5px;
#     }
#     .brand-name {
#       font-family: var(--mono); font-size: 11.5px; font-weight: 600;
#       text-transform: uppercase; letter-spacing: .04em; color: #fff;
#     }
#     .brand-sep { color: var(--ink-600); font-size: 12px; }
#     .brand-sub {
#       font-family: var(--mono); font-size: 11px; color: var(--ink-400);
#       white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
#     }
#     .topbar-status { display: flex; align-items: center; gap: 8px; flex: none; }
#     .chip {
#       display: inline-flex; align-items: center; gap: 6px;
#       padding: 3px 10px; border-radius: 5px;
#       font-family: var(--mono); font-size: 10.5px; font-weight: 500;
#       white-space: nowrap;
#     }
#     .chip-dot { width: 6px; height: 6px; border-radius: 50%; flex: none; }
#     .chip-critical { background: rgba(220,38,38,.18); color: #fca5a5;
#                      border: 1px solid rgba(220,38,38,.35); }
#     .chip-critical .chip-dot { background: #f87171; }
#     .chip-ok { background: rgba(5,150,105,.18); color: #6ee7b7;
#                border: 1px solid rgba(5,150,105,.35); }
#     .chip-ok .chip-dot { background: #34d399; }
#     .chip-muted { background: rgba(255,255,255,.07); color: var(--ink-300);
#                   border: 1px solid rgba(255,255,255,.13); }

#     /* ---- Hero record card ---- */
#     .record {
#       background: #fff; border: 1px solid var(--ink-200);
#       border-radius: var(--r); box-shadow: var(--shadow-subtle);
#       overflow: hidden; margin-bottom: 22px;
#     }
#     .record-body {
#       display: grid; grid-template-columns: minmax(0,1fr) 300px;
#       gap: 32px; padding: 28px 30px;
#     }
#     .eyebrow {
#       font-family: var(--mono); font-size: 11px; color: var(--ink-500);
#       letter-spacing: .02em; margin-bottom: 12px;
#     }
#     .eyebrow b { color: var(--ink-700); font-weight: 600; }
#     .record h1 {
#       font-size: 27px; font-weight: 700; letter-spacing: -0.6px;
#       color: var(--ink-950); line-height: 1.18;
#     }
#     .parties {
#       display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
#       margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--ink-100);
#     }
#     .party-name { font-size: 14.5px; font-weight: 650; color: var(--ink-900); }
#     .party-role { font-size: 12px; color: var(--ink-500); font-family: var(--mono); }
#     .party-arrow { color: var(--ink-300); font-size: 15px; }
#     .verdict {
#       margin-top: 16px; font-size: 14px; line-height: 1.68; color: var(--ink-700);
#     }
#     .verdict strong { color: var(--ink-950); font-weight: 600; }

#     /* ---- Composite score dial ---- */
#     .dial {
#       background: var(--ink-50); border: 1px solid var(--ink-200);
#       border-radius: var(--r); padding: 22px 20px;
#       display: flex; flex-direction: column; align-items: center; gap: 14px;
#     }
#     .dial-label {
#       font-family: var(--mono); font-size: 10.5px; font-weight: 600;
#       text-transform: uppercase; letter-spacing: .06em; color: var(--ink-500);
#     }
#     .dial-ring { position: relative; width: 116px; height: 116px; }
#     .dial-ring svg { transform: rotate(-90deg); width: 116px; height: 116px; }
#     .dial-centre {
#       position: absolute; inset: 0;
#       display: flex; flex-direction: column; align-items: center; justify-content: center;
#     }
#     .dial-num { font-size: 32px; font-weight: 700; color: var(--ink-950);
#                 letter-spacing: -1px; line-height: 1; }
#     .dial-max { font-family: var(--mono); font-size: 9.5px; color: var(--ink-400);
#                 text-transform: uppercase; margin-top: 3px; letter-spacing: .04em; }
#     .dial-grade {
#       display: inline-flex; align-items: center; gap: 7px;
#       padding: 5px 12px; border-radius: 6px;
#       font-family: var(--mono); font-size: 11.5px; font-weight: 600;
#     }
#     .dial-split {
#       width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
#       padding-top: 13px; border-top: 1px solid var(--ink-200);
#       font-family: var(--mono); font-size: 10px;
#     }
#     .dial-split-k { display: block; color: var(--ink-500); margin-bottom: 2px; }
#     .dial-split-v { font-size: 12.5px; font-weight: 700; color: var(--ink-900); }
#     .dial-split-r { color: var(--ink-400); }

#     /* ---- Telemetry ribbon ---- */
#     .ribbon {
#       background: var(--ink-100); border-top: 1px solid var(--ink-200);
#       padding: 14px 30px;
#       display: grid; grid-template-columns: repeat(6, 1fr); gap: 0;
#       font-family: var(--mono);
#     }
#     .ribbon-cell { padding: 0 16px; border-left: 1px solid var(--ink-200); min-width: 0; }
#     .ribbon-cell:first-child { border-left: none; padding-left: 0; }
#     .ribbon-k {
#       display: block; font-size: 9.5px; color: var(--ink-500); font-weight: 500;
#       text-transform: uppercase; letter-spacing: .05em; margin-bottom: 3px;
#     }
#     .ribbon-v {
#       display: block; font-size: 13.5px; font-weight: 700; color: var(--ink-900);
#       line-height: 1.25; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
#     }
#     .ribbon-v small { font-size: 10.5px; font-weight: 400; color: var(--ink-600); }
#     .ribbon-s { display: block; font-size: 9.5px; color: var(--ink-500); margin-top: 2px; }
#     .v-crit { color: var(--critical) !important; }
#     .v-warn { color: var(--warning-deep) !important; }
#     .v-ok   { color: var(--success-deep) !important; }

#     .refbar {
#       background: var(--ink-50); border-top: 1px solid var(--ink-200);
#       padding: 10px 30px; font-family: var(--mono); font-size: 10.5px;
#       color: var(--ink-500); display: flex; flex-wrap: wrap; gap: 6px 20px;
#     }
#     .refbar b { color: var(--ink-700); font-weight: 600; }

#     /* ---- Sections ---- */
#     .section { margin-bottom: 26px; }
#     .section-title {
#       font-family: var(--mono); font-size: 11.5px; font-weight: 700;
#       text-transform: uppercase; letter-spacing: .07em; color: var(--ink-950);
#       padding-bottom: 10px; margin-bottom: 14px;
#       border-bottom: 1px solid var(--ink-200);
#       display: flex; align-items: center; justify-content: space-between; gap: 12px;
#     }
#     .section-title .count {
#       font-size: 10.5px; font-weight: 500; color: var(--ink-500);
#       text-transform: none; letter-spacing: 0;
#     }

#     .card {
#       background: #fff; border: 1px solid var(--ink-200);
#       border-radius: var(--r); box-shadow: var(--shadow-subtle);
#       padding: 22px 24px;
#     }

#     /* ---- Stat grid ---- */
#     .stats-grid {
#       display: grid; grid-template-columns: repeat(4, 1fr); gap: 0;
#       background: #fff; border: 1px solid var(--ink-200);
#       border-radius: var(--r); box-shadow: var(--shadow-subtle); overflow: hidden;
#     }
#     .stat-card {
#       padding: 15px 18px; display: flex; flex-direction: column; gap: 4px;
#       border-right: 1px solid var(--ink-100); border-bottom: 1px solid var(--ink-100);
#       min-height: 86px;
#     }
#     .stat-card:nth-child(4n) { border-right: none; }
#     .stat-card:nth-last-child(-n+4) { border-bottom: none; }
#     .stat-label {
#       font-family: var(--mono); font-size: 9.5px; font-weight: 500; color: var(--ink-500);
#       text-transform: uppercase; letter-spacing: .05em;
#     }
#     .stat-value { font-size: 19px; font-weight: 700; color: var(--ink-950);
#                   letter-spacing: -0.4px; line-height: 1.22; }
#     .stat-sub { font-size: 11px; color: var(--ink-500); font-family: var(--mono); }

#     @media (max-width: 1060px) {
#       .record-body { grid-template-columns: minmax(0,1fr); }
#       .ribbon { grid-template-columns: repeat(3, 1fr); gap: 14px 0; }
#       .ribbon-cell:nth-child(3n+1) { border-left: none; padding-left: 0; }
#     }
#     @media (max-width: 720px) {
#       .page { padding: 0 14px 64px; }
#       .topbar-inner { padding: 0 14px; height: auto; min-height: 52px;
#                       flex-wrap: wrap; gap: 8px; padding-top: 9px; padding-bottom: 9px; }
#       .brand-sub { display: none; }
#       .record-body { padding: 22px 18px; gap: 22px; }
#       .record h1 { font-size: 21px; }
#       .ribbon { grid-template-columns: repeat(2, 1fr); padding: 14px 18px; }
#       .ribbon-cell:nth-child(3n+1) { border-left: 1px solid var(--ink-200); padding-left: 16px; }
#       .ribbon-cell:nth-child(2n+1) { border-left: none; padding-left: 0; }
#       .refbar { padding: 10px 18px; }
#       .stats-grid { grid-template-columns: repeat(2, 1fr); }
#       .stat-card:nth-child(4n) { border-right: 1px solid var(--ink-100); }
#       .stat-card:nth-child(2n) { border-right: none; }
#       .stat-card:nth-last-child(-n+4) { border-bottom: 1px solid var(--ink-100); }
#       .stat-card:nth-last-child(-n+2) { border-bottom: none; }
#     }



#     /* ---- Panel: the repeating container for every content block ----
#        White card, header strip carrying a title, an optional data sub-line and
#        a mono status pill on the right, then the body. Every section uses it, so
#        a reader learns the shape once and can then scan straight to the pill. */
#     .panel {
#       background: #fff; border: 1px solid var(--ink-200); border-radius: var(--r);
#       box-shadow: var(--shadow-subtle); overflow: hidden; margin-bottom: 16px;
#     }
#     .panel-head {
#       display: flex; align-items: flex-start; justify-content: space-between;
#       gap: 14px; flex-wrap: wrap;
#       padding: 16px 20px; border-bottom: 1px solid var(--ink-100);
#     }
#     .panel-title { font-size: 13.5px; font-weight: 700; color: var(--ink-950); }
#     .panel-sub { font-size: 11.5px; color: var(--ink-500); margin-top: 3px; font-family: var(--mono); }
#     .panel-pill {
#       font-family: var(--mono); font-size: 11px; font-weight: 600;
#       padding: 5px 11px; border-radius: 6px; white-space: nowrap;
#       background: var(--ink-100); color: var(--ink-700); border: 1px solid var(--ink-200);
#     }
#     .panel-pill.ok   { background: var(--success-bg); color: var(--success-deep); border-color: var(--success-border); }
#     .panel-pill.warn { background: var(--warning-bg); color: var(--warning-deep); border-color: var(--warning-border); }
#     .panel-pill.crit { background: var(--critical-bg); color: var(--critical-deep); border-color: var(--critical-border); }
#     .panel-pill.accent { background: var(--accent-subtle); color: #1e40af; border-color: #bfdbfe; }
#     .panel-body { padding: 18px 20px; }

#     .avatar {
#       width: 42px; height: 42px; border-radius: 8px; flex: none;
#       background: var(--ink-900); color: #fff;
#       display: flex; align-items: center; justify-content: center;
#       font-family: var(--mono); font-weight: 700; font-size: 14px; letter-spacing: -0.5px;
#     }
#     .split-legend {
#       display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
#       font-family: var(--mono); font-size: 11.5px; color: var(--ink-500); margin-bottom: 8px;
#     }
#     .split-legend b { color: var(--ink-900); font-weight: 650; }
#     .split-bar {
#       display: flex; height: 12px; border-radius: 6px; overflow: hidden;
#       background: var(--ink-100);
#     }
#     .split-bar i { display: block; height: 100%; }

#     .tally { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; }
#     .tally-item {
#       display: inline-flex; align-items: center; gap: 6px;
#       font-family: var(--mono); font-size: 11px; font-weight: 500;
#       padding: 4px 10px; border-radius: 5px;
#       background: var(--ink-100); color: var(--ink-600); border: 1px solid var(--ink-200);
#     }
#     .tally-item i { width: 6px; height: 6px; border-radius: 50%; flex: none; }
#     .tally-item.crit { background: var(--critical-bg); color: var(--critical-deep); border-color: var(--critical-border); }
#     .tally-item.crit i { background: var(--critical); }
#     .tally-item.warn { background: var(--warning-bg); color: var(--warning-deep); border-color: var(--warning-border); }
#     .tally-item.warn i { background: var(--warning); }
#     .tally-item.ok { background: var(--success-bg); color: var(--success-deep); border-color: var(--success-border); }
#     .tally-item.ok i { background: var(--success); }

#     /* Paired evidence: what was said beside what is true. Reading them
#        side by side is the whole point of the finding. */
#     .evidence-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
#     .ev {
#       padding: 13px 15px; border-radius: 9px; display: flex;
#       flex-direction: column; gap: 6px;
#     }
#     .ev-said { background: var(--ink-50); border: 1px solid var(--ink-200); }
#     .ev-true { background: var(--success-bg); border: 1px solid var(--success-border); }
#     .ev-k {
#       font-family: var(--mono); font-size: 9.5px; font-weight: 700;
#       text-transform: uppercase; letter-spacing: .06em;
#     }
#     .ev-said .ev-k { color: var(--critical-deep); }
#     .ev-true .ev-k { color: var(--success-deep); }
#     .ev-v { font-size: 12.5px; line-height: 1.6; color: var(--ink-900); }
#     .ev-said .ev-v {
#       font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
#       font-style: italic;
#     }
#     .grounds { font-size: 12.5px; line-height: 1.65; color: var(--ink-700); margin-bottom: 14px; }
#     .grounds b { color: var(--ink-950); font-weight: 650; }
#     .incident-foot {
#       display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
#       margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--ink-100);
#       font-family: var(--mono); font-size: 10.5px; color: var(--ink-500);
#     }
#     .incident-foot b { color: var(--ink-900); font-weight: 600; }

#     /* ---- Category grid: checklist, trust stages, why/hfte rows ---- */
#     .cat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
#     .cat {
#       padding: 13px 15px; border-radius: 9px;
#       border: 1px solid var(--ink-200); background: #fff;
#       display: flex; flex-direction: column; gap: 6px;
#     }
#     .cat.fail { border-color: var(--critical-border); background: #fffafa; }
#     .cat-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
#     .cat-name { font-size: 12.5px; font-weight: 700; color: var(--ink-950); }
#     .cat.fail .cat-name { color: var(--critical-deep); }
#     .cat-count {
#       font-family: var(--mono); font-size: 9.5px; font-weight: 500;
#       padding: 2px 8px; border-radius: 4px; white-space: nowrap;
#       background: var(--success-bg); color: var(--success-deep); border: 1px solid var(--success-border);
#     }
#     .cat-count.fail { background: var(--critical-bg); color: var(--critical-deep); border-color: var(--critical-border); }
#     .cat-count.nd { background: var(--ink-100); color: var(--ink-600); border-color: var(--ink-200); }
#     .cat-note { font-size: 11.5px; line-height: 1.55; color: var(--ink-600); }
#     .cat-note .f { color: var(--critical); font-weight: 650; }

#     .stage-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
#     .stage {
#       padding: 12px 13px; border-radius: 9px;
#       border: 1px solid var(--ink-200); background: var(--ink-50);
#       display: flex; flex-direction: column; gap: 6px;
#     }
#     .stage.done { background: var(--success-bg); border-color: var(--success-border); }
#     .stage.stall { background: var(--warning-bg); border-color: var(--warning-border); }
#     .stage-top {
#       display: flex; align-items: center; justify-content: space-between; gap: 6px;
#       font-family: var(--mono); font-size: 9.5px; font-weight: 700;
#       letter-spacing: .04em; color: var(--ink-500);
#     }
#     .stage.done .stage-top { color: var(--success-deep); }
#     .stage.stall .stage-top { color: var(--warning-deep); }
#     .stage-note { font-size: 11px; line-height: 1.5; color: var(--ink-700); }

#     .row-list { display: flex; flex-direction: column; gap: 9px; }
#     .row-item {
#       display: flex; align-items: flex-start; gap: 10px;
#       padding: 11px 13px; border-radius: 9px;
#       border: 1px solid var(--ink-200); background: var(--ink-50);
#     }
#     .row-item.ok   { background: var(--success-bg); border-color: var(--success-border); }
#     .row-item.warn { background: var(--warning-bg); border-color: var(--warning-border); }
#     .row-item.bad  { background: var(--critical-bg); border-color: var(--critical-border); }
#     .row-ico { width: 16px; height: 16px; flex: none; margin-top: 1px; }
#     .row-k { font-size: 12.5px; font-weight: 700; color: var(--ink-950); }
#     .row-tag { font-family: var(--mono); font-size: 10px; font-weight: 600; margin-left: 5px; }
#     .row-item.ok .row-tag { color: var(--success-deep); }
#     .row-item.warn .row-tag { color: var(--warning-deep); }
#     .row-item.bad .row-tag { color: var(--critical-deep); }
#     .row-note { font-size: 11.5px; line-height: 1.55; color: var(--ink-600); margin-top: 3px; }

#     .duo { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

#     @media (max-width: 1000px) {
#       .cat-grid { grid-template-columns: repeat(2, 1fr); }
#       .stage-grid { grid-template-columns: repeat(3, 1fr); }
#     }
#     @media (max-width: 760px) {
#       .evidence-pair, .duo { grid-template-columns: 1fr; }
#       .cat-grid, .stage-grid { grid-template-columns: 1fr; }
#     }

#     /* ---- Incident summary pills ---- */
#     .summary-pills { display: flex; flex-wrap: wrap; gap: 10px; }
#     .pill {
#       flex: 1 1 130px; display: flex; flex-direction: column; gap: 3px;
#       padding: 13px 16px; border-radius: 9px; border: 1px solid var(--ink-200);
#       background: #fff;
#     }
#     .pill-count { font-size: 24px; font-weight: 700; line-height: 1.1; letter-spacing: -0.6px; }
#     .pill-label {
#       font-family: var(--mono); font-size: 10px; font-weight: 500;
#       text-transform: uppercase; letter-spacing: .05em; color: var(--ink-500);
#     }
#     .pill.l1 { background: var(--warning-bg); border-color: var(--warning-border); }
#     .pill.l1 .pill-count { color: var(--warning-deep); }
#     .pill.l2 { background: #fff7ed; border-color: #fed7aa; }
#     .pill.l2 .pill-count { color: #c2410c; }
#     .pill.l3 { background: var(--critical-bg); border-color: var(--critical-border); }
#     .pill.l3 .pill-count { color: var(--critical-deep); }
#     .pill.total { background: var(--ink-950); border-color: var(--ink-950); }
#     .pill.total .pill-count { color: #fff; }
#     .pill.total .pill-label { color: var(--ink-400); }

#     /* ---- Incident cards ---- */
#     .incident-card {
#       border: 1px solid var(--ink-200); border-radius: var(--r);
#       background: #fff; box-shadow: var(--shadow-subtle);
#       margin-bottom: 14px; overflow: hidden;
#     }
#     .incident-header {
#       display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
#       padding: 13px 18px; background: var(--ink-50);
#       border-bottom: 1px solid var(--ink-200);
#     }
#     .incident-id {
#       font-family: var(--mono); font-size: 10.5px; font-weight: 700;
#       padding: 3px 9px; border-radius: 5px;
#       background: var(--ink-950); color: #fff;
#     }
#     .incident-category { font-size: 13px; font-weight: 650; color: var(--ink-950); flex: 1; }
#     .incident-ts {
#       font-family: var(--mono); font-size: 11px; color: var(--ink-500);
#       background: var(--ink-100); padding: 2px 8px; border-radius: 4px;
#     }
#     .incident-grid { padding: 16px 18px; display: flex; flex-direction: column; gap: 13px; }
#     .incident-field { display: flex; flex-direction: column; gap: 4px; }
#     .field-label {
#       font-family: var(--mono); font-size: 9.5px; font-weight: 600;
#       text-transform: uppercase; letter-spacing: .06em; color: var(--ink-500);
#     }
#     .field-value { font-size: 13px; color: var(--ink-700); line-height: 1.62; }
#     .transcript-quote {
#       border-left: 3px solid var(--critical); background: var(--critical-bg);
#       padding: 9px 14px; border-radius: 0 6px 6px 0;
#       font-size: 12.5px; color: var(--critical-deep); font-style: italic;
#     }
#     .violation-basis { font-size: 12.5px; color: var(--ink-600); padding: 0 18px 16px; }
#     .transcript-quote:empty, .violation-basis:empty, .field-value:empty { display: none; }
#     .incident-card .transcript-quote { margin: 0 18px 12px; }
#     .correct {
#       border-left: 3px solid var(--success); background: var(--success-bg);
#       padding: 9px 14px; border-radius: 0 6px 6px 0;
#       font-size: 12.5px; color: var(--success-deep);
#     }

#     .severity-badge {
#       display: inline-flex; align-items: center; gap: 5px;
#       font-family: var(--mono); font-size: 10px; font-weight: 600;
#       padding: 3px 9px; border-radius: 5px;
#       background: var(--ink-100); color: var(--ink-600); border: 1px solid var(--ink-200);
#     }
#     .severity-badge.sev-L1 { background: var(--warning-bg); color: var(--warning-deep);
#                              border-color: var(--warning-border); }
#     .severity-badge.sev-L2 { background: #fff7ed; color: #c2410c; border-color: #fed7aa; }
#     .severity-badge.sev-L3 { background: var(--critical-bg); color: var(--critical-deep);
#                              border-color: var(--critical-border); }

#     /* Severity colours the card's edge, never its field. A tinted body makes
#        the rep's quote hard to read and shouts louder than the finding. */
#     .incident-card.sev-L1 { border-left: 3px solid var(--warning); }
#     .incident-card.sev-L2 { border-left: 3px solid #ea580c; }
#     .incident-card.sev-L3 { border-left: 3px solid var(--critical); }

#     .snapshot { margin-bottom: 24px; }
#     .footer {
#       font-family: var(--mono); font-size: 10.5px; color: var(--ink-400);
#       text-align: center; padding-top: 26px; margin-top: 10px;
#       border-top: 1px solid var(--ink-200);
#     }

#     /* ---- QA checklist: coverage, not a 47-row table ---- */
#     .ck-legend { display: inline-flex; align-items: center; gap: 6px;
#                  font-family: var(--mono); font-size: 10.5px; font-weight: 500; color: var(--muted);
#                  text-transform: none; letter-spacing: 0; }
#     .ck-legend .ck-dot { margin-left: 6px; }

#     .ck-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%;
#               flex: none; }
#     .ck-pass { background: #34d399; }
#     .ck-fail { background: #f87171; }
#     .ck-nd   { background: #d7dde6; }

#     .ck-cat { border-bottom: 1px solid var(--rule-soft); }
#     .ck-cat:last-child { border-bottom: none; }
#     .ck-cat > summary {
#       display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
#       padding: 13px 20px; cursor: pointer; list-style: none;
#       transition: background .12s ease;
#     }
#     .ck-cat > summary::-webkit-details-marker { display: none; }
#     .ck-cat > summary:hover { background: #fafbfc; }
#     .ck-cat > summary:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
#     .ck-cat-name { font-size: 12.5px; font-weight: 650; color: var(--strong); min-width: 176px; }
#     .ck-dots { display: inline-flex; gap: 4px; align-items: center; min-width: 76px; }
#     .ck-counts { margin-left: auto; display: inline-flex; gap: 5px; align-items: center; }
#     .ck-n { font-family: var(--mono); font-size: 11px; color: #8a97a8; font-weight: 500; }
#     .ck-fail-t { color: #dc2626; font-weight: 650; }
#     .ck-nd-t { color: #a6b0bd; }

#     .ck-list { list-style: none; padding: 2px 20px 14px 20px; margin: 0; }
#     .ck-item { display: flex; align-items: center; gap: 10px; padding: 5px 0;
#                font-size: 12.5px; color: #55637a; }
#     .ck-text { flex: 1; }
#     .ck-ref { font-family: var(--mono); font-size: 10.5px; font-weight: 650; color: #b45309;
#               background: #fef3c7; border-radius: 4px; padding: 1px 7px; }
#     .ck-total { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-top: 10px; padding-left: 2px; }

#     .status-pass { color: #16a34a; font-weight: 700; }
#     .status-fail { color: #dc2626; font-weight: 700; }
#     .status-nd   { color: #94a3b8; font-weight: 500; }

#     @media print {
#       /* A collapsed <details> prints collapsed, which would silently drop
#          30-odd verified checks from a printed or PDF'd report. Force them open. */
#       .ck-cat > summary { cursor: default; }
#       .ck-list { display: block !important; }
#       .ck-cat { break-inside: avoid; }
#     }
#     .inc-ref-link {
#       display: inline-block;
#       font-size: 11px; font-weight: 700;
#       background: #ffedd5; color: #ea580c;
#       padding: 2px 8px; border-radius: var(--r);
#     }

#     .assessment-text { font-size: 14px; line-height: 1.8; color: #334155; font-weight: 500; }

#     .rule-box {
#       background: #fef2f2;
#       border: 1px solid #fee2e2;
#       border-radius: 8px;
#       padding: 14px 18px;
#       font-weight: 700; font-size: 14px; color: #991b1b;
#       margin-bottom: 20px;
#     }
#     .action-list { display: flex; flex-direction: column; gap: 10px; }
#     .action-item {
#       display: flex; align-items: center; gap: 14px;
#       padding: 12px 18px; border-radius: 8px;
#     }
#     .action-item.immediate  { background: #fff1f2; border: 1px solid #fecdd3; }
#     .action-item.short-term { background: #fffbeb; border: 1px solid #fef3c7; }
#     .action-item.follow-up  { background: #f0f9ff; border: 1px solid #bae6fd; }
    
#     .action-priority {
#       font-size: 10px; font-weight: 800; letter-spacing: 0; white-space: nowrap;
#       padding: 3px 10px; border-radius: var(--r);
#     }
#     .action-item.immediate  .action-priority { background: #e11d48; color: #fff; }
#     .action-item.short-term .action-priority { background: #d97706; color: #fff; }
#     .action-item.follow-up  .action-priority { background: #0284c7; color: #fff; }
#     .action-text { font-size: 13px; color: #1e293b; font-weight: 600; }

#     .footer {
#       text-align: center; font-size: 12px; color: #94a3b8;
#       margin-top: 60px; padding-top: 24px; border-top: 1px solid #e2e8f0; font-weight: 500;
#     }

#     /* Sales Intelligence Styles */
#     .si-grid {
#       display: grid;
#       grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
#       gap: 24px;
#     }
#     .si-card {
#       background: #ffffff;
#       border-radius: var(--r);
#       border: 1px solid #e2e8f0;
#       padding: 24px;
#       box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
#     }
#     .si-card-title {
#       font-size: 13px; font-weight: 700; color: #0f172a;
#       margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
#       letter-spacing: 0;
#       border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;
#     }
#     .si-item { margin-bottom: 14px; }
#     .si-item:last-child { margin-bottom: 0; }
#     .si-label { font-size: 11px; font-weight: 700; color: #64748b;  margin-bottom: 4px; display: block; }
#     .si-value { font-size: 13px; color: #334155; line-height: 1.5; font-weight: 500; }
#     .si-ts {
#       font-size: 10px; font-weight: 700; color: #1e3a8a;
#       background: #eff6ff; padding: 2px 6px; border-radius: 4px;
#       margin-left: 6px; vertical-align: middle;
#     }

#     /* Overall Score & Pitch Coverage Dashboard Fixes */
#     .overall-score-grid {
#       display: flex; gap: 48px; align-items: center; flex-wrap: wrap;
#     }
#     @media (max-width: 768px) { .overall-score-grid { gap: 28px; } }

#     .donut-wrapper { flex-shrink: 0; display: flex; justify-content: center; width: 140px; }
#     .donut-chart {
#       width: 130px; height: 130px; border-radius: 50%;
#       display: flex; align-items: center; justify-content: center;
#       box-shadow: inset 0 0 0 2px #f1f5f9;
#     }
#     .donut-inner {
#       width: 104px; height: 104px; background: #fff; border-radius: 50%;
#       display: flex; flex-direction: column; align-items: center; justify-content: center;
#       box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
#     }
#     .donut-score { font-size: 36px; font-weight: 800; color: #0f172a; line-height: 1; letter-spacing: -1px; }
#     .donut-max { font-size: 12px; color: #94a3b8; font-weight: 700; margin-top: 2px; }
    
#     .score-breakdown { flex-grow: 1; min-width: 300px; display: flex; flex-direction: column; gap: 14px; }
#     .breakdown-title { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0; margin-bottom: 2px; }
#     .breakdown-row { display: flex; align-items: center; gap: 16px; }
#     .breakdown-label { width: 160px; font-size: 13px; color: #475569; font-weight: 600; }
#     .breakdown-bar-bg { flex-grow: 1; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
#     .breakdown-bar-fill { height: 100%; border-radius: 4px; }
#     .fill-compliance { background: #10b981; }
#     .fill-pitch { background: #f59e0b; }
#     .fill-sales { background: #3b82f6; }
#     .breakdown-val { width: 60px; text-align: right; font-size: 13px; font-weight: 700; color: #0f172a; }
    
#     .grade-badge {
#       display: inline-block; padding: 6px 16px; border-radius: var(--r);
#       font-size: 12px; font-weight: 700; color: #b45309; background: #fef3c7;
#       margin-top: 12px; margin-bottom: 8px; letter-spacing: 0;
#     }
#     .deductions-text { font-size: 13px; color: #64748b; line-height: 1.6; font-weight: 500; margin-top: 4px; }

#     .pitch-map-header { margin-bottom: 32px; background: #f8fafc; padding: 20px 24px; border-radius: var(--r); border: 1px solid #f1f5f9; }
#     .pitch-map-title { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0; margin-bottom: 10px; }
#     .pitch-overall-bar-bg { width: 100%; height: 12px; background: #e2e8f0; border-radius: 4px; overflow: hidden; margin-bottom: 8px; }
#     .pitch-overall-bar-fill { height: 100%; background: #1e3a8a; border-radius: 4px; }
#     .pitch-overall-stats { display: flex; justify-content: space-between; font-size: 12px; color: #475569; font-weight: 700; }
    
#     .pitch-steps-container { position: relative; padding-left: 8px; }
#     /* Modern vertical timeline guide line */
#     .pitch-steps-container::before {
#       content: ''; position: absolute; left: 23px; top: 16px; bottom: 16px;
#       width: 2px; background: #e2e8f0; z-index: 1;
#     }
    
#     .pitch-step { display: flex; gap: 20px; margin-bottom: 24px; position: relative; z-index: 2; }
#     .pitch-step:last-child { margin-bottom: 0; }
#     .pitch-step-icon {
#       width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
#       display: flex; align-items: center; justify-content: center;
#       font-size: 14px; font-weight: 700; color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#     }
#     .icon-covered { background: #10b981; }
#     .icon-partial { background: #f59e0b; }
#     .icon-skipped { background: #ef4444; }
    
#     .pitch-step-content { flex-grow: 1; background: #f8fafc; padding: 14px 20px; border-radius: 8px; border: 1px solid #f1f5f9; }
#     .pitch-step-title-row { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; flex-wrap: wrap; }
#     .pitch-step-name { font-size: 14px; font-weight: 700; color: #0f172a; }
#     .pitch-step-badge { font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: var(--r); letter-spacing: 0; }
#     .badge-covered { background: #dcfce7; color: #15803d; }
#     .badge-partial { background: #fef3c7; color: #b45309; }
#     .badge-skipped { background: #fee2e2; color: #b91c1c; }
#     .pitch-step-ts { font-size: 11px; color: #2563eb; font-weight: 700; background: #eff6ff; padding: 2px 8px; border-radius: 4px; }
#     .pitch-step-reason { font-size: 13px; color: #475569; line-height: 1.6; font-weight: 500; }
# """


# def fmt_null(value, fallback="—"):
#     if value is None:
#         return f'<span class="meta-value null-val">{fallback}</span>'
#     return f'<span class="meta-value">{escape(str(value))}</span>'


# def render_topbar(d):
#     """Sticky identity bar: who this is about and whether it needs attention.

#     No action buttons — this is a generated static file, and a Share button
#     that cannot share is worse than no button.
#     """
#     flagged = d.get("call_flagged", False)
#     sev = d.get("highest_severity", "None") or "None"
#     call = escape(str(d.get("call_recording_file") or d.get("call_id") or ""))

#     status = (f'<span class="chip chip-critical"><i class="chip-dot"></i>'
#               f'{escape(sev)} Escalation</span>' if flagged else
#               '<span class="chip chip-ok"><i class="chip-dot"></i>No Incidents</span>')
#     dur = escape(str(d.get("call_duration") or ""))

#     return f"""
#   <div class="topbar">
#     <div class="topbar-inner">
#       <div class="brand">
#         <span class="brand-mark">AQ</span>
#         <span class="brand-name">Accredian QA</span>
#         <span class="brand-sep">/</span>
#         <span class="brand-sub">{call}</span>
#       </div>
#       <div class="topbar-status">
#         {status}
#         {f'<span class="chip chip-muted">{dur}</span>' if dur else ''}
#       </div>
#     </div>
#   </div>"""


# def render_record(d, report, dial="", ribbon="", verdict=""):
#     """The audit record header: identity, verdict and composite score together.

#     One card rather than a stack of sections, because a reader answers "who,
#     how bad, why" in a single glance before deciding which tab to open.
#     """
#     rep = escape(d.get("sales_rep_name") or "Unknown rep")
#     cust = escape(d.get("customer_name") or "Unknown customer")
#     rep_id = escape(str(d.get("sales_rep_id") or ""))
#     course = escape(d.get("course_name") or "")
#     institute = escape(d.get("course_institute") or "")

#     eyebrow_bits = [x for x in (institute, escape(str(report.get("analysis_date") or ""))) if x]
#     eyebrow = " &nbsp;&middot;&nbsp; ".join(eyebrow_bits)

#     verdict_html = f'<p class="verdict">{verdict}</p>' if verdict else ""

#     return f"""
#   <div class="record">
#     <div class="record-body">
#       <div>
#         <div class="eyebrow">{eyebrow}</div>
#         <h1>{course or "Call Quality Report"}</h1>
#         <div class="parties">
#           <span class="party-name">{rep}</span>
#           {f'<span class="party-role">{rep_id}</span>' if rep_id else ''}
#           <span class="party-arrow">&rarr;</span>
#           <span class="party-name">{cust}</span>
#         </div>
#         {verdict_html}
#       </div>
#       {dial}
#     </div>
#     {ribbon}
#   </div>"""


# def render_statistics(d, stats):
#     rep_ratio = stats.get("rep_talk_ratio_pct", 0)
#     cust_ratio = round(100 - rep_ratio, 1)
#     total_utterances = stats.get("sales_rep_utterances", 0) + stats.get("customer_utterances", 0)

#     def fmt_num(n):
#         return f"{n:,}" if isinstance(n, int) else str(n)

#     return f"""
#   <div class="section">
#     <div class="section-title">Call Statistics</div>
#     <div class="stats-grid">
#       <div class="stat-card">
#         <span class="stat-label">Duration</span>
#         <span class="stat-value">{escape(d.get("call_duration", ""))}</span>
#         <span class="stat-sub">{stats.get("duration_seconds", 0)} seconds</span>
#       </div>
#       <div class="stat-card">
#         <span class="stat-label">Total Words</span>
#         <span class="stat-value">{fmt_num(stats.get("total_words", 0))}</span>
#         <span class="stat-sub">Rep: {fmt_num(stats.get("rep_words", 0))} &nbsp;/&nbsp; Cust: {fmt_num(stats.get("customer_words", 0))}</span>
#         <div class="ratio-bar-wrap">
#           <div class="ratio-bar">
#             <div class="ratio-rep" style="width:{rep_ratio}%"></div>
#             <div class="ratio-cust" style="width:{cust_ratio}%"></div>
#           </div>
#           <div class="ratio-legend">
#             <span><span class="legend-dot" style="background:#1e3a8a"></span>Rep {rep_ratio}%</span>
#             <span><span class="legend-dot" style="background:#38bdf8"></span>Cust {cust_ratio}%</span>
#           </div>
#         </div>
#       </div>
#       <div class="stat-card">
#         <span class="stat-label">Utterances</span>
#         <span class="stat-value">{total_utterances}</span>
#         <span class="stat-sub">Rep: {stats.get("sales_rep_utterances", 0)} &nbsp;/&nbsp; Cust: {stats.get("customer_utterances", 0)}</span>
#       </div>
#       <div class="stat-card">
#         <span class="stat-label">Transcript Tokens</span>
#         <span class="stat-value">{fmt_num(stats.get("transcript_tokens", stats.get("est_transcript_tokens", 0)))}</span>
#         <span class="stat-sub">chars &divide; 4 estimate</span>
#       </div>
#       <div class="stat-card">
#         <span class="stat-label">Input Tokens</span>
#         <span class="stat-value">{fmt_num(stats.get("input_tokens", stats.get("est_input_tokens", 0)))}</span>
#         <span class="stat-sub">actual prompt tokens</span>
#       </div>
#       <div class="stat-card">
#         <span class="stat-label">Output Tokens</span>
#         <span class="stat-value">{fmt_num(stats.get("output_tokens", stats.get("est_output_tokens", 0)))}</span>
#         <span class="stat-sub">actual completion tokens</span>
#       </div>
#       <div class="stat-card">
#         <span class="stat-label">Total Tokens</span>
#         <span class="stat-value">{fmt_num(stats.get("total_tokens", stats.get("est_total_tokens", 0)))}</span>
#         <span class="stat-sub">input + output</span>
#       </div>
#     </div>
#   </div>"""


# ICO = {
#     "check": '<path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" '
#              'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>',
#     "cross": '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" '
#              'stroke-width="2.5" stroke-linecap="round"/>',
#     "minus": '<path d="M5 12h14" fill="none" stroke="currentColor" '
#              'stroke-width="2.5" stroke-linecap="round"/>',
#     "up":    '<path d="m4 15 6-6 4 4 6-7" fill="none" stroke="currentColor" '
#              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
#     "down":  '<path d="m4 9 6 6 4-4 6 7" fill="none" stroke="currentColor" '
#              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
# }


# def ico(name, cls="row-ico"):
#     return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">'
#             f'{ICO.get(name, "")}</svg>')


# def render_incident_summary(summary):
#     """Severity tally as a single header strip rather than four large pills."""
#     if not summary:
#         return ""
#     l1, l2, l3 = summary.get("L1", 0), summary.get("L2", 0), summary.get("L3", 0)
#     total = summary.get("total", l1 + l2 + l3)

#     items = ""
#     for n, label, cls in ((l3, "L3 Critical", "crit"), (l2, "L2 Major", "warn"),
#                           (l1, "L1 Minor", "warn")):
#         tone = cls if n else ""
#         items += f'<span class="tally-item {tone}"><i></i>{n} {label}</span>'

#     return f"""
#   <div class="panel">
#     <div class="panel-head">
#       <div>
#         <div class="panel-title">Compliance Incident Log</div>
#         <div class="panel-sub">{total} flagged &middot; verbatim claims checked against course data</div>
#       </div>
#       <div class="tally">{items}</div>
#     </div>
#   </div>"""


# def render_incidents(incidents):
#     """Each finding as a panel: what was said beside what is true.

#     Stacking the two made the reader hold the quote in their head while
#     scrolling to the correction; side by side, the discrepancy is the layout.
#     """
#     if not incidents:
#         return """
#   <div class="panel">
#     <div class="panel-body" style="color:var(--ink-500);font-size:13px">
#       No incidents detected.
#     </div>
#   </div>"""

#     out = ""
#     for inc in incidents:
#         sev = inc.get("severity", "L1")
#         sev_label = SEV_LABELS.get(sev, sev)
#         sev_cls = SEV_BADGE_CLASS.get(sev, "sev-L1")
#         ts = escape(inc.get("timestamp", "") or "")
#         basis = escape(inc.get("violation_basis", "") or "")
#         said = escape(inc.get("what_rep_said", "") or "")
#         quote = escape(inc.get("transcript_quote", "") or "")
#         correct = escape(inc.get("what_is_correct", "") or "")
#         category = escape(inc.get("category", "") or "")

#         grounds = (f'<div class="grounds"><b>Violation grounds:</b> {basis}</div>'
#                    if basis else "")
#         pair = ""
#         if said or quote or correct:
#             pair = f"""
#         <div class="evidence-pair">
#           <div class="ev ev-said">
#             <span class="ev-k">Rep stated</span>
#             <span class="ev-v">{quote or said}</span>
#           </div>
#           <div class="ev ev-true">
#             <span class="ev-k">Course data says</span>
#             <span class="ev-v">{correct or "&mdash;"}</span>
#           </div>
#         </div>"""

#         out += f"""
#   <div class="panel incident-card {sev_cls}">
#     <div class="panel-head">
#       <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
#         <span class="severity-badge {sev_cls}">{sev} &mdash; {sev_label}</span>
#         <span class="panel-title">Incident #{inc.get("id")} &middot; {category}</span>
#       </div>
#       {f'<span class="panel-pill">{ts}</span>' if ts else ''}
#     </div>
#     <div class="panel-body">
#       {grounds}
#       {pair}
#       <div class="incident-foot">
#         <span>Category <b>{category.split("&mdash;")[0].strip() or "&mdash;"}</b></span>
#         <span>Severity <b>{sev} &mdash; {sev_label}</b></span>
#       </div>
#     </div>
#   </div>"""

#     return f'<div class="section"><div class="section-title">Incidents</div>{out}</div>'


# def render_checklist(checklist):
#     """Coverage as a category grid.

#     36 individual rows buried the sections below it; a card per category with
#     its tally and a one-line summary of what actually failed keeps the whole
#     audit on one screen. Failed categories carry a red edge so they are found
#     without reading.
#     """
#     if not checklist:
#         return ""

#     cats = {}
#     for item in checklist:
#         cats.setdefault(item.get("category", "Other"), []).append(item)

#     def state(it):
#         st = str(it.get("status", "")).upper()
#         return "pass" if st == "PASS" else ("fail" if st in ("FAIL", "VIOLATION", "INCORRECT") else "nd")

#     tot = {"pass": 0, "fail": 0, "nd": 0}
#     cards = ""
#     for cat, items in cats.items():
#         c = {"pass": 0, "fail": 0, "nd": 0}
#         for it in items:
#             c[state(it)] += 1
#             tot[state(it)] += 1

#         bits = []
#         if c["fail"]:
#             bits.append(f'{c["fail"]} failed')
#         if c["pass"]:
#             bits.append(f'{c["pass"]} passed')
#         if c["nd"]:
#             bits.append(f'{c["nd"]} n/d')
#         cls = "fail" if c["fail"] else ("nd" if not c["pass"] else "")

#         failed = [escape(it.get("check", "")) for it in items if state(it) == "fail"]
#         nd = [escape(it.get("check", "")) for it in items if state(it) == "nd"]
#         note = ""
#         if failed:
#             note += f'<span class="f">Failed:</span> {"; ".join(failed)}. '
#         if nd:
#             note += f'Not discussed: {"; ".join(nd)}.'
#         if not note:
#             note = "All checks in this category passed."

#         cards += f"""
#       <div class="cat {'fail' if c['fail'] else ''}">
#         <div class="cat-top">
#           <span class="cat-name">{escape(cat)}</span>
#           <span class="cat-count {cls}">{' &middot; '.join(bits)}</span>
#         </div>
#         <span class="cat-note">{note}</span>
#       </div>"""

#     n = sum(tot.values())
#     pct = f"{100 * tot['pass'] / n:.1f}%" if n else "—"
#     return f"""
#   <div class="section">
#     <div class="panel">
#       <div class="panel-head">
#         <div>
#           <div class="panel-title">Quality Assurance Checklist</div>
#           <div class="panel-sub">{len(cats)} categories &middot; {n} checks &middot;
#             {tot['pass']} passed &middot; {tot['fail']} failed &middot; {tot['nd']} not discussed</div>
#         </div>
#         <span class="panel-pill {'crit' if tot['fail'] else 'ok'}">Pass rate {pct}</span>
#       </div>
#       <div class="panel-body">
#         <div class="cat-grid">{cards}</div>
#       </div>
#     </div>
#   </div>"""


# def render_assessment(text):
#     return f"""
#   <div class="section">
#     <div class="section-title">Overall Assessment</div>
#     <div class="card">
#       <p class="assessment-text">{escape(text or "")}</p>
#     </div>
#   </div>"""


# def render_recommended_action(rec_action):
#     rule = rec_action.get("rule", "")
#     actions = rec_action.get("actions", [])

#     action_items = ""
#     for act in actions:
#         priority = act.get("priority", "Follow-up")
#         cls = PRIORITY_CLASS.get(priority, "follow-up")
#         action_items += f"""
#         <div class="action-item {cls}">
#           <span class="action-priority">{escape(priority)}</span>
#           <span class="action-text">{escape(act.get("action", ""))}</span>
#         </div>"""

#     return f"""
#   <div class="section">
#     <div class="section-title">Recommended Action</div>
#     <div class="card">
#       <div class="rule-box">{escape(rule)}</div>
#       <div class="action-list">{action_items}
#       </div>
#     </div>
#   </div>"""


# def render_persona(d, si):
#     """Who the customer is, from the LLM's read of the call."""
#     persona = (si or {}).get("customer_persona", {}) or {}
#     name = d.get("customer_name") or "Customer"
#     initials = "".join(w[0] for w in str(name).split()[:2]).upper() or "?"

#     def val(obj, key):
#         it = obj.get(key)
#         if isinstance(it, dict):
#             return escape(str(it.get("value") or "—"))
#         return escape(str(it or "—"))

#     boxes = ""
#     for label, key in (("Professional context", "professional_context"),
#                        ("Financial baseline", "financial_baseline"),
#                        ("Core motivation", "core_motivation")):
#         boxes += f"""
#         <div class="ev ev-said" style="font-family:var(--sans)">
#           <span class="ev-k" style="color:var(--ink-500)">{label}</span>
#           <span class="ev-v" style="font-style:normal;font-family:var(--sans)">{val(persona, key)}</span>
#         </div>"""

#     course = escape(d.get("course_name") or "")
#     return f"""
#   <div class="panel">
#     <div class="panel-head">
#       <div style="display:flex;align-items:center;gap:12px">
#         <span class="avatar">{escape(initials)}</span>
#         <div>
#           <div class="panel-title">{escape(name)}</div>
#           <div class="panel-sub">{escape(d.get("customer_name") and course or "")}</div>
#         </div>
#       </div>
#       <span class="panel-pill">Prospect</span>
#     </div>
#     <div class="panel-body">
#       <div class="cat-grid" style="grid-template-columns:repeat(3,1fr)">{boxes}</div>
#     </div>
#   </div>"""


# def render_dynamics(stats, metrics):
#     """Conversational telemetry: the split bar plus four measured behaviours."""
#     if not stats and not metrics:
#         return ""
#     m = metrics or {}
#     ratio = stats.get("rep_talk_ratio_pct")
#     if ratio is None:
#         ratio = m.get("rep_talk_ratio_pct") or 0
#     over = ratio > 60

#     def box(k, v, sub, tone=""):
#         return f"""
#         <div class="cat">
#           <span class="stat-label">{k}</span>
#           <span class="stat-value {tone}" style="font-size:16px">{v}</span>
#           <span class="cat-note">{sub}</span>
#         </div>"""

#     boxes = ""
#     wpm = None
#     if stats.get("duration_seconds") and stats.get("rep_words"):
#         wpm = stats["rep_words"] / (stats["duration_seconds"] / 60)
#         boxes += box("Rep pace", f"{wpm:.0f} wpm", "measured conversational rate")

#     a, b = m.get("customer_words_first_half"), m.get("customer_words_second_half")
#     if a and b:
#         trend = "drop-off across the call" if b < a else "opened up across the call"
#         boxes += box("Customer response", f"{a:.0f} &rarr; {b:.0f} wds", trend,
#                      "v-crit" if b < a else "v-ok")

#     q = m.get("rep_question_count")
#     if q is not None:
#         openpct = (m.get("open_question_ratio") or 0) * 100
#         boxes += box("Question mix", f"{q} queries",
#                      f"{openpct:.0f}% open &middot; {100 - openpct:.0f}% closed")

#     lm = m.get("longest_rep_monologue_sec")
#     if lm is not None:
#         mins, secs = int(lm // 60), int(lm % 60)
#         boxes += box("Monologue ceiling", f"{mins}m {secs:02d}s",
#                      "3:00 is the penalty threshold",
#                      "v-crit" if lm > 180 else "v-ok")

#     return f"""
#   <div class="panel">
#     <div class="panel-head">
#       <div>
#         <div class="panel-title">Conversational Dynamics</div>
#         <div class="panel-sub">
#           {"Rep talk time exceeds the 60% benchmark" if over else "Talk ratio within benchmark"}
#         </div>
#       </div>
#       <span class="panel-pill {'crit' if over else 'ok'}">{ratio:.1f}% rep</span>
#     </div>
#     <div class="panel-body">
#       <div class="split-legend">
#         <span><b>Rep</b> {ratio:.1f}% &middot; {stats.get('rep_words', 0):,} words</span>
#         <span><b>Customer</b> {100 - ratio:.1f}% &middot; {stats.get('customer_words', 0):,} words</span>
#       </div>
#       <div class="split-bar">
#         <i style="width:{ratio:.1f}%;background:var(--ink-900)"></i>
#         <i style="width:{100 - ratio:.1f}%;background:var(--success)"></i>
#       </div>
#       <div class="cat-grid" style="grid-template-columns:repeat(4,1fr);margin-top:16px">{boxes}</div>
#     </div>
#   </div>"""


# def render_psychology(si):
#     """Sales psychology and lost-opportunity read, paired."""
#     if not si:
#         return ""
#     psych = si.get("sales_psychology", {}) or {}
#     lost = si.get("lost_opportunity", {}) or {}

#     def val(obj, key):
#         it = obj.get(key)
#         if isinstance(it, dict):
#             return escape(str(it.get("value") or "—")), escape(str(it.get("timestamp") or ""))
#         return escape(str(it or "—")), ""

#     def rows(obj, fields):
#         out = ""
#         for label, key in fields:
#             v, ts = val(obj, key)
#             out += f"""
#         <div class="row-item">
#           <div>
#             <span class="row-k">{label}</span>
#             {f'<span class="row-tag">{ts}</span>' if ts else ''}
#             <div class="row-note">{v}</div>
#           </div>
#         </div>"""
#         return out

#     return f"""
#   <div class="duo">
#     <div class="panel">
#       <div class="panel-head"><div class="panel-title">Sales Psychology</div></div>
#       <div class="panel-body"><div class="row-list">{rows(psych, (
#           ("Consultative vs product-push", "consultative_vs_product_push"),
#           ("Hype authenticity", "hype_authenticity"),
#           ("Tone &amp; energy", "tone_energy")))}</div></div>
#     </div>
#     <div class="panel">
#       <div class="panel-head"><div class="panel-title">Lost Opportunity</div></div>
#       <div class="panel-body"><div class="row-list">{rows(lost, (
#           ("Objection handling", "objection_handling"),
#           ("The &ldquo;drop&rdquo; reason", "drop_reason")))}</div></div>
#     </div>
#   </div>"""


# def render_telemetry(stats):
#     """Model and system token expenditure."""
#     if not stats:
#         return ""
#     fields = [("Total tokens", "total_tokens", "full context payload"),
#               ("Input tokens", "input_tokens", "prompt payload"),
#               ("Output tokens", "output_tokens", "structured response"),
#               ("Transcript tokens", "transcript_tokens",
#                f"{stats.get('total_words', 0):,} verbatim words")]
#     boxes = ""
#     for label, key, sub in fields:
#         v = stats.get(key)
#         if not v:
#             continue
#         boxes += f"""
#         <div class="cat">
#           <span class="stat-label">{label}</span>
#           <span class="stat-value" style="font-size:17px">{v:,}</span>
#           <span class="cat-note">{sub}</span>
#         </div>"""
#     if not boxes:
#         return ""
#     return f"""
#   <div class="panel">
#     <div class="panel-head">
#       <div class="panel-title">Model &amp; System Telemetry</div>
#       <span class="panel-pill">Token expenditure</span>
#     </div>
#     <div class="panel-body">
#       <div class="cat-grid" style="grid-template-columns:repeat(4,1fr)">{boxes}</div>
#     </div>
#   </div>"""


# def render_overall_call_score(overall_call_score: dict) -> str:
#     if not overall_call_score:
#         return ""

#     total = overall_call_score.get("total_score", 0)
#     c_score = overall_call_score.get("compliance_score", 0)
#     p_score = overall_call_score.get("pitch_coverage_score", 0)
#     s_score = overall_call_score.get("sales_quality_score", 0)
#     grade = overall_call_score.get("grade", "")
#     deductions = overall_call_score.get("deductions_text", "")

#     # Calculate percentages for the bars
#     c_pct = min(100, (c_score / 35) * 100) if c_score else 0
#     p_pct = min(100, (p_score / 30) * 100) if p_score else 0
#     s_pct = min(100, (s_score / 35) * 100) if s_score else 0

#     return f"""
#   <div class="section">
#     <div class="section-title">Overall Call Score</div>
#     <div class="card">
#       <div class="overall-score-grid">
#         <div class="donut-wrapper">
#           <div class="donut-chart" style="background: conic-gradient(#f59e0b 0% {total}%, #f1f5f9 {total}% 100%);">
#             <div class="donut-inner">
#               <span class="donut-score">{total}</span>
#               <span class="donut-max">/100</span>
#             </div>
#           </div>
#         </div>
#         <div class="score-breakdown">
#           <div class="breakdown-title">Score Breakdown</div>
          
#           <div class="breakdown-row">
#             <span class="breakdown-label">Compliance (&times;35)</span>
#             <div class="breakdown-bar-bg">
#               <div class="breakdown-bar-fill fill-compliance" style="width: {c_pct}%;"></div>
#             </div>
#             <span class="breakdown-val">{c_score} / 35</span>
#           </div>

#           <div class="breakdown-row">
#             <span class="breakdown-label">Pitch Coverage (&times;30)</span>
#             <div class="breakdown-bar-bg">
#               <div class="breakdown-bar-fill fill-pitch" style="width: {p_pct}%;"></div>
#             </div>
#             <span class="breakdown-val">{p_score} / 30</span>
#           </div>

#           <div class="breakdown-row">
#             <span class="breakdown-label">Sales Quality (&times;35)</span>
#             <div class="breakdown-bar-bg">
#               <div class="breakdown-bar-fill fill-sales" style="width: {s_pct}%;"></div>
#             </div>
#             <span class="breakdown-val">{s_score} / 35</span>
#           </div>
          
#           <div style="margin-top: 4px;">
#             <span class="grade-badge">{escape(grade)}</span>
#             <div class="deductions-text">{escape(deductions)}</div>
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>"""


# def render_sales_pitch_coverage(pitch_coverage: dict) -> str:
#     if not pitch_coverage:
#         return ""

#     overall_pct = pitch_coverage.get("overall_coverage_pct", 0)
#     steps_covered = pitch_coverage.get("steps_covered", 0)
#     total_steps = pitch_coverage.get("total_steps", 0)
#     steps = pitch_coverage.get("steps", [])

#     step_html = ""
#     for s in steps:
#         status = s.get("status", "SKIPPED").upper()
#         if status == "COVERED":
#             icon = "&#10003;"
#             icon_cls = "icon-covered"
#             badge_cls = "badge-covered"
#         elif status == "PARTIAL":
#             icon = "~"
#             icon_cls = "icon-partial"
#             badge_cls = "badge-partial"
#         else:
#             icon = "&#10007;"
#             icon_cls = "icon-skipped"
#             badge_cls = "badge-skipped"

#         ts = s.get("timestamp_range")
#         ts_html = f'<span class="pitch-step-ts">{escape(ts)}</span>' if ts else ""

#         step_html += f"""
#         <div class="pitch-step">
#           <div class="pitch-step-icon {icon_cls}">{icon}</div>
#           <div class="pitch-step-content">
#             <div class="pitch-step-title-row">
#               <span class="pitch-step-name">{escape(s.get("step_title", ""))}</span>
#               <span class="pitch-step-badge {badge_cls}">{status}</span>
#               {ts_html}
#             </div>
#             <div class="pitch-step-reason">{escape(s.get("reasoning", ""))}</div>
#           </div>
#         </div>"""

#     return f"""
#   <div class="section">
#     <div class="section-title">Sales Pitch Coverage Map</div>
#     <div class="card">
#       <div class="pitch-map-header">
#         <div class="pitch-map-title">Overall Pitch Coverage Score</div>
#         <div class="pitch-overall-bar-bg">
#           <div class="pitch-overall-bar-fill" style="width: {overall_pct}%;"></div>
#         </div>
#         <div class="pitch-overall-stats">
#           <span>0%</span>
#           <span>{overall_pct}% ({steps_covered} / {total_steps} steps)</span>
#           <span>100%</span>
#         </div>
#       </div>
#       <div class="pitch-steps-container">
#         {step_html}
#       </div>
#     </div>
#   </div>"""


# def generate_html(data: dict) -> str:
#     report = data.get("report", {})
#     stats = report.get("call_statistics", {})
#     rep_name = data.get("sales_rep_name", "Rep")
#     customer = data.get("customer_name", "Customer")
#     title = f"Call Quality Report &mdash; {escape(rep_name)} / {escape(customer)}"
#     rubric = report.get("rubric_assessment")
#     has_rubric = bool(rubric and rubric.get("_methodology"))

#     if has_rubric:
#         rubric["_call_id"] = data.get("call_id")
#         rubric["_stt"] = os.path.basename(data["call_stt_file"]) if data.get("call_stt_file") else None

#     # ---- Tab 1: compliance findings ----
#     incidents = report.get("incidents") or []
#     incident_html = "\n".join(filter(None, [
#         render_incident_summary(report.get("incident_summary", {})),
#         render_incidents(incidents),
#         render_checklist(report.get("checklist", [])),
#         render_assessment(report.get("overall_assessment", "")),
#         render_recommended_action(report["recommended_action"])
#         if report.get("recommended_action") else "",
#     ]))

#     # ---- Tab 2: rubric ----
#     rubric_html = ""
#     if has_rubric:
#         rubric_html = (render_call_snapshot(rubric, stats)
#                        + render_methodology_section(rubric, CHAPTERS))

#     # ---- Tab 3: sales intelligence ----
#     # 4 WHYs and HFTE move here from the rubric tab: they are a read of the
#     # customer's psychology, not a score, and they sit naturally beside the
#     # persona and conversational telemetry.
#     si = report.get("sales_intelligence")
#     metrics = (rubric or {}).get("_metrics") or {}
#     intel_html = "\n".join(filter(None, [
#         render_persona(data, si),
#         render_dynamics(stats, metrics),
#         render_psychology(si),
#         render_diagnostics(rubric) if has_rubric else "",
#     ]))

#     panels, badges = [], {}
#     panels.append(("incident", "Incidents & Compliance", incident_html))
#     checklist = report.get("checklist") or []
#     passed = sum(1 for c in checklist if str(c.get("status", "")).upper() == "PASS")
#     badges["incident"] = (f"{len(incidents)} flagged · {passed}/{len(checklist)} pass"
#                           if checklist else f"{len(incidents)} flagged")

#     if rubric_html:
#         panels.append(("rubric", "Rubric Scorecard & Methodology", rubric_html))
#         badges["rubric"] = (f"{rubric['methodology_score']:.0f} / "
#                             f"{rubric['methodology_max']:.0f} pts")
#     if intel_html:
#         panels.append(("intel", "Sales Intelligence", intel_html))

#     dial = render_score_banner(rubric) if has_rubric else ""
#     ribbon = render_ribbon(rubric, stats) if has_rubric else ""
#     verdict = render_verdict(rubric) if has_rubric else ""

#     body = "\n".join([
#         render_record(data, report, dial=dial, ribbon=ribbon, verdict=verdict),
#         render_tabs(panels, badges=badges),
#         '  <div class="footer">Generated by Call Quality Agent '
#         '&nbsp;&middot;&nbsp; Accredian</div>',
#     ])

#     return f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <title>{title}</title>
#   <style>{CSS}
# {tabs_css()}
# {methodology_css()}
#   </style>
# </head>
# <body>
# {render_topbar(data)}
# <div class="page">
# {body}
# </div>
# </body>
# </html>
# """
"""Generate a self-contained HTML report from a call-quality report JSON file.

Usage:
    python src/report_html.py output/0.report.json
    # writes output/0.report.html
"""

import json
import os
import sys
from html import escape as html_escape

from src.report_css import CSS
from src.report_tabs import tabs_css, render_tabs
from src.report_methodology import (
    methodology_css, render_methodology_section, render_gauge,
    render_verdict, render_vitals, render_diagnostics,
)

CHAPTERS = {
    "customer_profiling": "Chapter 5", "need_identification": "Chapter 6",
    "vision_setting": "Chapter 7",     "program_mapping": "Chapter 8",
    "fee_and_urgency": "Chapter 9",    "objection_handling": "Chapter 10",
    "trust_journey": "Framework 4",
}

SEV_LABELS = {"L1": "Minor", "L2": "Major", "L3": "Critical", "None": "Clean"}
SEV_BADGE_CLASS = {"L1": "sev-L1", "L2": "sev-L2", "L3": "sev-L3", "None": "sev-None"}

# Inline SVG rather than an icon webfont: the reference pulls Material Symbols
# from Google's CDN, which would leave a row of empty boxes in an offline or
# emailed report.
ICONS = {
    "check": '<path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" '
             'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "cross": '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" '
             'stroke-width="2.6" stroke-linecap="round"/>',
    "minus": '<path d="M5 12h14" fill="none" stroke="currentColor" '
             'stroke-width="2.6" stroke-linecap="round"/>',
    "dot":   '<circle cx="12" cy="12" r="4.5" fill="currentColor"/>',
    "half":  '<path d="M12 3a9 9 0 0 1 0 18Z" fill="currentColor"/>'
             '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>',
    "chev":  '<path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" '
             'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    "audio": '<path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3Z" fill="currentColor"/>'
             '<path d="M5 11a7 7 0 0 0 14 0M12 18v4" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round"/>',
    "gavel": '<path d="m14 4 6 6-3 3-6-6 3-3ZM4 20h10M9.5 11.5 4 17" fill="none" '
             'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
             'stroke-linejoin="round"/>',
    "brain": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>'
             '<path d="M12 7v5l3.2 1.9" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round"/>',
}


def icon(name, cls="row-ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">'
            f'{ICONS.get(name, "")}</svg>')


def escape(s):
    return "" if s is None else html_escape(str(s))


def fmt_null(value, fallback="&mdash;"):
    return escape(value) if value not in (None, "") else fallback


def _fmt_dur(sec):
    if not sec:
        return "&mdash;"
    sec = int(sec)
    return f"{sec // 60}m {sec % 60:02d}s" if sec >= 60 else f"{sec}s"


# =============================================================================
# Chrome
# =============================================================================

def render_topbar(d):
    """Sticky identity bar. No action buttons: this is a generated static file,
    and a Share button that cannot share is worse than no button."""
    flagged = d.get("call_flagged", False)
    sev = d.get("highest_severity", "None") or "None"
    rec = os.path.basename(str(d.get("call_recording_file") or "")) or escape(d.get("call_id") or "")
    dur = escape(d.get("call_duration") or "")

    status = (f'<span class="tb-chip crit"><i class="tb-dot"></i>{escape(sev)} Escalation</span>'
              if flagged else
              '<span class="tb-chip ok"><i class="tb-dot"></i>No Incidents</span>')

    return f"""
  <div class="topbar">
    <div class="topbar-in">
      <div class="brand">
        <span class="brand-mark">AQ</span>
        <span class="brand-name">Accredian QA<span class="brand-tag">Enterprise</span></span>
        <span class="brand-sep">/</span>
        <span class="brand-file">{icon("audio", "row-ico")}{escape(rec)}</span>
      </div>
      <div class="topbar-right">
        {status}
        {f'<span class="tb-chip mut">{dur}</span>' if dur else ''}
      </div>
    </div>
  </div>"""


def render_registry(d, report, score):
    """Token audit bar. Engineering telemetry belongs in the chrome, not in a
    content panel competing with the call's own numbers."""
    stats = report.get("call_statistics", {}) or {}
    stt = os.path.basename(str(d.get("call_stt_file") or ""))

    items = ""
    for label, key in (("Transcript", "transcript_tokens"), ("Input", "input_tokens"),
                       ("Output", "output_tokens")):
        v = stats.get(key)
        if v:
            items += f'<span><span class="reg-k">{label}:</span><span class="reg-v">{v:,}</span></span>'
    total = stats.get("total_tokens")
    if total:
        items += (f'<span class="reg-total"><span class="reg-k">Total:</span> '
                  f'{total:,} Tokens</span>')

    ver = ""
    if score:
        ver = (f'<span class="reg-ver">Rubric v{escape(score.get("rubric_version"))} '
               f'&middot; Scoring v{escape(score.get("scoring_version"))}</span>')

    if not items and not ver:
        return ""

    return f"""
  <div class="registry">
    <div class="registry-in">
      <div class="reg-left">
        <span class="reg-title">Audit Token Registry</span>
        {f'<span class="reg-file">{escape(stt)}</span>' if stt else ''}
      </div>
      <div class="reg-right">{items}{ver}</div>
    </div>
  </div>"""


def render_hero(d, report, gauge="", verdict=""):
    """Identity, synthesis and composite score in one card: a reader answers
    who, how bad and why before deciding which tab to open."""
    rep = escape(d.get("sales_rep_name") or "Unknown rep")
    cust = escape(d.get("customer_name") or "Unknown customer")
    course = escape(d.get("course_name") or "Call Quality Report")
    institute = escape(d.get("course_institute") or "")
    date = escape(report.get("analysis_date") or "")

    def initials(name):
        parts = [w for w in str(name).split() if w]
        return "".join(w[0] for w in parts[:2]).upper() or "?"

    chip_bits = " &middot; ".join(x for x in (institute, date) if x)
    chip = (f'<span class="eyebrow-chip"><i class="tb-dot"></i>{chip_bits}</span>'
            if chip_bits else "")
    call_id = escape(d.get("call_id") or "")

    verdict_html = (f'<div class="verdict"><b>Executive synthesis:</b> {verdict}</div>'
                    if verdict else "")

    return f"""
  <div class="hero">
    <div>
      <div class="hero-eyebrow">
        {chip}
        {f'<span class="eyebrow-mut">{call_id}</span>' if call_id else ''}
      </div>
      <h1>{course}</h1>
      <div class="parties">
        <span class="party">
          <span class="party-av rep">{escape(initials(rep))}</span>
          <span class="party-name">{rep}</span>
          <span class="party-role rep">Rep</span>
        </span>
        <span class="party-arrow">&rarr;</span>
        <span class="party">
          <span class="party-av cust">{escape(initials(cust))}</span>
          <span class="party-name">{cust}</span>
          <span class="party-role cust">Prospect</span>
        </span>
      </div>
      {verdict_html}
    </div>
    {gauge}
  </div>"""


# =============================================================================
# Tab 1 — incidents & compliance
# =============================================================================

def render_incident_summary(summary):
    if not summary:
        return ""
    l1, l2, l3 = summary.get("L1", 0), summary.get("L2", 0), summary.get("L3", 0)
    total = summary.get("total", l1 + l2 + l3)

    items = ""
    for n, label, cls in ((l3, "L3 Critical", "crit"), (l2, "L2 Major", "warn"),
                          (l1, "L1 Minor", "warn")):
        items += f'<span class="pill {cls if n else ""}"><i></i>{n} {label}</span>'

    return f"""
  <div class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-title">Audited Compliance Incident Log</div>
        <div class="panel-sub">{total} flagged &middot; rep assertions cross-examined
          against official course data</div>
      </div>
      <div class="tally">{items}</div>
    </div>
  </div>"""


def render_incidents(incidents):
    """Each finding as a panel with what was said beside what is true.

    Stacking them made the reader hold the quote in their head while scrolling
    to the correction; side by side, the discrepancy is the layout."""
    if not incidents:
        return """
  <div class="panel">
    <div class="panel-body" style="color:var(--s500);font-size:13px">
      No incidents detected on this call.
    </div>
  </div>"""

    out = ""
    for inc in incidents:
        sev = inc.get("severity", "L1")
        sev_label = SEV_LABELS.get(sev, sev)
        sev_cls = SEV_BADGE_CLASS.get(sev, "sev-L1")
        ts = escape(inc.get("timestamp") or "")
        basis = escape(inc.get("violation_basis") or "")
        said = escape(inc.get("what_rep_said") or "")
        quote = escape(inc.get("transcript_quote") or "")
        correct = escape(inc.get("what_is_correct") or "")
        category = escape(inc.get("category") or "")

        grounds = f'<div class="grounds"><b>Violation grounds:</b> {basis}</div>' if basis else ""
        pair = ""
        if said or quote or correct:
            pair = f"""
        <div class="ev-pair">
          <div class="ev ev-said">
            <span class="ev-k">Rep stated verbatim</span>
            <span class="ev-v">{quote or said}</span>
          </div>
          <div class="ev ev-true">
            <span class="ev-k">Official course data</span>
            <span class="ev-v">{correct or "&mdash;"}</span>
          </div>
        </div>"""

        out += f"""
  <div class="panel inc {sev_cls}">
    <div class="panel-head">
      <div style="display:flex;align-items:center;gap:11px;flex-wrap:wrap">
        <span class="sev-badge {sev_cls}">{sev} {sev_label}</span>
        <span class="panel-title">Incident #{inc.get("id")}: {category}</span>
      </div>
      {f'<span class="pill">{ts}</span>' if ts else ''}
    </div>
    <div class="panel-body">
      {grounds}{pair}
      <div class="inc-foot">
        <span>Category <b>{category.split("&mdash;")[0].strip() or "&mdash;"}</b></span>
        <span>Severity <b>{sev} &mdash; {sev_label}</b></span>
      </div>
    </div>
  </div>"""
    return out


def render_checklist(checklist):
    """Coverage as a category grid.

    36 individual rows buried the sections below; a card per category with its
    tally and a line naming what actually failed keeps the audit on one screen.
    """
    if not checklist:
        return ""

    cats = {}
    for item in checklist:
        cats.setdefault(item.get("category", "Other"), []).append(item)

    def state(it):
        st = str(it.get("status", "")).upper()
        return ("pass" if st == "PASS"
                else "fail" if st in ("FAIL", "VIOLATION", "INCORRECT") else "nd")

    tot = {"pass": 0, "fail": 0, "nd": 0}
    cards = ""
    for cat, items in cats.items():
        c = {"pass": 0, "fail": 0, "nd": 0}
        for it in items:
            c[state(it)] += 1
            tot[state(it)] += 1

        bits = []
        if c["fail"]:
            bits.append(f'{c["fail"]} failed')
        if c["pass"]:
            bits.append(f'{c["pass"]} passed')
        if c["nd"]:
            bits.append(f'{c["nd"]} n/d')
        cls = "fail" if c["fail"] else ("nd" if not c["pass"] else "")

        failed = [escape(it.get("check", "")) for it in items if state(it) == "fail"]
        nd = [escape(it.get("check", "")) for it in items if state(it) == "nd"]
        note = ""
        if failed:
            note += f'<span class="f">Failed:</span> {"; ".join(failed)}. '
        if nd:
            note += f'Not discussed: {"; ".join(nd)}.'
        if not note:
            note = "All checks in this category passed."

        cards += f"""
      <div class="cat {'fail' if c['fail'] else ''}">
        <div class="cat-top">
          <span class="cat-name">{escape(cat)}</span>
          <span class="cat-n {cls}">{' &middot; '.join(bits)}</span>
        </div>
        <span class="cat-note">{note}</span>
      </div>"""

    n = sum(tot.values())
    pct = f"{100 * tot['pass'] / n:.1f}%" if n else "&mdash;"
    return f"""
  <div class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-title">Institutional Quality Assurance Checklist</div>
        <div class="panel-sub">{len(cats)} categories &middot; {n} checks &middot;
          {tot['pass']} passed &middot; {tot['fail']} failed &middot;
          {tot['nd']} out of scope</div>
      </div>
      <span class="pill {'crit' if tot['fail'] else 'ok'}">Checklist score {pct}</span>
    </div>
    <div class="panel-body"><div class="g3">{cards}</div></div>
  </div>"""


def render_assessment(text):
    if not text:
        return ""
    return f"""
  <div class="panel">
    <div class="panel-head"><div class="panel-title">Overall Assessment</div></div>
    <div class="panel-body" style="font-size:13px;line-height:1.72;color:var(--s700)">
      {escape(text)}
    </div>
  </div>"""


def render_recommended_action(rec):
    """Remediation protocol: priority-tagged rows, severest first."""
    if not rec:
        return ""

    actions = rec if isinstance(rec, list) else rec.get("actions")
    if not actions:
        pr = rec.get("priority") or "Follow-up"
        actions = [{"priority": pr, "action": rec.get("action", "")}]

    tone = {"immediate": "now", "short-term": "soon", "short term": "soon",
            "follow-up": "next", "follow up": "next"}
    rows = ""
    for a in actions:
        pr = str(a.get("priority", "Follow-up"))
        cls = tone.get(pr.lower(), "next")
        rows += f"""
      <div class="act {cls}">
        <span class="act-tag">{escape(pr)}</span>
        <span class="act-text">{escape(a.get("action", ""))}</span>
      </div>"""

    rule = escape(rec.get("rule", "")) if isinstance(rec, dict) else ""
    return f"""
  <div class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-title">Recommended Actions &amp; Remediation Plan</div>
        {f'<div class="panel-sub">{rule}</div>' if rule else ''}
      </div>
      <span class="pill crit">Action required</span>
    </div>
    <div class="panel-body">{rows}</div>
  </div>"""


# =============================================================================
# Tab 3 — sales intelligence
# =============================================================================

def render_persona(d, si):
    persona = (si or {}).get("customer_persona", {}) or {}
    name = d.get("customer_name") or "Customer"
    inits = "".join(w[0] for w in str(name).split()[:2]).upper() or "?"

    def val(key):
        it = persona.get(key)
        return escape(str(it.get("value") if isinstance(it, dict) else it) or "&mdash;")

    boxes = ""
    for label, key in (("Professional context", "professional_context"),
                       ("Financial baseline", "financial_baseline"),
                       ("Core motivation", "core_motivation")):
        boxes += f"""
        <div class="cat">
          <span class="stat-k">{label}</span>
          <span class="cat-note" style="font-size:12.5px;color:var(--s700)">{val(key)}</span>
        </div>"""

    return f"""
  <div class="panel">
    <div class="panel-head">
      <div style="display:flex;align-items:center;gap:13px">
        <span class="avatar">{escape(inits)}</span>
        <div>
          <div class="panel-title">{escape(name)}</div>
          <div class="panel-sub">{escape(d.get("course_institute") or "")}</div>
        </div>
      </div>
      <span class="pill">Prospect profile</span>
    </div>
    <div class="panel-body"><div class="g3">{boxes}</div></div>
  </div>"""


def render_dynamics(stats, metrics):
    if not stats and not metrics:
        return ""
    m = metrics or {}
    ratio = stats.get("rep_talk_ratio_pct")
    if ratio is None:
        ratio = m.get("rep_talk_ratio_pct") or 0
    over = ratio > 60

    def box(k, v, sub, tone=""):
        return f"""
        <div class="stat-box">
          <span class="stat-k">{k}</span>
          <span class="stat-v {tone}">{v}</span>
          <span class="stat-s">{sub}</span>
        </div>"""

    boxes = ""
    if stats.get("duration_seconds") and stats.get("rep_words"):
        wpm = stats["rep_words"] / (stats["duration_seconds"] / 60)
        boxes += box("Rep pace", f"{wpm:.0f} wpm", "measured conversational rate")

    a, b = m.get("customer_words_first_half"), m.get("customer_words_second_half")
    if a and b:
        boxes += box("Customer response", f"{a:.0f} &rarr; {b:.0f} wds",
                     "drop-off across the call" if b < a else "opened up across the call",
                     "crit" if b < a else "ok")

    q = m.get("rep_question_count")
    if q is not None:
        op = (m.get("open_question_ratio") or 0) * 100
        boxes += box("Question mix", f"{q} queries",
                     f"{op:.0f}% open &middot; {100 - op:.0f}% closed")

    lm = m.get("longest_rep_monologue_sec")
    if lm is not None:
        boxes += box("Monologue ceiling", _fmt_dur(lm), "3:00 is the penalty threshold",
                     "crit" if lm > 180 else "ok")

    return f"""
  <div class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-title">Conversational Dynamics</div>
        <div class="panel-sub">{"Rep talk time exceeds the 60% benchmark" if over
                                else "Talk ratio within benchmark"}</div>
      </div>
      <span class="pill {'crit' if over else 'ok'}">{ratio:.1f}% rep</span>
    </div>
    <div class="panel-body">
      <div class="split-legend">
        <span><b>Rep</b> {ratio:.1f}% &middot; {stats.get('rep_words', 0):,} words</span>
        <span><b>Customer</b> {100 - ratio:.1f}% &middot; {stats.get('customer_words', 0):,} words</span>
      </div>
      <div class="split-bar">
        <i style="width:{ratio:.1f}%;background:var(--s900)"></i>
        <i style="width:{100 - ratio:.1f}%;background:var(--emer)"></i>
      </div>
      <div class="g4">{boxes}</div>
    </div>
  </div>"""


def render_psychology(si):
    """Psychology and lost-opportunity signals on a dark card: these are the
    interpretive notes, visually distinct from the measured panels above."""
    if not si:
        return ""
    psych = si.get("sales_psychology", {}) or {}
    lost = si.get("lost_opportunity", {}) or {}

    def box(label, obj, key):
        it = obj.get(key)
        if isinstance(it, dict):
            v, ts = it.get("value"), it.get("timestamp")
        else:
            v, ts = it, None
        if not v:
            return ""
        head = f"{label}{f' ({escape(ts)})' if ts else ''}"
        return f"""
      <div class="dark-box">
        <span class="dark-k">{head}</span>
        <span class="dark-v">{escape(v)}</span>
      </div>"""

    boxes = "".join([
        box("Consultative vs product-push", psych, "consultative_vs_product_push"),
        box("Hype authenticity", psych, "hype_authenticity"),
        box("Delivery &amp; tone", psych, "tone_energy"),
        box("Objection handling", lost, "objection_handling"),
        box("The &ldquo;drop&rdquo; reason", lost, "drop_reason"),
    ])
    if not boxes:
        return ""

    return f"""
  <div class="dark-card">
    <h3>{icon("brain", "row-ico")}Sales Psychology &amp; Lost Opportunity Signals</h3>
    <div class="duo">{boxes}</div>
  </div>"""


# =============================================================================
# Legacy pitch-score renderers (unchanged behaviour, restyled shell)
# =============================================================================

def render_overall_call_score(s):
    """Sales Pitch score — rendered only when a Sales Pitch was uploaded."""
    if not s:
        return ""
    bars = ""
    for label, key, mx, colour in (("Compliance", "compliance_score", 35, "var(--blue)"),
                                   ("Pitch coverage", "pitch_coverage_score", 30, "var(--amber)"),
                                   ("Sales quality", "sales_quality_score", 35, "var(--emer)")):
        v = s.get(key) or 0
        pct = round(100 * v / mx) if mx else 0
        bars += f"""
        <div class="split-legend" style="margin-bottom:4px">
          <span>{label}</span><span><b>{v}</b> / {mx}</span>
        </div>
        <div class="split-bar" style="margin-bottom:12px">
          <i style="width:{pct}%;background:{colour}"></i>
        </div>"""

    return f"""
  <div class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-title">Sales Pitch Score</div>
        <div class="panel-sub">{escape(s.get("grade", ""))}</div>
      </div>
      <span class="pill dark">{s.get("total_score", 0)} / 100</span>
    </div>
    <div class="panel-body">
      {bars}
      <div class="cat-note">{escape(s.get("deductions_text", ""))}</div>
    </div>
  </div>"""


def render_sales_pitch_coverage(pc):
    if not pc or not pc.get("steps"):
        return ""
    tone = {"COVERED": ("ok", "check"), "PARTIAL": ("warn", "half"), "SKIPPED": ("bad", "cross")}
    rows = ""
    for st in pc["steps"]:
        cls, ic = tone.get(str(st.get("status", "")).upper(), ("bad", "cross"))
        ts = escape(st.get("timestamp_range") or "")
        rows += f"""
      <div class="row {cls}">
        {icon(ic)}
        <div>
          <span class="row-k">{escape(st.get("step_title", ""))}</span>
          {f'<span class="row-tag">{ts}</span>' if ts else ''}
          <div class="row-note">{escape(st.get("reasoning", ""))}</div>
        </div>
      </div>"""

    return f"""
  <div class="panel">
    <div class="panel-head">
      <div class="panel-title">Sales Pitch Coverage</div>
      <span class="pill">{pc.get("steps_covered", 0)} / {pc.get("total_steps", 0)} steps
        &middot; {pc.get("overall_coverage_pct", 0)}%</span>
    </div>
    <div class="panel-body"><div class="rows">{rows}</div></div>
  </div>"""


# =============================================================================
# Page
# =============================================================================

def generate_html(data: dict) -> str:
    report = data.get("report", {})
    stats = report.get("call_statistics", {}) or {}
    rep_name = data.get("sales_rep_name", "Rep")
    customer = data.get("customer_name", "Customer")
    title = f"Call Quality Report &mdash; {escape(rep_name)} / {escape(customer)}"

    rubric = report.get("rubric_assessment")
    has_rubric = bool(rubric and rubric.get("_methodology"))
    metrics = (rubric or {}).get("_metrics") or {}

    # ---- Tab 1: compliance findings ----
    incidents = report.get("incidents") or []
    incident_html = "\n".join(filter(None, [
        render_incident_summary(report.get("incident_summary", {})),
        render_incidents(incidents),
        render_checklist(report.get("checklist", [])),
        render_overall_call_score(report.get("overall_call_score")),
        render_sales_pitch_coverage(report.get("sales_pitch_coverage")),

        render_recommended_action(report.get("recommended_action")),
    ]))

    # ---- Tab 2: rubric & methodology ----
    rubric_html = render_methodology_section(rubric, CHAPTERS) if has_rubric else ""

    # ---- Tab 3: sales intelligence ----
    # The 4 WHYs and HFTE live here rather than in the rubric tab: they read the
    # customer's psychology, they are not a score.
    si = report.get("sales_intelligence")
    intel_html = "\n".join(filter(None, [
        render_persona(data, si),
        render_dynamics(stats, metrics),
        render_diagnostics(rubric) if has_rubric else "",
        render_psychology(si),
    ]))

    checklist = report.get("checklist") or []
    passed = sum(1 for c in checklist if str(c.get("status", "")).upper() == "PASS")

    panels = [("incident", "Incidents & Compliance", incident_html)]
    badges = {"incident": (f"{len(incidents)} flagged \u00b7 {passed}/{len(checklist)} pass"
                           if checklist else f"{len(incidents)} flagged")}
    if rubric_html:
        panels.append(("rubric", "Rubric & Methodology", rubric_html))
        badges["rubric"] = f"{rubric['methodology_score']:.0f} / {rubric['methodology_max']:.0f} pts"
    if intel_html:
        panels.append(("intel", "Sales Intelligence & Prospect", intel_html))
        tj = (rubric or {}).get("_methodology", {}).get("trust_journey", {})
        reached = sum(1 for s in tj.get("stages", []) if s.get("reached"))
        if tj.get("stages"):
            badges["intel"] = f"{reached}/5 trust reached"

    gauge = render_gauge(rubric) if has_rubric else ""
    verdict = render_verdict(rubric) if has_rubric else ""
    vitals = render_vitals(rubric, stats) if has_rubric else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>{CSS}
{tabs_css()}
{methodology_css()}
  </style>
</head>
<body>
{render_topbar(data)}
{render_registry(data, report, rubric if has_rubric else None)}
<div class="page">
{render_hero(data, report, gauge=gauge, verdict=verdict)}
{vitals}
{render_tabs(panels, badges=badges)}
</div>
<div class="footer">
  <span class="footer-l"><i class="footer-dot"></i>Accredian QA Intelligence Engine</span>
  <span>{escape(report.get("analysis_date") or "")}</span>
</div>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    data = json.loads(open(src, encoding="utf-8").read())
    out = src.replace(".report.json", ".report.html")
    open(out, "w", encoding="utf-8").write(generate_html(data))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
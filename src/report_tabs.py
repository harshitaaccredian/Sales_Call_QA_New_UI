# # """
# # Tab shell for the call quality report.

# # Wraps the existing report body (Incident Report) and the new Sales Bible
# # assessment (Rubric Report) into two switchable tabs, without touching either
# # one's markup.

# # Design notes
# # ------------
# # - No framework. The existing report is vanilla CSS on a slate palette; pulling
# #   in a Tailwind CDN for two tabs would add a network dependency to a file that
# #   is often opened straight from disk or emailed as an attachment.
# # - Tabs work without JavaScript. The CSS `:checked` sibling selector drives
# #   visibility off hidden radio inputs, so the report degrades to a working
# #   document in any renderer that blocks scripts (many email clients, some PDF
# #   converters). The small script only adds deep-linking via #hash.
# # - Print stylesheet expands every panel, so Cmd-P still produces the full report
# #   rather than whichever tab happened to be open.

# # Usage
# # -----
# #     from src.report_tabs import tabs_css, render_tabs

# #     body = render_tabs([
# #         ("incident", "Incident Report", incident_html),
# #         ("rubric",   "Rubric Report",   rubric_html),
# #     ])
# # """

# # from __future__ import annotations

# # import html as _html


# # def tabs_css() -> str:
# #     return """
# #     /* ---- Report tabs ---- */
# #     /* ---- Pill tabs: filled dark when active ---- */
# #     .rt-tabs { margin-bottom: 24px; }
# #     .rt-radio { position: absolute; opacity: 0; pointer-events: none; }

# #     .rt-tablist { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 24px; }
# #     .rt-tab {
# #       flex: 1 1 230px; cursor: pointer; user-select: none;
# #       padding: 12px 16px; border-radius: 9px;
# #       display: inline-flex; align-items: center; justify-content: center; gap: 9px;
# #       font-size: 13px; font-weight: 600; color: var(--ink-600, #475569);
# #       background: transparent; border: 1px solid transparent;
# #       transition: background .14s ease, color .14s ease, border-color .14s ease;
# #       white-space: nowrap; min-width: 0;
# #     }
# #     .rt-tab:hover { color: var(--ink-950, #090d16); background: var(--ink-100, #f1f5f9); }
# #     .rt-tab:focus-visible { outline: 2px solid var(--accent, #2563eb); outline-offset: 2px; }
# #     .rt-tab-ico { width: 16px; height: 16px; flex: none; opacity: .85; }
# #     .rt-tab-label { overflow: hidden; text-overflow: ellipsis; }

# #     .rt-badge {
# #       font-family: var(--mono, monospace);
# #       font-size: 10.5px; font-weight: 500; padding: 2px 8px; border-radius: 5px;
# #       background: var(--ink-100, #f1f5f9); color: var(--ink-600, #475569);
# #       border: 1px solid var(--ink-200, #e2e8f0); flex: none;
# #     }

# #     .rt-panel { display: none; }

# #     #rt-0:checked ~ .rt-tablist label[for="rt-0"],
# #     #rt-1:checked ~ .rt-tablist label[for="rt-1"],
# #     #rt-2:checked ~ .rt-tablist label[for="rt-2"] {
# #       background: var(--ink-950, #090d16); color: #fff;
# #       border-color: var(--ink-950, #090d16);
# #       box-shadow: 0 1px 2px rgba(9,13,22,.2);
# #     }
# #     #rt-0:checked ~ .rt-tablist label[for="rt-0"] .rt-badge,
# #     #rt-1:checked ~ .rt-tablist label[for="rt-1"] .rt-badge,
# #     #rt-2:checked ~ .rt-tablist label[for="rt-2"] .rt-badge {
# #       background: var(--ink-800, #1e293b); color: var(--ink-200, #e2e8f0);
# #       border-color: var(--ink-700, #334155);
# #     }
# #     #rt-0:checked ~ .rt-panels > #rt-panel-0,
# #     #rt-1:checked ~ .rt-panels > #rt-panel-1,
# #     #rt-2:checked ~ .rt-panels > #rt-panel-2 { display: block; }

# #     /* No-JS / unsupported-selector fallback: never render a blank page. */
# #     .rt-panels > .rt-panel:first-child { display: block; }
# #     #rt-1:checked ~ .rt-panels > .rt-panel:first-child,
# #     #rt-2:checked ~ .rt-panels > .rt-panel:first-child { display: none; }

# #     @media print {
# #       .rt-tablist { display: none; }
# #       .rt-panel, .rt-panels > .rt-panel:first-child { display: block !important; }
# #       .rt-panel + .rt-panel { page-break-before: always; }
# #     }
# #     @media (max-width: 760px) {
# #       .rt-tab { flex: 1 1 100%; justify-content: flex-start; }
# #     }
# #     """


# # # Inline SVGs rather than an icon webfont: the reference uses Material Symbols
# # # from Google's CDN, which would leave a row of empty boxes in an offline or
# # # emailed report.
# # _ICONS = {
# #     "incident": '<path d="M12 2 3 6v6c0 5 3.8 9.2 9 10 5.2-.8 9-5 9-10V6l-9-4Z"/>'
# #                 '<path d="M12 8v5" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
# #                 '<circle cx="12" cy="16.2" r="1.1" fill="#fff"/>',
# #     "rubric":   '<path d="M4 4h16v16H4z" opacity=".15"/>'
# #                 '<path d="M7 8h10M7 12h10M7 16h6" stroke="currentColor" stroke-width="2" '
# #                 'stroke-linecap="round" fill="none"/>',
# #     "intel":    '<circle cx="12" cy="12" r="9" opacity=".15"/>'
# #                 '<path d="M12 7v5l3.2 1.9" stroke="currentColor" stroke-width="2" '
# #                 'stroke-linecap="round" fill="none"/>',
# # }


# # def _icon(slug: str) -> str:
# #     path = _ICONS.get(slug)
# #     if not path:
# #         return ""
# #     return (f'<svg class="rt-tab-ico" viewBox="0 0 24 24" fill="currentColor" '
# #             f'aria-hidden="true">{path}</svg>')


# # def render_tabs(panels: list[tuple[str, str, str]], badges: dict[str, str] | None = None) -> str:
# #     """Build the tab shell.

# #     Args:
# #         panels: list of (slug, label, inner_html), in display order.
# #         badges: optional {slug: badge_text}, e.g. {"incident": "3", "rubric": "62"}.

# #     Returns the complete tabs markup. Requires tabs_css() in the stylesheet.
# #     """
# #     badges = badges or {}
# #     e = lambda v: _html.escape(str(v), quote=True)

# #     radios = "".join(
# #         f'<input class="rt-radio" type="radio" name="rt" id="rt-{i}"'
# #         f'{" checked" if i == 0 else ""}>'
# #         for i in range(len(panels))
# #     )

# #     tabs = ""
# #     for i, (slug, label, _) in enumerate(panels):
# #         badge = (f'<span class="rt-badge">{e(badges[slug])}</span>'
# #                  if slug in badges and badges[slug] not in (None, "") else "")
# #         tabs += (f'<label class="rt-tab" for="rt-{i}" tabindex="0" '
# #                  f'role="tab" data-slug="{e(slug)}">{_icon(slug)}'
# #                  f'<span class="rt-tab-label">{e(label)}</span>{badge}</label>')

# #     body = "".join(
# #         f'<div class="rt-panel" id="rt-panel-{i}" data-slug="{e(slug)}" role="tabpanel">{inner}</div>'
# #         for i, (slug, _, inner) in enumerate(panels)
# #     )

# #     # Progressive enhancement only: keyboard activation and #hash deep-linking.
# #     script = """
# # <script>
# # (function () {
# #   var labels = document.querySelectorAll('.rt-tab');
# #   function select(slug) {
# #     for (var i = 0; i < labels.length; i++) {
# #       if (labels[i].dataset.slug === slug) {
# #         var r = document.getElementById(labels[i].getAttribute('for'));
# #         if (r) { r.checked = true; }
# #         return true;
# #       }
# #     }
# #     return false;
# #   }
# #   labels.forEach(function (el) {
# #     el.addEventListener('keydown', function (ev) {
# #       if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); el.click(); }
# #     });
# #     el.addEventListener('click', function () {
# #       if (history.replaceState) {
# #         history.replaceState(null, '', '#' + el.dataset.slug);
# #       }
# #     });
# #   });
# #   if (location.hash) { select(location.hash.slice(1)); }
# # })();
# # </script>"""

# #     return (f'<div class="rt-tabs">{radios}'
# #             f'<div class="rt-tablist" role="tablist">{tabs}</div>'
# #             f'<div class="rt-panels">{body}</div></div>{script}')

# """
# Tab shell for the call quality report.

# Wraps the existing report body (Incident Report) and the new Sales Bible
# assessment (Rubric Report) into two switchable tabs, without touching either
# one's markup.

# Design notes
# ------------
# - No framework. The existing report is vanilla CSS on a slate palette; pulling
#   in a Tailwind CDN for two tabs would add a network dependency to a file that
#   is often opened straight from disk or emailed as an attachment.
# - Tabs work without JavaScript. The CSS `:checked` sibling selector drives
#   visibility off hidden radio inputs, so the report degrades to a working
#   document in any renderer that blocks scripts (many email clients, some PDF
#   converters). The small script only adds deep-linking via #hash.
# - Print stylesheet expands every panel, so Cmd-P still produces the full report
#   rather than whichever tab happened to be open.

# Usage
# -----
#     from src.report_tabs import tabs_css, render_tabs

#     body = render_tabs([
#         ("incident", "Incident Report", incident_html),
#         ("rubric",   "Rubric Report",   rubric_html),
#     ])
# """

# from __future__ import annotations

# import html as _html


# def tabs_css() -> str:
#     return """
#     /* ---- Report tabs ---- */
#     /* ---- Pill tabs: filled dark when active ---- */
#     .rt-tabs { margin-bottom: 24px; }
#     .rt-radio { position: absolute; opacity: 0; pointer-events: none; }

#     .rt-tablist { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 24px; }
#     .rt-tab {
#       flex: 1 1 230px; cursor: pointer; user-select: none;
#       padding: 12px 16px; border-radius: 9px;
#       display: inline-flex; align-items: center; justify-content: center; gap: 9px;
#       font-size: 13px; font-weight: 600; color: var(--ink-600, #475569);
#       background: transparent; border: 1px solid transparent;
#       transition: background .14s ease, color .14s ease, border-color .14s ease;
#       white-space: nowrap; min-width: 0;
#     }
#     .rt-tab:hover { color: var(--ink-950, #090d16); background: var(--ink-100, #f1f5f9); }
#     .rt-tab:focus-visible { outline: 2px solid var(--accent, #2563eb); outline-offset: 2px; }
#     .rt-tab-ico { width: 16px; height: 16px; flex: none; opacity: .85; }
#     .rt-tab-label { overflow: hidden; text-overflow: ellipsis; }

#     .rt-badge {
#       font-family: var(--mono, monospace);
#       font-size: 10.5px; font-weight: 500; padding: 2px 8px; border-radius: 5px;
#       background: var(--ink-100, #f1f5f9); color: var(--ink-600, #475569);
#       border: 1px solid var(--ink-200, #e2e8f0); flex: none;
#     }

#     .rt-panel { display: none; }

#     #rt-0:checked ~ .rt-tablist label[for="rt-0"],
#     #rt-1:checked ~ .rt-tablist label[for="rt-1"],
#     #rt-2:checked ~ .rt-tablist label[for="rt-2"] {
#       background: var(--ink-950, #090d16); color: #fff;
#       border-color: var(--ink-950, #090d16);
#       box-shadow: 0 1px 2px rgba(9,13,22,.2);
#     }
#     #rt-0:checked ~ .rt-tablist label[for="rt-0"] .rt-badge,
#     #rt-1:checked ~ .rt-tablist label[for="rt-1"] .rt-badge,
#     #rt-2:checked ~ .rt-tablist label[for="rt-2"] .rt-badge {
#       background: var(--ink-800, #1e293b); color: var(--ink-200, #e2e8f0);
#       border-color: var(--ink-700, #334155);
#     }
#     #rt-0:checked ~ .rt-panels > #rt-panel-0,
#     #rt-1:checked ~ .rt-panels > #rt-panel-1,
#     #rt-2:checked ~ .rt-panels > #rt-panel-2 { display: block; }

#     /* No-JS / unsupported-selector fallback: never render a blank page. */
#     .rt-panels > .rt-panel:first-child { display: block; }
#     #rt-1:checked ~ .rt-panels > .rt-panel:first-child,
#     #rt-2:checked ~ .rt-panels > .rt-panel:first-child { display: none; }

#     @media print {
#       .rt-tablist { display: none; }
#       .rt-panel, .rt-panels > .rt-panel:first-child { display: block !important; }
#       .rt-panel + .rt-panel { page-break-before: always; }
#     }
#     @media (max-width: 760px) {
#       .rt-tab { flex: 1 1 100%; justify-content: flex-start; }
#     }
#     """


# # Inline SVGs rather than an icon webfont: the reference uses Material Symbols
# # from Google's CDN, which would leave a row of empty boxes in an offline or
# # emailed report.
# _ICONS = {
#     "incident": '<path d="M12 2 3 6v6c0 5 3.8 9.2 9 10 5.2-.8 9-5 9-10V6l-9-4Z"/>'
#                 '<path d="M12 8v5" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
#                 '<circle cx="12" cy="16.2" r="1.1" fill="#fff"/>',
#     "rubric":   '<path d="M4 4h16v16H4z" opacity=".15"/>'
#                 '<path d="M7 8h10M7 12h10M7 16h6" stroke="currentColor" stroke-width="2" '
#                 'stroke-linecap="round" fill="none"/>',
#     "intel":    '<circle cx="12" cy="12" r="9" opacity=".15"/>'
#                 '<path d="M12 7v5l3.2 1.9" stroke="currentColor" stroke-width="2" '
#                 'stroke-linecap="round" fill="none"/>',
# }


# def _icon(slug: str) -> str:
#     path = _ICONS.get(slug)
#     if not path:
#         return ""
#     return (f'<svg class="rt-tab-ico" viewBox="0 0 24 24" fill="currentColor" '
#             f'aria-hidden="true">{path}</svg>')


# def render_tabs(panels: list[tuple[str, str, str]], badges: dict[str, str] | None = None) -> str:
#     """Build the tab shell.

#     Args:
#         panels: list of (slug, label, inner_html), in display order.
#         badges: optional {slug: badge_text}, e.g. {"incident": "3", "rubric": "62"}.

#     Returns the complete tabs markup. Requires tabs_css() in the stylesheet.
#     """
#     badges = badges or {}
#     e = lambda v: _html.escape(str(v), quote=True)

#     radios = "".join(
#         f'<input class="rt-radio" type="radio" name="rt" id="rt-{i}"'
#         f'{" checked" if i == 0 else ""}>'
#         for i in range(len(panels))
#     )

#     tabs = ""
#     for i, (slug, label, _) in enumerate(panels):
#         badge = (f'<span class="rt-badge">{e(badges[slug])}</span>'
#                  if slug in badges and badges[slug] not in (None, "") else "")
#         tabs += (f'<label class="rt-tab" for="rt-{i}" tabindex="0" '
#                  f'role="tab" data-slug="{e(slug)}">{_icon(slug)}'
#                  f'<span class="rt-tab-label">{e(label)}</span>{badge}</label>')

#     body = "".join(
#         f'<div class="rt-panel" id="rt-panel-{i}" data-slug="{e(slug)}" role="tabpanel">{inner}</div>'
#         for i, (slug, _, inner) in enumerate(panels)
#     )

#     # Progressive enhancement only: keyboard activation and #hash deep-linking.
#     script = """
# <script>
# (function () {
#   var labels = document.querySelectorAll('.rt-tab');
#   function select(slug) {
#     for (var i = 0; i < labels.length; i++) {
#       if (labels[i].dataset.slug === slug) {
#         var r = document.getElementById(labels[i].getAttribute('for'));
#         if (r) { r.checked = true; }
#         return true;
#       }
#     }
#     return false;
#   }
#   labels.forEach(function (el) {
#     el.addEventListener('keydown', function (ev) {
#       if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); el.click(); }
#     });
#     el.addEventListener('click', function () {
#       if (history.replaceState) {
#         history.replaceState(null, '', '#' + el.dataset.slug);
#       }
#     });
#   });
#   if (location.hash) { select(location.hash.slice(1)); }
# })();
# </script>"""

#     return (f'<div class="rt-tabs">{radios}'
#             f'<div class="rt-tablist" role="tablist">{tabs}</div>'
#             f'<div class="rt-panels">{body}</div></div>{script}')


"""
Tab shell for the call quality report.

Wraps the existing report body (Incident Report) and the new Sales Bible
assessment (Rubric Report) into two switchable tabs, without touching either
one's markup.

Design notes
------------
- No framework. The existing report is vanilla CSS on a slate palette; pulling
  in a Tailwind CDN for two tabs would add a network dependency to a file that
  is often opened straight from disk or emailed as an attachment.
- Tabs work without JavaScript. The CSS `:checked` sibling selector drives
  visibility off hidden radio inputs, so the report degrades to a working
  document in any renderer that blocks scripts (many email clients, some PDF
  converters). The small script only adds deep-linking via #hash.
- Print stylesheet expands every panel, so Cmd-P still produces the full report
  rather than whichever tab happened to be open.

Usage
-----
    from src.report_tabs import tabs_css, render_tabs

    body = render_tabs([
        ("incident", "Incident Report", incident_html),
        ("rubric",   "Rubric Report",   rubric_html),
    ])
"""

from __future__ import annotations

import html as _html


def tabs_css() -> str:
    return """
    /* ---- Report tabs: segmented control ----
       Inactive tabs get their own white surface + hairline border inside a
       recessed track, so every segment reads as a discrete button rather than
       as text floating on the page. Active segment is the dark fill. */
    .rt-tabs { margin-bottom: 22px; }
    .rt-radio { position: absolute; opacity: 0; pointer-events: none; }

    .rt-tablist {
      display: flex; gap: 5px; flex-wrap: wrap;
      margin-bottom: 22px; padding: 5px;
      background: #2b3040;
      border: 1px solid #2b3040;
      border-radius: 12px;
      box-shadow: inset 0 1px 2px rgba(0,0,0,.15);
    }
    .rt-tab {
      flex: 1 1 0; min-width: 0; cursor: pointer; user-select: none;
      padding: 10px 14px; border-radius: 8px;
      display: inline-flex; align-items: center; justify-content: center; gap: 9px;
      font-size: 13px; font-weight: 600; color: #cbd5e1;
      background: transparent;
      border: 1px solid transparent;
      box-shadow: none;
      transition: background .14s ease, color .14s ease,
                  border-color .14s ease, box-shadow .14s ease, transform .14s ease;
    }
    .rt-tab:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
      border-color: transparent;
      box-shadow: none;
      transform: translateY(-1px);
    }
    .rt-tab:active { transform: translateY(0); }
    .rt-tab:focus-visible { outline: 2px solid var(--blue, #2563eb); outline-offset: 2px; }
    
    .rt-tab-ico { width: 17px; height: 17px; flex: none; opacity: 1; }
    label[for="rt-0"] .rt-tab-ico { color: #f59e0b; }
    label[for="rt-1"] .rt-tab-ico { color: #3b82f6; }
    label[for="rt-2"] .rt-tab-ico { color: #10b981; }
    
    .rt-tab-label { white-space: nowrap; }

    .rt-badge {
      font-family: var(--mono, monospace);
      font-size: 10.5px; font-weight: 600; padding: 4px 10px; border-radius: 12px;
      background: rgba(255,255,255,0.05); color: #94a3b8;
      border: 1px solid rgba(255,255,255,0.05); flex: none; white-space: nowrap;
    }

    .rt-panel { display: none; }

    #rt-0:checked ~ .rt-tablist label[for="rt-0"],
    #rt-1:checked ~ .rt-tablist label[for="rt-1"],
    #rt-2:checked ~ .rt-tablist label[for="rt-2"] {
      background: #fff; color: #1e293b;
      border-color: #fff;
      box-shadow: 0 2px 8px rgba(0,0,0,.1);
      transform: none;
    }
    #rt-0:checked ~ .rt-tablist label[for="rt-0"] .rt-tab-ico,
    #rt-1:checked ~ .rt-tablist label[for="rt-1"] .rt-tab-ico,
    #rt-2:checked ~ .rt-tablist label[for="rt-2"] .rt-tab-ico { opacity: 1; }
    #rt-0:checked ~ .rt-tablist label[for="rt-0"] .rt-badge {
      background: #fffbeb; color: #b45309; border-color: #fde68a;
    }
    #rt-1:checked ~ .rt-tablist label[for="rt-1"] .rt-badge {
      background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe;
    }
    #rt-2:checked ~ .rt-tablist label[for="rt-2"] .rt-badge {
      background: #f0fdf4; color: #15803d; border-color: #bbf7d0;
    }
    #rt-0:checked ~ .rt-panels > #rt-panel-0,
    #rt-1:checked ~ .rt-panels > #rt-panel-1,
    #rt-2:checked ~ .rt-panels > #rt-panel-2 { display: block; }

    /* No-JS / unsupported-selector fallback: never render a blank page. */
    .rt-panels > .rt-panel:first-child { display: block; }
    #rt-1:checked ~ .rt-panels > .rt-panel:first-child,
    #rt-2:checked ~ .rt-panels > .rt-panel:first-child { display: none; }

    /* Below this the three labels + badges no longer fit side by side and
       would clip inside their own segments, so stack them full width. */
    @media (max-width: 1100px) {
      .rt-tablist { border-radius: 12px; }
      .rt-tab { flex: 1 1 100%; justify-content: flex-start; }
      .rt-tab .rt-badge { margin-left: auto; }
    }
    /* Phone: the longest badge no longer fits beside its label, so let the
       segment wrap instead of pressing the badge against the border. */
    @media (max-width: 480px) {
      .rt-tab { flex-wrap: wrap; row-gap: 7px; }
    }

    @media print {
      .rt-tablist { display: none; }
      .rt-panel, .rt-panels > .rt-panel:first-child { display: block !important; }
      .rt-panel + .rt-panel { page-break-before: always; }
    }
    """


# Inline SVGs rather than an icon webfont: the reference uses Material Symbols
# from Google's CDN, which would leave a row of empty boxes in an offline or
# emailed report.
_ICONS = {
    "incident": '<path d="M12 2 3 6v6c0 5 3.8 9.2 9 10 5.2-.8 9-5 9-10V6l-9-4Z"/>'
                '<path d="M12 8v5" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
                '<circle cx="12" cy="16.2" r="1.1" fill="#fff"/>',
    "rubric":   '<path d="M4 4h16v16H4z" opacity=".15"/>'
                '<path d="M7 8h10M7 12h10M7 16h6" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" fill="none"/>',
    "intel":    '<circle cx="12" cy="12" r="9" opacity=".15"/>'
                '<path d="M12 7v5l3.2 1.9" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" fill="none"/>',
}


def _icon(slug: str) -> str:
    path = _ICONS.get(slug)
    if not path:
        return ""
    return (f'<svg class="rt-tab-ico" viewBox="0 0 24 24" fill="currentColor" '
            f'aria-hidden="true">{path}</svg>')


def render_tabs(panels: list[tuple[str, str, str]], badges: dict[str, str] | None = None) -> str:
    """Build the tab shell.

    Args:
        panels: list of (slug, label, inner_html), in display order.
        badges: optional {slug: badge_text}, e.g. {"incident": "3", "rubric": "62"}.

    Returns the complete tabs markup. Requires tabs_css() in the stylesheet.
    """
    badges = badges or {}
    e = lambda v: _html.escape(str(v), quote=True)

    radios = "".join(
        f'<input class="rt-radio" type="radio" name="rt" id="rt-{i}"'
        f'{" checked" if i == 0 else ""}>'
        for i in range(len(panels))
    )

    tabs = ""
    for i, (slug, label, _) in enumerate(panels):
        badge = (f'<span class="rt-badge">{e(badges[slug])}</span>'
                 if slug in badges and badges[slug] not in (None, "") else "")
        tabs += (f'<label class="rt-tab" for="rt-{i}" tabindex="0" '
                 f'role="tab" data-slug="{e(slug)}">{_icon(slug)}'
                 f'<span class="rt-tab-label">{e(label)}</span>{badge}</label>')

    body = "".join(
        f'<div class="rt-panel" id="rt-panel-{i}" data-slug="{e(slug)}" role="tabpanel">{inner}</div>'
        for i, (slug, _, inner) in enumerate(panels)
    )

    # Progressive enhancement only: keyboard activation and #hash deep-linking.
    script = """
<script>
(function () {
  var labels = document.querySelectorAll('.rt-tab');
  function select(slug) {
    for (var i = 0; i < labels.length; i++) {
      if (labels[i].dataset.slug === slug) {
        var r = document.getElementById(labels[i].getAttribute('for'));
        if (r) { r.checked = true; }
        return true;
      }
    }
    return false;
  }
  labels.forEach(function (el) {
    el.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); el.click(); }
    });
    el.addEventListener('click', function () {
      if (history.replaceState) {
        history.replaceState(null, '', '#' + el.dataset.slug);
      }
    });
  });
  if (location.hash) { select(location.hash.slice(1)); }

  // Expand/collapse all accordions. Revealed only once this runs, so a
  // JS-free reader is never shown a control that cannot work.
  var btn = document.querySelector('[data-expand-all]');
  if (btn) {
    btn.hidden = false;
    btn.addEventListener('click', function () {
      var all = document.querySelectorAll('details.acc');
      var open = btn.getAttribute('data-open') === '1';
      all.forEach(function (d) { d.open = !open; });
      btn.setAttribute('data-open', open ? '0' : '1');
      btn.textContent = open ? 'Expand all details' : 'Collapse all details';
    });
  }
})();
</script>"""

    return (f'<div class="rt-tabs">{radios}'
            f'<div class="rt-tablist" role="tablist">{tabs}</div>'
            f'<div class="rt-panels">{body}</div></div>{script}')
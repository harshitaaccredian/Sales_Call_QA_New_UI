"""Design-system stylesheet for the call quality report.

Mirrors the approved reference UI. Two typefaces by role: sans for prose a
person wrote, mono for anything a machine measured. No webfonts and no CDN —
these reports are emailed and opened from disk, so a network dependency means a
broken document offline. The stacks below resolve to Inter-class and
SF-Mono-class faces natively on macOS, Windows and most Linux desktops.
"""

CSS = """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --s950:#020617; --s900:#0f172a; --s800:#1e293b; --s700:#334155;
      --s600:#475569; --s500:#64748b; --s400:#94a3b8; --s300:#cbd5e1;
      --s200:#e2e8f0; --s100:#f1f5f9; --s50:#f8fafc;

      --blue:#2563eb;   --blue-d:#1d4ed8;  --blue-bg:#eff6ff;  --blue-br:#bfdbfe;
      --indigo:#4f46e5;
      --rose:#e11d48;   --rose-d:#9f1239;  --rose-bg:#fff1f2;  --rose-br:#fecdd3;
      --amber:#d97706;  --amber-d:#92400e; --amber-bg:#fffbeb; --amber-br:#fde68a;
      --emer:#059669;   --emer-d:#065f46;  --emer-bg:#ecfdf5;  --emer-br:#a7f3d0;
      --sky:#0284c7;    --sky-bg:#f0f9ff;  --sky-br:#bae6fd;

      --sans: -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI",
              Inter, Roboto, "Helvetica Neue", Arial, sans-serif;
      --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
              "Liberation Mono", "Courier New", monospace;

      --r: 14px; --r-sm: 10px;
      --sh: 0 1px 2px 0 rgba(15,23,42,.04);
      --sh-xs: 0 1px 2px 0 rgba(15,23,42,.03);
    }

    body {
      font-family: var(--sans); font-size: 14px; line-height: 1.6;
      color: var(--s700); background: var(--s50);
      font-variant-numeric: tabular-nums;
      -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
    }
    .mono { font-family: var(--mono); }
    .page { max-width: 1180px; margin: 0 auto; padding: 0 24px; }

    /* ================= Top bar ================= */
    .topbar { position: sticky; top: 0; z-index: 60;
              background: var(--s900); border-bottom: 1px solid var(--s800); }
    .topbar-in {
      max-width: 1180px; margin: 0 auto; padding: 0 24px; height: 56px;
      display: flex; align-items: center; justify-content: space-between; gap: 16px;
    }
    .brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
    .brand-mark {
      width: 28px; height: 28px; border-radius: 7px; flex: none;
      background: linear-gradient(45deg, var(--blue), #6366f1);
      color: #fff; display: flex; align-items: center; justify-content: center;
      font-weight: 700; font-size: 11px; box-shadow: 0 2px 8px rgba(37,99,235,.35);
    }
    .brand-name { color: #fff; font-weight: 700; font-size: 14px;
                  letter-spacing: -0.2px; white-space: nowrap; }
    .brand-tag {
      font-family: var(--mono); font-size: 9.5px; text-transform: uppercase;
      letter-spacing: .05em; padding: 2px 6px; border-radius: 4px;
      background: var(--s800); border: 1px solid var(--s700); color: var(--s400);
      margin-left: 7px;
    }
    .brand-sep { color: var(--s600); }
    .brand-file {
      font-family: var(--mono); font-size: 12px; color: var(--s300);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      display: flex; align-items: center; gap: 6px; min-width: 0;
    }
    .topbar-right { display: flex; align-items: center; gap: 10px; flex: none; }
    .tb-chip {
      display: inline-flex; align-items: center; gap: 7px;
      padding: 5px 10px; border-radius: 6px;
      font-family: var(--mono); font-size: 11.5px; font-weight: 600; white-space: nowrap;
    }
    .tb-chip.crit { background: rgba(127,29,29,.5); border: 1px solid rgba(153,27,27,.8);
                    color: #fca5a5; }
    .tb-chip.ok   { background: rgba(6,78,59,.5); border: 1px solid rgba(6,95,70,.8);
                    color: #6ee7b7; }
    .tb-chip.mut  { background: var(--s800); border: 1px solid var(--s700); color: var(--s300); }
    .tb-dot { width: 7px; height: 7px; border-radius: 50%; flex: none; }
    .tb-chip.crit .tb-dot { background: #ef4444; }
    .tb-chip.ok .tb-dot { background: #10b981; }

    /* ================= Token registry bar ================= */
    .registry { background: var(--s950); border-bottom: 1px solid rgba(30,41,59,.8);
                color: var(--s300); font-family: var(--mono); font-size: 11.5px;
                padding: 9px 0; }
    .registry-in {
      max-width: 1180px; margin: 0 auto; padding: 0 24px;
      display: flex; flex-wrap: wrap; align-items: center;
      justify-content: space-between; gap: 8px 24px;
    }
    .reg-left { display: flex; align-items: center; gap: 9px; min-width: 0; color: var(--s400); }
    .reg-title { color: var(--s200); font-weight: 600; white-space: nowrap; }
    .reg-file { color: var(--s500); font-size: 11px; white-space: nowrap;
                overflow: hidden; text-overflow: ellipsis; max-width: 340px; }
    .reg-right { display: flex; flex-wrap: wrap; align-items: center; gap: 16px; }
    .reg-k { color: var(--s500); }
    .reg-v { color: var(--s200); font-weight: 600; margin-left: 5px; }
    .reg-total { padding: 3px 9px; border-radius: 5px; background: var(--s900);
                 border: 1px solid var(--s800); color: #60a5fa; font-weight: 700; }
    .reg-total .reg-k { color: var(--s400); font-weight: 400; }
    .reg-ver { color: var(--s500); border-left: 1px solid var(--s800); padding-left: 14px; }

    /* ================= Hero ================= */
    .hero {
      background: #fff; border: 1px solid rgba(226,232,240,.9); border-radius: 16px;
      box-shadow: var(--sh); padding: 26px 28px; margin: 24px 0; display: grid;
      grid-template-columns: minmax(0,8fr) minmax(0,4fr); gap: 30px; align-items: start;
    }
    .hero-eyebrow { display: flex; flex-wrap: wrap; align-items: center; gap: 9px; margin-bottom: 11px; }
    .eyebrow-chip {
      display: inline-flex; align-items: center; gap: 7px;
      padding: 3px 11px; border-radius: 999px; background: var(--s100);
      color: var(--s700); font-family: var(--mono); font-size: 10.5px;
      font-weight: 600; text-transform: uppercase; letter-spacing: .03em;
    }
    .eyebrow-chip .tb-dot { background: var(--indigo); width: 6px; height: 6px; }
    .eyebrow-mut { font-family: var(--mono); font-size: 11.5px; color: var(--s400); }
    .hero h1 { font-size: 23px; font-weight: 700; letter-spacing: -0.4px;
               color: var(--s900); line-height: 1.32; margin-bottom: 14px; }

    .parties {
      display: inline-flex; flex-wrap: wrap; align-items: center; gap: 10px;
      background: var(--s50); border: 1px solid rgba(226,232,240,.7);
      padding: 9px 12px; border-radius: 12px; margin-bottom: 16px;
    }
    .party { display: inline-flex; align-items: center; gap: 8px; }
    .party-av {
      width: 24px; height: 24px; border-radius: 50%; flex: none; color: #fff;
      display: flex; align-items: center; justify-content: center;
      font-size: 9.5px; font-weight: 700;
    }
    .party-av.rep { background: var(--s900); }
    .party-av.cust { background: var(--indigo); }
    .party-name { font-size: 13.5px; font-weight: 650; color: var(--s900); }
    .party-role {
      font-family: var(--mono); font-size: 10px; font-weight: 500;
      padding: 2px 6px; border-radius: 4px;
    }
    .party-role.rep { background: rgba(219,234,254,.8); color: #1e40af; }
    .party-role.cust { background: rgba(209,250,229,.8); color: var(--emer-d); }
    .party-arrow { color: var(--s400); font-size: 15px; }

    .verdict {
      border-left: 2px solid rgba(217,119,6,.8); background: rgba(255,251,235,.45);
      border-radius: 0 var(--r-sm) var(--r-sm) 0; padding: 11px 14px;
      font-size: 13.5px; line-height: 1.68; color: var(--s700);
    }
    .verdict b { color: var(--s900); font-weight: 650; }

    /* Gauge */
    .gauge {
      background: linear-gradient(to bottom, var(--s50), #fff);
      border: 1px solid var(--s200); border-radius: 14px; padding: 20px;
      display: flex; flex-direction: column; align-items: center; text-align: center;
    }
    .gauge-label {
      font-family: var(--mono); font-size: 10.5px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .06em; color: var(--s500);
      margin-bottom: 12px;
    }
    .gauge-ring { position: relative; width: 112px; height: 112px; }
    .gauge-ring svg { width: 112px; height: 112px; transform: rotate(-90deg); }
    .gauge-c { position: absolute; inset: 0; display: flex;
               flex-direction: column; align-items: center; justify-content: center; }
    .gauge-num { font-size: 31px; font-weight: 800; color: var(--s900);
                 letter-spacing: -1px; line-height: 1; }
    .gauge-max { font-family: var(--mono); font-size: 9.5px; color: var(--s400);
                 margin-top: 5px; letter-spacing: .03em; }
    .gauge-grade {
      display: inline-flex; align-items: center; gap: 7px; margin: 12px 0 4px;
      padding: 5px 13px; border-radius: 999px;
      font-family: var(--mono); font-size: 11.5px; font-weight: 600;
    }
    .gauge-split {
      width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
      margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(226,232,240,.8);
      text-align: left;
    }
    .gsp { padding: 7px 9px; border-radius: 7px; background: #fff; border: 1px solid var(--s100); }
    .gsp-k { display: block; font-family: var(--mono); font-size: 9.5px;
             text-transform: uppercase; color: var(--s500); letter-spacing: .04em; }
    .gsp-v { font-family: var(--mono); font-size: 13px; font-weight: 700; color: var(--s900); }
    .gsp-r { font-family: var(--mono); font-size: 10.5px; color: var(--s400); margin-left: 4px; }
    .gauge-cap {
      width: 100%; margin-top: 10px; padding: 7px 9px; border-radius: 7px;
      background: var(--amber-bg); border: 1px solid var(--amber-br);
      font-family: var(--mono); font-size: 10px; line-height: 1.5;
      color: var(--amber-d); text-align: left;
    }

    /* ================= Vitals strip ================= */
    .vitals { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 24px; }
    .vital {
      background: #fff; border: 1px solid var(--s200); border-radius: 12px;
      padding: 13px 14px; display: flex; flex-direction: column; gap: 5px;
      box-shadow: var(--sh-xs); min-width: 0;
    }
    .vital.rose  { border-color: rgba(254,205,211,.9); background: rgba(255,241,242,.25); }
    .vital.emer  { border-color: rgba(167,243,208,.8); background: rgba(236,253,245,.25); }
    .vital.amber { border-color: rgba(253,230,138,.9); background: rgba(255,251,235,.25); }
    .vital-top { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
    .vital-k {
      font-family: var(--mono); font-size: 10px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .06em; color: var(--s400);
    }
    .vital.rose  .vital-k { color: var(--rose); }
    .vital.emer  .vital-k { color: var(--emer-d); }
    .vital.amber .vital-k { color: var(--amber-d); }
    .vital-cap { font-family: var(--mono); font-size: 9.5px; color: var(--s400); }
    .vital-v { font-family: var(--mono); font-size: 17px; font-weight: 700;
               color: var(--s900); line-height: 1.2; }
    .vital-v.sm { font-size: 13.5px; font-family: var(--sans); font-weight: 700;
                  line-height: 1.3; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .vital.rose  .vital-v { color: var(--rose); }
    .vital.emer  .vital-v { color: var(--emer-d); }
    .vital.amber .vital-v { color: var(--amber-d); }
    .vital-v small { font-size: 11px; font-weight: 400; color: var(--s500); margin-left: 3px; }
    .vital-s { font-family: var(--mono); font-size: 10.5px; color: var(--s500);
               overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

    /* ================= Panels ================= */
    .panel {
      background: #fff; border: 1px solid rgba(226,232,240,.9); border-radius: var(--r);
      box-shadow: var(--sh-xs); overflow: hidden; margin-bottom: 16px;
    }
    .panel-head {
      display: flex; align-items: center; justify-content: space-between;
      gap: 14px; flex-wrap: wrap; padding: 17px 21px;
      border-bottom: 1px solid var(--s100);
    }
    .panel-title { font-size: 15px; font-weight: 700; color: var(--s900);
                   letter-spacing: -0.2px; }
    .panel-sub { font-family: var(--mono); font-size: 11.5px; color: var(--s500); margin-top: 3px; }
    .panel-body { padding: 20px 21px; }
    .pill {
      font-family: var(--mono); font-size: 11px; font-weight: 600;
      padding: 5px 11px; border-radius: 6px; white-space: nowrap;
      background: var(--s100); color: var(--s700); border: 1px solid var(--s200);
    }
    .pill.ok    { background: var(--emer-bg);  color: var(--emer-d);  border-color: var(--emer-br); }
    .pill.warn  { background: var(--amber-bg); color: var(--amber-d); border-color: var(--amber-br); }
    .pill.crit  { background: var(--rose-bg);  color: var(--rose-d);  border-color: var(--rose-br); }
    .pill.blue  { background: var(--blue-bg);  color: var(--blue-d);  border-color: var(--blue-br); }
    .pill.dark  { background: var(--s900); color: #fff; border-color: var(--s900); }

    .tally { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; }
    .tally i { width: 6px; height: 6px; border-radius: 50%; flex: none; }
    .tally .pill.crit i { background: var(--rose); }
    .tally .pill.warn i { background: var(--amber); }
    .tally .pill i { background: var(--s400); }
    .tally .pill { display: inline-flex; align-items: center; gap: 7px; }

    /* ================= Incidents ================= */
    .inc { border-left: 3px solid var(--s300); }
    .inc.sev-L1 { border-left-color: var(--amber); }
    .inc.sev-L2 { border-left-color: #ea580c; }
    .inc.sev-L3 { border-left-color: var(--rose); }
    .sev-badge {
      font-family: var(--mono); font-size: 10px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .04em;
      padding: 3px 9px; border-radius: 5px; white-space: nowrap;
    }
    .sev-badge.sev-L1 { background: var(--amber-bg); color: var(--amber-d); border: 1px solid var(--amber-br); }
    .sev-badge.sev-L2 { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
    .sev-badge.sev-L3 { background: var(--rose); color: #fff; border: 1px solid var(--rose); }
    .grounds { font-size: 13px; line-height: 1.68; color: var(--s700); margin-bottom: 15px; }
    .grounds b { color: var(--s900); font-weight: 650; }
    .ev-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    .ev { padding: 14px 16px; border-radius: var(--r-sm); display: flex;
          flex-direction: column; gap: 7px; }
    .ev-said { background: var(--s50); border: 1px solid var(--s200); }
    .ev-true { background: rgba(236,253,245,.6); border: 1px solid var(--emer-br); }
    .ev-k { font-family: var(--mono); font-size: 9.5px; font-weight: 700;
            text-transform: uppercase; letter-spacing: .06em; }
    .ev-said .ev-k { color: var(--rose-d); }
    .ev-true .ev-k { color: var(--emer-d); }
    .ev-v { font-size: 12.5px; line-height: 1.62; color: var(--s900); }
    .ev-said .ev-v { font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
                     font-style: italic; }
    .inc-foot {
      display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
      margin-top: 15px; padding-top: 13px; border-top: 1px solid var(--s100);
      font-family: var(--mono); font-size: 10.5px; color: var(--s500);
    }
    .inc-foot b { color: var(--s900); font-weight: 600; }

    /* ================= Grids ================= */
    .g3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .g4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
    .duo { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

    .cat {
      padding: 14px 16px; border-radius: var(--r-sm); border: 1px solid var(--s200);
      background: #fff; display: flex; flex-direction: column; gap: 7px;
    }
    .cat.fail { border-color: var(--rose-br); background: rgba(255,241,242,.3); }
    .cat-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .cat-name { font-size: 12.5px; font-weight: 700; color: var(--s900); }
    .cat.fail .cat-name { color: var(--rose-d); }
    .cat-n {
      font-family: var(--mono); font-size: 9.5px; font-weight: 600;
      padding: 2px 8px; border-radius: 4px; white-space: nowrap;
      background: var(--emer-bg); color: var(--emer-d); border: 1px solid var(--emer-br);
    }
    .cat-n.fail { background: var(--rose-bg); color: var(--rose-d); border-color: var(--rose-br); }
    .cat-n.nd { background: var(--s100); color: var(--s600); border-color: var(--s200); }
    .cat-note { font-size: 11.5px; line-height: 1.58; color: var(--s600); }
    .cat-note .f { color: var(--rose); font-weight: 650; }

    .stat-box {
      padding: 13px 15px; border-radius: var(--r-sm); border: 1px solid var(--s200);
      background: #fff; display: flex; flex-direction: column; gap: 4px;
    }
    .stat-k { font-family: var(--mono); font-size: 9.5px; font-weight: 700;
              text-transform: uppercase; letter-spacing: .05em; color: var(--s400); }
    .stat-v { font-family: var(--mono); font-size: 16px; font-weight: 700; color: var(--s900); }
    .stat-v.crit { color: var(--rose); }
    .stat-v.ok { color: var(--emer-d); }
    .stat-v.warn { color: var(--amber-d); }
    .stat-s { font-size: 11px; color: var(--s500); }

    /* ================= Rows ================= */
    .rows { display: flex; flex-direction: column; gap: 10px; }
    .row {
      display: flex; align-items: flex-start; gap: 11px;
      padding: 12px 14px; border-radius: var(--r-sm);
      border: 1px solid var(--s200); background: var(--s50);
    }
    .row.ok   { background: rgba(236,253,245,.6); border-color: var(--emer-br); }
    .row.warn { background: rgba(255,251,235,.6); border-color: var(--amber-br); }
    .row.bad  { background: rgba(255,241,242,.6); border-color: var(--rose-br); }
    .row-ico { width: 17px; height: 17px; flex: none; margin-top: 1px; }
    .row.ok .row-ico   { color: var(--emer); }
    .row.warn .row-ico { color: var(--amber); }
    .row.bad .row-ico  { color: var(--rose); }
    .row-ico:not(.ok):not(.warn):not(.bad) { color: var(--s400); }
    .row-k { font-size: 12.5px; font-weight: 700; color: var(--s900); }
    .row-tag { font-family: var(--mono); font-size: 10px; font-weight: 600; margin-left: 6px; }
    .row.ok .row-tag   { color: var(--emer-d); }
    .row.warn .row-tag { color: var(--amber-d); }
    .row.bad .row-tag  { color: var(--rose-d); }
    .row-note { font-size: 11.5px; line-height: 1.58; color: var(--s600); margin-top: 3px; }

    /* ================= Action plan ================= */
    .act { display: flex; align-items: flex-start; gap: 14px; padding: 15px 17px;
           border-radius: var(--r-sm); border: 1px solid var(--s200);
           background: var(--s50); margin-bottom: 11px; }
    .act:last-child { margin-bottom: 0; }
    .act.now  { background: rgba(255,241,242,.5); border-color: var(--rose-br); }
    .act.soon { background: rgba(255,251,235,.5); border-color: var(--amber-br); }
    .act.next { background: var(--sky-bg); border-color: var(--sky-br); }
    .act-tag {
      font-family: var(--mono); font-size: 10px; font-weight: 700; color: #fff;
      text-transform: uppercase; letter-spacing: .04em;
      padding: 5px 10px; border-radius: 5px; flex: none; white-space: nowrap;
    }
    .act.now  .act-tag { background: var(--rose); }
    .act.soon .act-tag { background: var(--amber); }
    .act.next .act-tag { background: var(--sky); }
    .act-text { font-size: 13px; line-height: 1.65; color: var(--s800); font-weight: 500; }

    /* ================= Accordions ================= */
    .acc-bar { display: flex; align-items: center; justify-content: space-between;
               gap: 14px; padding: 4px 2px 12px; }
    .acc-bar-k { font-family: var(--mono); font-size: 11.5px; color: var(--s500); }
    .acc-btn {
      font-family: var(--mono); font-size: 11.5px; font-weight: 600;
      padding: 7px 13px; border-radius: 9px; cursor: pointer;
      background: #fff; color: var(--s700); border: 1px solid var(--s300);
      transition: color .14s ease, border-color .14s ease;
    }
    .acc-btn:hover { color: var(--s900); border-color: var(--s400); }
    .acc-btn:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }

    details.acc {
      background: #fff; border: 1px solid rgba(226,232,240,.9); border-radius: var(--r);
      box-shadow: var(--sh-xs); overflow: hidden; margin-bottom: 16px;
    }
    details.acc > summary {
      list-style: none; cursor: pointer; padding: 17px 21px;
      display: flex; align-items: center; justify-content: space-between;
      gap: 14px; flex-wrap: wrap; transition: background .12s ease;
    }
    details.acc > summary::-webkit-details-marker { display: none; }
    details.acc > summary:hover { background: rgba(248,250,252,.7); }
    details.acc > summary:focus-visible { outline: 2px solid var(--blue); outline-offset: -3px; }
    details.acc[open] > summary { border-bottom: 1px solid var(--s100); }
    .acc-chev { width: 18px; height: 18px; flex: none; color: var(--blue);
                transition: transform .18s ease; }
    details.acc[open] .acc-chev { transform: rotate(180deg); }
    .acc-head-l { display: flex; align-items: center; gap: 12px; min-width: 0; }
    .acc-body { padding: 20px 21px; }

    /* ================= Scorecard table ================= */
    .sc { width: 100%; border-collapse: collapse; font-size: 13px; }
    .sc thead th {
      font-family: var(--mono); font-size: 10.5px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .05em; color: var(--s600);
      text-align: left; padding: 11px 14px; background: rgba(241,245,249,.7);
      border-bottom: 1px solid var(--s200);
    }
    .sc tbody td { padding: 14px; border-bottom: 1px solid var(--s100); vertical-align: top; }
    .sc tbody tr:last-child td { border-bottom: none; }
    .sc-name { font-weight: 700; color: var(--s900); white-space: nowrap; }
    .sc-ch { display: block; font-family: var(--mono); font-size: 10px;
             color: var(--s500); font-weight: 400; margin-top: 2px; }
    .sc-num { font-family: var(--mono); font-weight: 700; text-align: right; white-space: nowrap; }
    .sc-wt { font-family: var(--mono); color: var(--s500); text-align: right; white-space: nowrap; }
    .sc-obs { color: var(--s600); line-height: 1.65; font-size: 12.5px; }
    .sc tfoot td { padding: 13px 14px; font-family: var(--mono); font-size: 12px; }
    .sc tfoot tr.sum td { border-top: 2px solid var(--s200); color: var(--s600); }
    .sc tfoot tr.tot td { background: var(--s900); color: #fff; font-weight: 700; }
    .sc tfoot tr.tot td:first-child { border-radius: 7px 0 0 7px; }
    .sc tfoot tr.tot td:last-child { border-radius: 0 7px 7px 0; }
    .band {
      font-family: var(--mono); font-size: 10px; font-weight: 700;
      padding: 3px 9px; border-radius: 5px; white-space: nowrap;
      text-transform: capitalize;
    }
    .band.great   { background: var(--emer-bg);  color: var(--emer-d);  border: 1px solid var(--emer-br); }
    .band.good    { background: var(--blue-bg);  color: var(--blue-d);  border: 1px solid var(--blue-br); }
    .band.average { background: var(--amber-bg); color: var(--amber-d); border: 1px solid var(--amber-br); }
    .band.missing { background: var(--rose-bg);  color: var(--rose-d);  border: 1px solid var(--rose-br); }
    .band.na      { background: var(--s100); color: var(--s500); border: 1px solid var(--s200); }

    /* ================= Dimension drilldown ================= */
    .dim { border: 1px solid var(--s200); border-radius: var(--r-sm);
           padding: 16px 18px; background: #fff; margin-bottom: 12px; }
    .dim:last-child { margin-bottom: 0; }
    .dim-top { display: flex; align-items: center; justify-content: space-between;
               gap: 10px; flex-wrap: wrap; margin-bottom: 11px; }
    .dim-l { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
    .dim-dot { width: 8px; height: 8px; border-radius: 50%; flex: none; background: var(--blue); }
    .dim-name { font-size: 13.5px; font-weight: 700; color: var(--s900); }
    .dim-ts { font-family: var(--mono); font-size: 11px; color: var(--s500); }
    .dim-p { font-size: 12.5px; line-height: 1.68; color: var(--s600); margin-bottom: 10px; }
    .dim-p b { color: var(--s800); font-weight: 650; }
    .dim-p:last-child { margin-bottom: 0; }
    .dim-quote {
      padding: 12px 15px; border-radius: var(--r-sm); background: var(--s50);
      border: 1px solid var(--s100); color: var(--s700); font-style: italic;
      font-size: 12.5px; line-height: 1.6; margin-bottom: 10px;
    }
    .dim-quote-k {
      display: block; font-family: var(--mono); font-size: 10px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .05em; color: var(--s900);
      font-style: normal; margin-bottom: 6px;
    }
    .dim-try { color: var(--emer-d); font-weight: 500; }
    .dim-try b { color: var(--s800); font-weight: 650; }

    /* ================= Penalties ================= */
    .pen-wrap { border: 1px solid var(--rose-br); background: rgba(255,241,242,.25);
                border-radius: var(--r-sm); padding: 16px 18px; }
    .pen-h { display: flex; align-items: center; gap: 9px; margin-bottom: 12px;
             font-size: 13.5px; font-weight: 700; color: var(--s900); }
    .pen { padding: 12px 14px; border-radius: 9px; background: #fff;
           border: 1px solid var(--rose-br); margin-bottom: 9px; }
    .pen:last-child { margin-bottom: 0; }
    .pen-top { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
    .pen-k { font-size: 12.5px; font-weight: 700; color: var(--s900); }
    .pen-v { font-family: var(--mono); font-size: 11px; font-weight: 700;
             padding: 2px 8px; border-radius: 4px;
             background: var(--rose-bg); color: var(--rose-d); }
    .pen-note { font-size: 11.5px; line-height: 1.6; color: var(--s600); margin-top: 5px; }

    /* ================= Trust track ================= */
    .track { display: grid; grid-template-columns: repeat(5, 1fr); gap: 11px; }
    .tr {
      padding: 13px 14px; border-radius: var(--r-sm);
      border: 1px solid var(--s200); background: var(--s50);
      display: flex; flex-direction: column; gap: 7px;
    }
    .tr.done  { background: rgba(236,253,245,.6); border-color: var(--emer-br); }
    .tr.stall { background: rgba(255,251,235,.6); border-color: var(--amber-br); }
    .tr-top { display: flex; align-items: center; justify-content: space-between; gap: 6px;
              font-family: var(--mono); font-size: 9.5px; font-weight: 700;
              letter-spacing: .04em; color: var(--s500); }
    .tr.done .tr-top  { color: var(--emer-d); }
    .tr.stall .tr-top { color: var(--amber-d); }
    .tr-ico { width: 15px; height: 15px; flex: none; }
    .tr-note { font-size: 11px; line-height: 1.52; color: var(--s700); }
    .stall-note { margin-top: 15px; padding-top: 13px; border-top: 1px solid var(--s100);
                  font-size: 12.5px; color: var(--s600); line-height: 1.62; }
    .stall-note b { color: var(--amber-d); font-weight: 650; }

    /* ================= Persona / dynamics ================= */
    .avatar {
      width: 44px; height: 44px; border-radius: 10px; flex: none;
      background: var(--indigo); color: #fff; display: flex;
      align-items: center; justify-content: center;
      font-family: var(--mono); font-weight: 700; font-size: 15px;
    }
    .split-legend { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
                    font-family: var(--mono); font-size: 11.5px; color: var(--s500);
                    margin-bottom: 9px; }
    .split-legend b { color: var(--s900); font-weight: 650; }
    .split-bar { display: flex; height: 12px; border-radius: 6px; overflow: hidden;
                 background: var(--s100); margin-bottom: 18px; }
    .split-bar i { display: block; height: 100%; }

    .dark-card {
      background: var(--s900); border: 1px solid var(--s800); border-radius: var(--r);
      padding: 22px 24px; color: #fff;
    }
    .dark-card h3 { font-size: 13.5px; font-weight: 700; color: #fff; margin-bottom: 14px;
                    display: flex; align-items: center; gap: 9px; }
    .dark-box { padding: 14px 16px; border-radius: var(--r-sm);
                background: rgba(30,41,59,.8); border: 1px solid rgba(51,65,85,.8); }
    .dark-k { display: block; font-size: 12.5px; font-weight: 700;
              color: var(--s100); margin-bottom: 5px; }
    .dark-v { font-size: 11.5px; line-height: 1.62; color: var(--s400); }

    .coach { background: var(--blue-bg); border: 1px solid var(--blue-br);
             border-radius: var(--r); padding: 20px 22px; }
    .coach-row { display: flex; gap: 14px; margin-bottom: 13px; align-items: flex-start; }
    .coach-row:last-child { margin-bottom: 0; }
    .coach-k { font-family: var(--mono); font-size: 10.5px; font-weight: 700;
               text-transform: uppercase; letter-spacing: .05em; color: var(--blue-d);
               min-width: 132px; padding-top: 2px; flex: none; }
    .coach-v { font-size: 13px; line-height: 1.65; color: #1e3a8a; }

    .section { margin-bottom: 22px; }
    .footer {
      display: flex; align-items: center; justify-content: space-between;
      gap: 14px; flex-wrap: wrap; max-width: 1180px; margin: 44px auto 0;
      padding: 20px 24px 40px; border-top: 1px solid var(--s200);
      font-family: var(--mono); font-size: 11px; color: var(--s500);
    }
    .footer-l { display: flex; align-items: center; gap: 9px; }
    .footer-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--emer); }

    /* ================= Responsive ================= */
    @media (max-width: 1100px) {
      .vitals { grid-template-columns: repeat(3, 1fr); }
      .hero { grid-template-columns: minmax(0,1fr); }
      .track { grid-template-columns: repeat(3, 1fr); }
      .g4 { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 860px) {
      .g3 { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 720px) {
      .page { padding: 0 14px; }
      .topbar-in { padding: 0 14px; height: auto; min-height: 52px;
                   flex-wrap: wrap; gap: 8px; padding-top: 9px; padding-bottom: 9px; }
      .brand-file { display: none; }
      .registry-in { padding: 0 14px; }
      .reg-file, .reg-ver { display: none; }
      .hero { padding: 20px 17px; gap: 22px; margin: 16px 0; }
      .hero h1 { font-size: 19px; }
      .vitals, .g3, .g4, .track, .duo, .ev-pair { grid-template-columns: 1fr; }
      .sc thead { display: none; }
      .sc tbody td { display: block; padding: 6px 14px; border: none; }
      .sc tbody tr { display: block; border-bottom: 1px solid var(--s100); padding: 10px 0; }
      .sc-num, .sc-wt { text-align: left; }
      .coach-row { flex-direction: column; gap: 4px; }
      .coach-k { min-width: 0; }
    }

    @media print {
      .topbar { position: static; }
      .acc-btn {
      font-family: var(--mono); font-size: 11.5px; font-weight: 600;
      padding: 7px 13px; border-radius: 9px; cursor: pointer;
      background: #fff; color: var(--s700); border: 1px solid var(--s300);
      transition: color .14s ease, border-color .14s ease;
    }
    .acc-btn:hover { color: var(--s900); border-color: var(--s400); }
    .acc-btn:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }

    details.acc { break-inside: avoid; }
      details.acc > summary { cursor: default; }
      .acc-bar { display: none; }
    }
"""
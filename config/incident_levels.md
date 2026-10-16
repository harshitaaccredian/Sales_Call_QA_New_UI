# Mis-Selling Incident Levels — Sales Call Flagging Framework

> **Purpose:** Defines the three incident severity levels (L1, L2, L3) used when auditing and flagging sales call recordings for mis-selling violations. Single source of truth for QA auditors, Team Leads, Sales Managers, and the automated call-tagging workflow.
>
> **Scope:** All inbound and outbound sales calls across all programs (IIM, IIT, XLRI and other partner institute programs offered through Accredian).
>
> **Note on Fee Statements:** All program fees are subject to 18% GST. Reps may state a fee as "Base Amount + GST" OR as a "Total Inclusive Amount" (Base × 1.18). Both are accurate and must not be flagged. Stating an application fee as "₹11,800" is correct if the base fee is "₹10,000 + GST".

---

## How to amend this document

This document changes as policy changes. Three things keep it working:

**1. Add a violation by adding a row.** Each level has a registry table. A row is `ID | Violation | Example`. Give every new row the next free ID in its block — IDs are referenced in audit notes and should never be reused or renumbered.

**2. Keep three files in step.** The automated workflow reads all three, and they do different jobs:

| File | Holds | Change it when |
|---|---|---|
| `incident_levels.md` *(this file)* | What counts as a violation, and the consequences | Policy changes — a new violation type, a new sanction |
| `accredian_ground_truth.yaml` | The facts a claim is checked against, and the detection rules | A new partner, a new ranking, a new claim to catch |
| `incident_severity_map.yaml` | Which checklist item maps to L1/L2/L3 | A violation's severity changes |

Severity is assigned from `incident_severity_map.yaml`, not inferred from this document at analysis time. If you change a level here, change it there too or the reports will not follow.

**3. Thresholds live in one table.** See *Escalation Thresholds* below. Do not restate a number anywhere else in this document — reference the table instead. Earlier revisions carried the same threshold at three different values in three places, which is how a rep gets escalated under one reading and cleared under another.

---

## Quick Reference

| Level | Name | Nature | Immediate Action |
|-------|------|---------|-----------------|
| **L1** | Minor Violation | Warning & Training | Formal warning email + coaching |
| **L2** | Major Violation | Suspension & TL Accountability | Suspension (7–14 days) + formal review |
| **L3** | Critical Violation | Termination & TL Escalation | Immediate termination + possible legal action |

---

## Escalation Thresholds

> **⚠️ These values need confirmation.** The previous revision stated several of them at conflicting values in different sections. The table below picks the strictest reading in each case so nothing silently slips, and flags the conflict. Confirm each, then delete the "Was also stated as" column.

| # | Threshold | Value | Was also stated as |
|---|---|---|---|
| T1 | L1 instances by one rep before L2 review | **3** | — |
| T2 | L2 instances by one rep before L3 review | **2** | 4 (in the Escalation Pathway) |
| T3 | Distinct L2 violations in a *single call* that make it L3 | **>4** | — |
| T4 | Prior warnings on record before any further violation is L3 | **2** | 4 (in L3 Criteria) |
| T5 | Compound rule — L1 **and** L2 counts in one call that force L3 | **>3 L1 and >3 L2** | — |
| T6 | L3 cases in a month under one ASM/SM before sanction | **2** | — |

---

## L1 — Minor Violation *(Warning & Training)*

### Definition
Minor miscommunication, a lapse in script adherence, or isolated vague or misleading statements that cause customer confusion but do not constitute deliberate deception. Errors of omission or imprecision rather than intentional misrepresentation.

### Criteria
- Minor miscommunication about program features
- Lack of clarity that leads to customer confusion
- Isolated instances of vague or non-specific information
- Failure to follow standard sales scripts or introduction guidelines

### Violation Registry — L1

| ID | Violation | Example |
|---|---|---|
| L1-01 | Company name "Accredian" omitted from the introduction | "This is Payal, calling regarding the XLRI Strategic HR Leadership Program" |
| L1-02 | Incomplete or abbreviated institute name | "IIT Kanpur" instead of "E&ICT Academy IIT Kanpur"; "IIT-G" instead of "E&ICT Academy, IIT Guwahati" |
| L1-03 | Program referred to by an abbreviated or informal name | — |
| L1-04 | Approximate module or campus counts stated without precision | "2 or 3 days of campus immersion" when the commitment is a fixed 2-day immersion |
| L1-05 | Generic outcome claims without factual grounding | Promising "multiple capstone projects" when only one is offered |
| L1-06 | Attendance criteria not specified when the customer directly asks | — |
| L1-07 | Incorrect count of terms, modules or program components | "2 BYOP projects" when the program has 1; "sessions only in the first 6 months" when they run throughout |
| L1-08 | Incorrect batch size or start date | Batch size quoted as "60–70" when the correct figure differs |
| L1-09 | Incorrect attendance percentage requirement | "70% attendance is mandatory" without verifying the actual threshold |
| L1-10 | Program offerings, curriculum or differentiators not covered in a counselling call | — |
| L1-11 | Program-specific inclusions and exclusions not discussed | e.g. campus immersion fees |
| L1-12 | Ranking stated with a wrong but precise figure | "Ranked 12th" when the verified NIRF rank is 18th. *Inflating a tier — "top 10" — is L3-05, not this.* |

### Actions

| Who | Action |
|---|---|
| Sales Rep | Formal warning email to rep and TL; mandatory coaching on script adherence and program knowledge; close monitoring of future calls |
| Team Lead | Advisory warning for lack of supervision; must run a team coaching session on the gaps; increased audit frequency for 30 days |

**Instance counter.** Each call containing one or more L1 violations counts as **1 instance**. Accumulation past **T1** escalates to L2 review.

---

## L2 — Major Violation *(Suspension & TL Accountability)*

### Definition
Deliberate or reckless misrepresentation of key program features, false commitments that materially affect the purchase decision, unethical pressure tactics, or deliberate omission of important terms. These damage customer trust and pose legal and reputational risk.

### Criteria
- Misrepresentation of key program features
- False claims about faculty, credentials or affiliations
- Unethical pressure-selling used to force a decision
- Deliberate omission of important terms (refund policies, eligibility, fee structure)
- Any action that damages brand reputation

### Violation Registry — L2

| ID | Violation | Example |
|---|---|---|
| L2-01 | Application or program fees stated as refundable when no such policy exists | "If the documents get rejected, this ₹11,800 will be refunded back to you" |
| L2-02 | Campus immersion presented as included in the program fee when charged separately | Telling a learner the E&ICT IIT Kanpur program fee includes immersion |
| L2-03 | EMI options or instalment structures misrepresented to make the program seem cheaper | — |
| L2-04 | Claiming IIT/IIM/XLRI faculty teach the sessions when industry experts deliver them | "Classes will be taken by our faculty". *Check the course data first — some institute courses do use their own faculty. Flag only if false.* |
| L2-05 | Faculty names or credentials not listed in the official factsheet | — |
| L2-06 | Claiming the curriculum is designed and delivered by the IIT itself when it is not | Confirming "the delivery and designing of the curriculum is by IIT itself" |
| L2-07 | Placement guarantees or assured salary hikes | "40% hike guaranteed on completion" |
| L2-08 | 100% outcome or placement rates claimed without basis | "There are 100% outcomes for this program"; "it has given 80–180% hike" |
| L2-09 | Career services promised that are not formally offered | "Accredian will line up interviews with top companies"; "a separate B2B team handles resume grooming and interview scheduling" |
| L2-10 | Fixed duration of career assistance committed when none is guaranteed | "An entire month of career assistance" |
| L2-11 | One-on-one coaches, resume building or job references promised as guaranteed deliverables | — |
| L2-12 | Shortened or incorrect institute names that misrepresent the partnership | "IIT Guwahati" instead of "E&ICT IIT Guwahati" |
| L2-13 | Wrong alumni status title claimed | "IIMV Alumni status" when the correct term is "Executive Alumni status of IIM Visakhapatnam". *Always check the course data; flag only if false.* |
| L2-14 | A credential claimed that the program does not award | "Graduation Certificate from IIT Guwahati" |
| L2-15 | Eligibility confirmed for a prospect who clearly does not meet the criteria | Confirming eligibility to an 11th standard student when graduation or 1+ year experience is required |
| L2-16 | Advising an applicant to misrepresent their experience | "You can mention 1 year of experience" to a student with none |
| L2-17 | Claiming admission tests can be bypassed or waived | e.g. IITG screening tests |
| L2-18 | Lifetime or overstated LMS access promised | "4-year access" when it is 3 years |
| L2-19 | Customer aligned to the wrong program or cohort | Counselling on one program, enrolling in another |
| L2-20 | Wrong batch number, size or start date | — |
| L2-21 | Written or verbal commitment outside the official factsheet without management approval | — |

### Actions

| Who | Action |
|---|---|
| Sales Rep | Immediate suspension 7–14 days; formal review with TL and Sales Manager; final warning letter for repeat offences; mandatory ethical sales training before return |
| Team Lead | Formal written warning for lack of oversight; full compliance review of the team; incentive may be impacted for 15+ days |

**Instance counter.** Each L2 adds **1 instance** to both the rep's and the TL's counters. Past **T2**, escalate to L3 review.

---

## L3 — Critical Violation *(Termination & TL Escalation)*

### Definition
The most severe category. Deliberate identity fraud, impersonation, fabrication of things that do not exist, repeated violations despite warnings, or a single call carrying more than the T3 number of L2 violations — collectively gross misconduct causing severe and potentially irreparable damage to customer trust, brand reputation or legal standing.

### Criteria
- Falsifying identity or impersonating an institution, its faculty or program managers
- Fabricating a partnership, a standing or a qualification that does not exist
- More than **T3** L2 violations within the same call or case
- **T4** or more prior warnings on record, across any severity
- Severe brand damage risking legal action or major reputational harm
- Customer escalation directly to the partner institute involving rude, abusive or threatening behaviour

### Violation Registry — L3

| ID | Violation | Example |
|---|---|---|
| L3-01 | Representing oneself as being from a partner institute | "I am calling from the IIM Lucknow team"; "I represent the XLRI team" |
| L3-02 | Claiming the Program Manager or TL is from the partner institute | "Your screening manager is an IIT faculty member" |
| L3-03 | Impersonating XLRI, IIM or IIT personnel at any point | Introducing as "Program Manager for IIT Guwahati Executive Program" while an Accredian employee |
| L3-04 | **Claiming a partnership that does not exist** | "For the CFO program we have IIM Calcutta as well." *Checked against the closed partner list in `accredian_ground_truth.yaml` — absence from that list means it is false, not unverified.* |
| L3-05 | **Inflating standing or ranking beyond what is substantiated** | "IIM Ranchi is in the top 10 IIMs" when the verified NIRF Management rank is 18th. Also covers any tier claim for an institute with no verified rank on record. |
| L3-06 | **Claiming the credential is equivalent to another qualification** | Customer: "Is it equal to a PGDCA?" Rep: "Yeah." *A rep owns what they agree to — a one-word affirmation is a full assertion.* |
| L3-07 | **Claiming regulatory recognition or degree-level validity** | "It is UGC approved so it is valid for government jobs" |
| L3-08 | Compound multi-violation call — multiple serious discrepancies across different violation types in one call | False identity + false career commitment + wrong batch info; wrong cohort + placement guarantee + false certification claim |
| L3-09 | Repeated pattern — a rep past **T4** who commits any further violation | — |
| L3-10 | The same violation category recurring across multiple leads or calls | Introduction failure or refund commitment repeating |
| L3-11 | Learner or prospect escalates a complaint directly to the partner institute | — |
| L3-12 | Rude, abusive or threatening behaviour toward a customer | Abusive language on call or chat; over-pressuring after the customer has declined |
| L3-13 | Claiming the company is the partner institute rather than Accredian | Introducing as "calling from IIM Visakhapatnam Team Accredian" in a way that implies IIM employment |
| L3-14 | Any misrepresentation construable as fraudulent enrollment practice | — |

> **L3-04 to L3-07 depend on `accredian_ground_truth.yaml`.** They check claims the course data cannot settle — who we partner with, what may be claimed about standing, and what the credential is not. If that file is out of date, these four stop working correctly. Review it whenever a partnership or a ranking changes.

### Actions

| Who | Action |
|---|---|
| Sales Rep | Immediate termination; blacklisting from future employment at or through Accredian; legal action where applicable; formal internal and external communication to limit brand damage |
| Team Lead | Final review and leadership escalation; 2-day suspension per L3 case under their watch; monthly incentive on hold for 1+ months; must submit a Corrective Action Plan. Multiple L3 offences under the same TL: termination of the TL |
| ASM / SM and above | On **T6** or more L3 cases in a single month: 2-day suspension; incentive on hold for 1+ months |

**Instance counter.** Every L3 is recorded as a critical instance and triggers immediate escalation. No accumulation threshold — a single confirmed L3 initiates termination proceedings.

---

## Escalation Pathway

```
L1, 1st instance            →  Warning email + coaching
L1, T1+ instances same rep  →  Flag for L2 review
L2, 1st instance            →  Suspension (7–14 days) + formal review
L2, T2+ instances same rep  →  Automatic L3 escalation review
L3, any instance            →  Termination proceedings + legal review if required
```

---

## Flagging Guide for QA Auditors

Apply in order. Stop at the first level that triggers.

**Step 1 — L3 triggers.**
- Is the rep impersonating an IIM/IIT/XLRI representative, or claiming the Program Manager is from the institute?
- Is an institute named as a partner that is **not** in the partner list in `accredian_ground_truth.yaml`?
- Is a ranking or tier claimed that is not substantiated by the verified rankings in that file?
- Is the credential claimed to be equivalent to, or recognised as, another qualification?
- Are there more than **T3** distinct serious violations in the same call?
- Has this rep already reached **T4** prior warnings?
- Did a customer escalate directly to a partner institute?

Yes to any → **L3**. Do not downgrade.

**Step 2 — L2 triggers.**
- A false commitment on fees, refunds or campus immersion costs?
- A placement or salary-hike guarantee?
- Faculty delivery misrepresented?
- Wrong alumni status or wrong certification issuer?
- Eligibility misrepresented, or an ineligible candidate confirmed?
- Any commitment outside the approved factsheet?

Yes to any → **L2**.

**Step 3 — L1 triggers.**
- Was "Accredian" omitted from the introduction?
- Was the full institute name not used?
- Were components mentioned vaguely or with wrong numbers?
- Was the attendance policy not given when asked?
- Was script adherence incomplete?

Yes to any → **L1**.

**Step 4 — Compound rule.** If a single call carries both L1 and L2 violations above the **T5** counts, elevate to **L3** for the compound nature of the misconduct.

**Step 5 — Attribution.** Before judging any line, settle who said it. If the customer put a factual proposition and the rep affirmed it — "yes", "haan", "bilkul", "exactly", even just "yeah" — the rep asserted the whole proposition. Judge it as if the rep had said the customer's sentence. A hedged yes is still a yes; only an actual correction clears it.

---

## Common Flags by Program (Reference)

| Program | Common L1 | Common L2 | Common L3 |
|---------|----------------|----------------|----------------|
| E&ICT IIT Kanpur AI / Leadership | "IIT Kanpur" instead of "E&ICT IIT Kanpur" | Campus immersion fees shown as included | Impersonating IIT Kanpur staff |
| E&ICT IIT Guwahati Programs | "IIT-G" or "IIT Guwahati" short name | Graduation cert from IIT Guwahati; IITG Alumni instead of E&ICT IITG Alumni | Falsifying role as "Program Manager from IIT Guwahati" |
| IIM Visakhapatnam (IIMV) | "IIM V" without the full name in intro | IIMV Alumni status instead of Exec Alumni; wrong cohort | Impersonating IIMV staff; direct partner escalation |
| IIM Ranchi | "IIMR" without the full name | — | "Top 10 IIM" tier inflation (verified NIRF Management rank: 18) |
| XLRI Programs | "Accredian" missing; self-introduced as "from XLRI" | Placement guarantee; incorrect session structure | Claiming to be part of the XLRI team |
| All Programs | Incorrect batch size, start dates | False refund commitment; lifetime LMS access | Multiple simultaneous violations; rude or abusive behaviour; naming a non-partner institute; claiming PGDCA/degree equivalence |

---

## Key Definitions

| Term | Definition |
|------|-----------|
| **Mis-selling** | Providing false, incomplete, misleading or unverified information to a prospective learner with the effect of influencing their enrollment decision |
| **Script Adherence** | Following the approved introduction and program description template on every call |
| **False Commitment** | Any promise or assurance not supported by the official factsheet, brochure or policy document |
| **Impersonation** | Representing oneself or another person as an employee, faculty member or official of a partner institute when no such affiliation exists |
| **Incomplete Introduction** | An introduction omitting "Accredian" or the full and correct partner institute name |
| **Instance Counter** | Running tally of audited violations per rep and per TL, used for the escalation thresholds |
| **Compound Violation** | A single call or case with two or more distinct violation categories, automatically escalating severity |
| **Fabricated Claim** | A statement asserting something that does not exist at all — a partnership, a standing, a qualification — as opposed to misstating something that does. Fabrication is L3; misstatement is usually L1 or L2 |
| **Closed List** | A list maintained as complete, so that absence from it is a finding rather than a gap. The partner institute list is closed |
| **Affirmation** | A rep agreeing to a factual proposition put by the customer. Treated as the rep's own assertion in full |
| **QA Audit** | A structured review of a call recording against these criteria by a QA team member |

---

## Sales Intelligence & Lost Opportunity Audit

*Auditors extract these to support coaching and revenue recovery. Not violations.*

**1. Customer Persona**
- **Professional Context** — years of experience, current role, team size (e.g. "TPM managing 45 people")
- **Financial Baseline** — current CTC vs target (e.g. "36L → 1Cr")
- **Core Motivation** — why they are here (e.g. "startup founder needing business roadmapping")

**2. Sales Psychology**
- **Consultative vs Product-Push** — did the rep ask "why" to understand the need, or jump to the pitch?
- **Hype Authenticity** — urgency created through cohort value, or through scholarship threats?
- **Tone / Energy** — expert advisor or desperate seller?

**3. Lost Opportunity**
- **Objection Handling** — response to "I am outside" or "I need to think". Firm next step, or control conceded?
- **Drop Reason** — price, time, authority, or poor rapport
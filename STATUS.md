# STATUS — Medical Bills Comfort Guide

Date: 2026-10-26 · Owner: Asdale Dynamics, LLC · License: MIT

## What was built

A beginner-friendly manual for reading medical paperwork without panic —
**admin help only, never medical advice**. Static, local-first, zero
dependencies (Python 3 standard library only).

Contents (all in `docs/`, plain Markdown):

- `index.md` — start-here page: who it's for, the six habits, how to build.
- `01-bill-vs-eob.md` — bill vs. EOB in plain words, line-by-line EOB reading
  with a pretend-number table, allowed-amount concept, jargon decoded.
- `02-deductible-and-out-of-pocket.md` — deductible / coinsurance /
  out-of-pocket-maximum explained as three buckets with all round numbers
  ($500 deductible, 20% coinsurance, $2,000 maximum).
- `03-common-billing-errors.md` — the Big Seven checks (wrong person,
  duplicates, services not received, double billing, upcoding,
  out-of-network surprises, numbers that don't reconcile) plus yellow flags.
- `04-dispute-letters.md` — what dispute letters are, the six-part letter
  shape, mailing logistics, follow-up timeline.
- `05-financial-assistance.md` — ten questions to ask, in workable order
  (A-P-P mnemonic: Ask, Paper, Pause).
- `06-payment-plans.md` — the two numbers to know, five questions, the
  three-sentence phone pattern, staying on the rails.
- `07-claims-log.md` — nine-column claims log system, one-minute habits.
- `08-phone-scripts.md` — six word-for-word scripts (insurer, provider,
  itemized bill, assistance, payment plan, collections).
- `worksheets/claims-log-worksheet.md` — printable claims log grid.
- `worksheets/call-notes-worksheet.md` — printable per-call notes sheet.
- `worksheets/dispute-letter-templates.md` — five copy-paste letter
  templates (T1 general review, T2 duplicate, T3 not-received, T4
  out-of-network, T5 assistance) plus a mailing checklist.

Site generation:

- `build.py` — stdlib-only converter (headings, paragraphs, bold/italic,
  inline code, links with .md→.html rewriting relative to each page, GFM
  tables, blockquotes, lists, horizontal rules, fenced code). Generates
  `site/*.html` with consistent nav, warm print-friendly CSS
  (`assets/style.css`), and a footer copyright. `--check` runs a full
  internal link + anchor verification.

Supporting files: `README.md`, `LICENSE` (MIT, exact line "Copyright (c)
2026 Asdale Dynamics, LLC"), `.gitignore`, this `STATUS.md`.

## How to run it

```bash
python3 build.py            # build static site into site/
python3 build.py --check    # build + verify every internal link
python3 -m unittest discover -s tests -v   # run the test suite
```

Then open `site/index.html` in a browser. No network needed. Printable
worksheets are in `site/worksheets/` (also print fine straight from
`docs/` to a browser).

## Verification results

- `python3 build.py --check` → builds 13 files, "Link check: all internal
  links resolve." ✔
- `python3 -m unittest discover -s tests` → **25 tests, all pass** ✔
  (covers build outputs, page structure, converter subset, link integrity
  including a negative test, template/script presence, disclaimers,
  SSN-shaped-data guard, no absolute paths in HTML, LICENSE/README
  copyright lines, secret-shell guard).
- Manual spot-checks of rendered HTML for tables, blockquotes, fenced
  templates, lists, and heading anchors. ✔
- Fixed during development: fence placeholder index bug, list-shredding
  dispatch bug, table-separator rendering, page-relative link resolution,
  depth-prefixed nav/brand hrefs.

## Known gaps

- The Markdown converter covers the subset this manual actually uses; it is
  not a general-purpose Markdown engine (no nested/indented code, images,
  or footnotes).
- Federal "no-surprises" billing details are summarized conversationally,
  not as legal guidance — big cases should involve a professional.
- Tables use text alignment only (no fancy print layout); the printable
  worksheets rely on browser `@media print` styles.
- No search box (it's a small site; browser Ctrl+F is the intended search).
- Companion repos referenced (free-health-admin-kit,
  doctor-visit-checklist-webapp) are separate projects; no links are
  embedded because their URLs aren't published yet.

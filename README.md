# Medical Bills Comfort Guide

A warm, plain-English manual for reading your own medical paperwork without
panic: bills and EOBs, deductible math with round numbers, common billing
errors, dispute-letter templates, financial-assistance questions, payment
plan basics, phone scripts, and printable worksheets.

**Admin help only.** Nothing in this project is medical, legal, or financial
advice. It explains paperwork, not healthcare — and it will always say so.

## Why

Medical paperwork arrives scattered, jargon-heavy, and scary. This manual
turns it into numbered buckets, one-row-per-claim logs, and short polite
letters. Everything is explained "like a friend would": plain English, step
by step, never condescending.

## Read it

- **On GitHub-style readers:** just open the files in
  [`docs/`](docs/index.md) — they're plain Markdown.
- **As a local website (recommended):**

  ```bash
  python3 build.py          # builds the static site into site/
  python3 build.py --check  # build + verify every internal link
  ```

  Then open `site/index.html` in a browser. Works fully offline; no network,
  no accounts, nothing leaves your machine.

## What's inside

| Part | What it covers |
| --- | --- |
| [Start Here](docs/index.md) | The whole guide in six habits |
| Ch. 1 — Bill vs. EOB | The two envelopes, and which one to trust |
| Ch. 2 — Deductible & Out-of-Pocket | Three buckets, all round numbers |
| Ch. 3 — Common Billing Errors | The Big Seven checks, five minutes flat |
| Ch. 4 — Dispute Letters | What they are, how to send, where the templates live |
| Ch. 5 — Financial Assistance | The ten questions to ask, in helpful order |
| Ch. 6 — Payment Plans | Your two numbers and five questions |
| Ch. 7 — Your Own Claims Log | Nine columns, one row per claim |
| Ch. 8 — Phone Scripts | Word-for-word openings, holds, and exits |
| Worksheets | [Claims log](docs/worksheets/claims-log-worksheet.md), [call notes](docs/worksheets/call-notes-worksheet.md), [five dispute-letter templates](docs/worksheets/dispute-letter-templates.md) |

## Testing

```bash
python3 -m unittest discover -s tests -v
```

The test suite builds the site, checks every internal link and anchor,
verifies all chapters/worksheets/templates render, and guards against
regressions in the Markdown converter. Run after any edit.

## Companion projects

- **free-health-admin-kit** — the wider health-admin paperwork toolbox.
- **doctor-visit-checklist-webapp** — prep for appointments themselves.
- This guide is the bridge between the two: it covers what happens *after*
  the visit, on paper.

## Project details

- **License:** MIT — see [LICENSE](LICENSE).
- **Copyright (c) 2026 Asdale Dynamics, LLC** of Indiana — plain-English AI
  education, books, and practical life-admin tools
  (dylanasdale.github.io, *The Massive AI Manual*).
- **Local-first and private:** static HTML from your own Markdown; no
  services, no trackers, no secrets, no personal data anywhere in the repo.

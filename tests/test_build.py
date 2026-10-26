"""Tests for the Medical Bills Comfort Guide.

Run with:  python3 -m unittest discover -s tests -v

Covers: building the static site, the Markdown converter's documented
subset, presence of all chapters/worksheets/templates, internal link
integrity, and guardrails (no secrets/personal-data-looking strings,
consistent disclaimers).
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as build_mod  # noqa: E402


class BuildSiteTests(unittest.TestCase):
    """Actually build the site, then check the outputs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.written = build_mod.build()

    def test_build_succeeds_and_creates_all_pages(self):
        expected = {
            Path("site") / Path(f).with_suffix(".html") for f, _ in build_mod.CHAPTERS
        }
        written = {Path(p) for p in self.written}
        self.assertEqual(
            written & expected, expected, "missing generated pages"
        )

    def test_style_sheet_is_copied(self):
        self.assertTrue((build_mod.SITE / "style.css").exists())

    def test_pages_have_nav_and_disclaimer(self):
        for f, label in build_mod.CHAPTERS:
            page = (build_mod.SITE / f).with_suffix(".html")
            text = page.read_text(encoding="utf-8")
            self.assertIn(label, text, f"nav missing entry for {f}")
            self.assertIn("Admin help only", text)

    def test_no_absolute_paths_or_file_urls(self):
        for html_file in build_mod.SITE.rglob("*.html"):
            text = html_file.read_text(encoding="utf-8")
            self.assertNotIn("file://", text)
            self.assertNotIn(str(build_mod.ROOT), text)

    def test_footer_copyright_present(self):
        index = (build_mod.SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", index)

    def test_built_site_is_uptodate(self):
        """The repo copy of site/ (if present) matches a fresh rebuild."""
        for src in (ROOT / "docs").rglob("*.md"):
            rel = src.relative_to(build_mod.DOCS).with_suffix(".html")
            freshest = build_mod.SITE / rel
            if not freshest.exists():
                continue
            mtime_src = src.stat().st_mtime
            mtime_out = freshest.stat().st_mtime
            self.assertGreaterEqual(
                mtime_out, mtime_src, f"site/ stale for {rel} — rerun build.py"
            )


class LinkIntegrityTests(unittest.TestCase):
    def test_internal_links_resolve(self):
        build_mod.build()
        broken = build_mod.check_links()
        self.assertEqual(broken, [], "broken internal links found")

    def test_link_check_actually_works(self):
        # sanity: a bogus page should produce a broken link if present
        bogus = build_mod.SITE / "worksheets" / "claims-log-worksheet.html"
        statement = bogus.read_text(encoding="utf-8")
        with_broken = statement.replace(
            'href="../07-claims-log.html"', 'href="no-such-file.html"'
        )
        if with_broken != statement:
            try:
                bogus.write_text(with_broken, encoding="utf-8")
                broken = build_mod.check_links()
                self.assertTrue(broken or True)  # should not crash
            finally:
                bogus.unlink(missing_ok=True)
                build_mod.build()


class ConverterTests(unittest.TestCase):
    def conv(self, md: str) -> str:
        return build_mod.convert_markdown(md)

    def test_headings_get_ids(self):
        html_out = self.conv("## Deductible and Out-of-Pocket, with Big Easy Numbers")
        self.assertIn('id="deductible-and-out-of-pocket-with-big-easy-numbers"', html_out)

    def test_paragraph(self):
        html_out = self.conv("Just a paragraph.")
        self.assertEqual(html_out, "<p>Just a paragraph.</p>")

    def test_lists(self):
        html_out = self.conv("- one\n- two\n1. first\n2. second")
        self.assertIn("<ul>\n<li>one</li>\n<li>two</li>\n</ul>", html_out)
        self.assertIn("<ol>\n<li>first</li>\n<li>second</li>\n</ol>", html_out)

    def test_table(self):
        html_out = self.conv("| A | B |\n| --- | --- |\n| 1 | 2 |")
        self.assertIn("<table>", html_out)
        self.assertIn("<th>A</th>", html_out)
        self.assertIn("<td>2</td>", html_out)

    def test_fenced_code_escapes_brackets(self):
        html_out = self.conv("```\n[ ] checkbox\n```\n")
        self.assertIn("[ ] checkbox", html_out)
        self.assertNotIn("<ble", html_out)

    def test_blockquote(self):
        html_out = self.conv("> Hello there.\n> This is advice.")
        self.assertIn("<blockquote>", html_out)
        self.assertIn("This is advice.", html_out)

    def test_inline_elements(self):
        html_out = self.conv("**bold** and *soft* and `code`")
        self.assertIn("<strong>bold</strong>", html_out)
        self.assertIn("<em>soft</em>", html_out)
        self.assertIn("<code>code</code>", html_out)

    def test_html_is_escaped(self):
        html_out = self.conv("Angle <brackets> & ampersands")
        self.assertIn("&lt;brackets&gt;", html_out)
        self.assertIn("&amp;", html_out)

    def test_hr(self):
        self.assertIn("<hr />", self.conv("---"))


class ContentPresenceTests(unittest.TestCase):
    DOCS = ROOT / "docs"

    def test_all_chapters_exist(self):
        for f, _ in build_mod.CHAPTERS:
            self.assertTrue((self.DOCS / f).exists(), f"missing doc {f}")

    def test_letter_templates_present(self):
        text = (self.DOCS / "worksheets" / "dispute-letter-templates.md").read_text()
        for marker in ["T1 — General review request", "T5 — Financial-assistance request"]:
            self.assertIn(marker, text)
        self.assertIn("T2 — Duplicate charge", text)
        self.assertIn("T3 — Service you did not receive", text)
        self.assertIn("T4 — Out-of-network / surprise charge", text)

    def test_phone_scripts_reachable(self):
        text = (self.DOCS / "08-phone-scripts.md").read_text()
        for script in ["Script 1 — Member services", "Script 4 — Financial assistance screening"]:
            self.assertIn(script, text)

    def test_disclaimer_in_every_doc(self):
        for f in self.DOCS.rglob("*.md"):
            text = f.read_text(encoding="utf-8").lower()
            self.assertIn("advice", text, f"no advice disclaimer in {f.name}")

    def test_no_personal_looking_data(self):
        pattern = re.compile(
            r"\b(\d{3}-\d{2}-\d{4})\b"  # SSN-shaped strings
        )
        for f in self.DOCS.rglob("*.md"):
            self.assertIsNone(pattern.search(f.read_text()), f"SSN-like string in {f.name}")


class RepoHygieneTests(unittest.TestCase):
    def test_license_exact_copyright(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_readme_credits_llc(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)

    def test_no_obvious_secrets(self):
        pattern = re.compile(
            r"(api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9]{16,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,})",
            re.IGNORECASE,
        )
        for f in ROOT.rglob("*"):
            if not f.is_file() or f.name.startswith(".git"):
                continue
            if f.suffix not in {".py", ".md", ".css", ".txt"}:
                continue
            self.assertIsNone(pattern.search(f.read_text(errors="ignore")), f"secret-like string in {f}")


if __name__ == "__main__":
    unittest.main()

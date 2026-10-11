from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.docs_nav import directory_title, first_h1

from scripts.check_masterclass_navigation import authored_entries, check_rendered_navigation


class CatalogNavigationTests(unittest.TestCase):
    expected = authored_entries([
        {"Course": [{"Home": "course/index.md"}, {"Safety & trust": "course/safety.md"}]}
    ])
    html = """<nav id="bijux-navigation" data-bijux-nav-variant="complete">
        <details><summary>Course</summary>
        <a class="md-nav__link" href="./" aria-current="page"><span>Home</span></a>
        <a class="md-nav__link" href="safety/"><span>Safety &amp; trust</span></a>
        </details></nav>"""

    def test_complete_tree_preserves_authored_labels_order_and_destinations(self) -> None:
        check_rendered_navigation(self.html, "course/index.html", self.expected)

    def test_missing_tree_entry_is_rejected(self) -> None:
        with self.assertRaisesRegex(AssertionError, "authored order"):
            check_rendered_navigation(self.html.replace("md-nav__link", "unrelated", 1), "course/index.html", self.expected)

    def test_reordered_tree_entries_are_rejected(self) -> None:
        with self.assertRaisesRegex(AssertionError, "authored order"):
            check_rendered_navigation(self.html, "course/index.html", list(reversed(self.expected)))

    def test_incorrect_link_destination_is_rejected(self) -> None:
        with self.assertRaisesRegex(AssertionError, "authored order"):
            check_rendered_navigation(self.html.replace('href="safety/"', 'href="missing/"'), "course/index.html", self.expected)

    def test_missing_current_page_is_rejected(self) -> None:
        with self.assertRaisesRegex(AssertionError, "current-page"):
            check_rendered_navigation(self.html.replace('aria-current="page"', ''), "course/index.html", self.expected)

    def test_another_page_marked_current_is_rejected(self) -> None:
        html = self.html.replace('aria-current="page"', '').replace('href="safety/"', 'href="safety/" aria-current="page"')
        with self.assertRaisesRegex(AssertionError, "current-page"):
            check_rendered_navigation(html, "course/index.html", self.expected)

    def test_retired_scoped_variant_is_rejected(self) -> None:
        with self.assertRaisesRegex(AssertionError, "complete catalog"):
            check_rendered_navigation(self.html.replace('variant="complete"', 'variant="scoped"'), "course/index.html", self.expected)


class AuthoredHeadingTests(unittest.TestCase):
    def test_heading_attributes_do_not_change_reader_navigation_labels(self) -> None:
        root=Path(__file__).resolve().parents[2]
        artifacts=root/'artifacts/docs/navigation-controls'
        artifacts.mkdir(parents=True,exist_ok=True)
        with TemporaryDirectory(dir=artifacts) as directory:
            reference=Path(directory)/'reference';reference.mkdir()
            page=reference/'index.md';page.write_text('# Deep Dive Make Reference {#reference}\n')
            self.assertEqual(first_h1(page),'Deep Dive Make Reference')
            self.assertEqual(directory_title(reference),'Reference')
            self.assertEqual(page.read_text(),'# Deep Dive Make Reference {#reference}\n')

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.markdown import (
    github_math_diagnostics,
    github_math_issues,
    headings,
    normalize_github_math,
    normalize_parenthetical_math,
    prose_only,
)


class MarkdownStructureTests(unittest.TestCase):
    def test_atx_headings_outside_fences_are_found(self) -> None:
        text = "# Real\n\n```text\n## Not Real\n```\n\n## Also Real ##\n"
        self.assertEqual(["Real", "Also Real"], [heading.title for heading in headings(text)])

    def test_tilde_fence_content_is_removed_from_prose(self) -> None:
        text = "before\n~~~markdown\n[missing](missing.md)\n~~~\nafter\n"
        prose = prose_only(text)
        self.assertIn("before", prose)
        self.assertIn("after", prose)
        self.assertNotIn("missing.md", prose)

    def test_legacy_math_is_normalized_without_rewriting_code_fences(self) -> None:
        text = "\\[\nx^2\n\\]\n\nLet \\(x_i\\in X\\) be valid. `\\eta=x/y`\n\n```text\n\\(not math\\)\n```\n"
        normalized = normalize_github_math(text)
        self.assertIn("$$\nx^2\n$$", normalized)
        self.assertIn("Let $x_i\\in X$ be valid. `\\eta=x/y`", normalized)
        self.assertIn("\\(not math\\)", normalized)
        self.assertEqual(
            ("mathematical TeX must use math delimiters rather than inline code",),
            github_math_issues(normalized),
        )

    def test_rendering_lint_rejects_legacy_delimiters_and_math_in_code(self) -> None:
        issues = github_math_issues("Use \\(x\\) and `\\eta=x/y`; raw \\alpha is invalid.\n")
        self.assertEqual(2, len(issues))

    def test_programming_escapes_remain_inline_code(self) -> None:
        text = "Use `a\\r\\nb\\n`, `e\\u0301`, and `\\q` as literal source text.\n"
        self.assertEqual(text, normalize_github_math(text))
        self.assertEqual((), github_math_issues(text))

    def test_html_comment_payload_is_not_normalized_as_math(self) -> None:
        text = '<!-- bijux-verify: {"stdout":"value=(a\\n)\\n"} -->\n'
        self.assertEqual(text, normalize_github_math(text))
        self.assertEqual((), github_math_issues(text))

    def test_inline_code_detection_does_not_span_adjacent_code_spans(self) -> None:
        text = "Use `left` before $a\\mapsto b$ and then `right`.\n"
        self.assertEqual((), github_math_issues(text))

    def test_verification_annotation_with_arrow_is_not_math_prose(self) -> None:
        text = '<!-- bijux-verify: {"stdout":"draft --submit--> published\\n"} -->\n'
        self.assertEqual((), github_math_issues(text))

    def test_display_math_body_is_not_converted_to_nested_inline_math(self) -> None:
        text = "\\[\nf(x)=(x+1)\\times2\n\\]\n"
        normalized = normalize_github_math(text)
        self.assertEqual("$$\nf(x)=(x+1)\\times2\n$$\n", normalized)

    def test_parenthetical_tex_requires_authorial_review(self) -> None:
        text = "Existing $x\\to y$ and raw (obs_B:O\\to A_B); code `f(x)`.\n"
        normalized = normalize_github_math(text)
        self.assertEqual(text, normalized)
        self.assertEqual(
            ("remaining TeX command outside recognized math delimiters",),
            github_math_diagnostics(normalized),
        )

    def test_dollar_in_inline_code_does_not_hide_later_raw_tex(self) -> None:
        text = "The sentinel is `$`; raw \\alpha remains invalid.\n"
        self.assertEqual(
            ("remaining TeX command outside recognized math delimiters",),
            github_math_diagnostics(text),
        )

    def test_parenthetical_notation_can_be_repaired_explicitly(self) -> None:
        text = "Let (P) contain programs and (p(x)=(x+1)+1) define behavior.\n"
        self.assertEqual(
            "Let $P$ contain programs and $p(x)=(x+1)+1$ define behavior.\n",
            normalize_parenthetical_math(text),
        )

    def test_parenthetical_repair_normalizes_lost_tex_commands(self) -> None:
        text = "Space is (Theta(n)), with (operatorname{rank}_1(i)=i) and $log_2 n$.\n"
        self.assertEqual(
            r"Space is $\Theta(n)$, with $\operatorname{rank}_1(i)=i$ and $\log_2 n$." + "\n",
            normalize_parenthetical_math(text),
        )

    def test_parenthetical_repair_handles_arithmetic_and_half_open_ranges(self) -> None:
        text = "Use (n-1), (B[i]), and (B[0..i)); there are (2^n) cases.\n"
        self.assertEqual(
            "Use $n-1$, $B[i]$, and $B[0..i)$; there are $2^n$ cases.\n",
            normalize_parenthetical_math(text),
        )

    def test_parenthetical_repair_recovers_backspace_damaged_binomial(self) -> None:
        text = "There are (\x08inom{n}{m}) choices.\n"
        self.assertEqual(
            r"There are $\binom{n}{m}$ choices." + "\n",
            normalize_parenthetical_math(text),
        )

    def test_parenthetical_repair_preserves_prose_code_links_and_math(self) -> None:
        text = (
            "Keep (HTTP), (for example), `f(x)`, [guide](docs/(current).md), "
            "and $q(x)$; convert (x).\n"
        )
        self.assertEqual(
            "Keep (HTTP), (for example), `f(x)`, [guide](docs/(current).md), "
            "and $q(x)$; convert $x$.\n",
            normalize_parenthetical_math(text),
        )



if __name__ == "__main__":
    unittest.main()

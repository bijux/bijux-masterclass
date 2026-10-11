"""Preserve authored link intent while projecting course documents to public routes."""
from __future__ import annotations
import re
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urlsplit, urlunsplit
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")

def split_anchor(target: str) -> tuple[str, str]:
    if "#" not in target:
        return target, ""
    path, anchor = target.split("#", 1)
    return path, f"#{anchor}"


def normalize_catalog_path(target: str) -> str:
    path, anchor = split_anchor(target)
    path = path.replace("/course-book/", "/")
    path = path.replace("/capstone/docs/", "/capstone-docs/")
    if path.startswith("course-book/"):
        path = path.removeprefix("course-book/")
    if path.startswith("capstone/docs/"):
        path = f"capstone-docs/{path[len('capstone/docs/'):]}"
    if path == "README.md":
        path = "index.md"
    elif path.endswith("/README.md"):
        path = f"{path[:-len('README.md')]}index.md"
    return f"{path}{anchor}"


def rewrite_link_target(
    target: str,
    *,
    capstone_docs_public_parent: bool = False,
) -> str:
    if "://" in target or target.startswith(("mailto:", "#")):
        return target
    path, anchor = split_anchor(target)
    if capstone_docs_public_parent and path == "../README.md":
        return f"../capstone/index.md{anchor}"
    return normalize_catalog_path(target)


def _code_mask(content: str) -> str:
    """Keep parser offsets stable while excluding Markdown fenced and inline code."""
    masked = list(content)
    offset = 0
    fence = None
    for line in content.splitlines(keepends=True):
        marker = re.match(r" {0,3}(`{3,}|~{3,})(.*)", line)
        if fence:
            for index in range(offset, offset + len(line)):
                if masked[index] != "\n":
                    masked[index] = " "
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
        elif marker and not (marker[1][0] == "`" and "`" in marker[2]):
            fence = (marker[1][0], len(marker[1]))
            for index in range(offset, offset + len(line)):
                if masked[index] != "\n":
                    masked[index] = " "
        offset += len(line)
    text = "".join(masked)
    delimiters = list(re.finditer(r"(?<!`)(`+)(?!`)", text))
    cursor = 0
    while cursor < len(delimiters):
        opening = delimiters[cursor]
        prefix = text[:opening.start()]
        if (len(prefix) - len(prefix.rstrip("\\"))) % 2:
            cursor += 1
            continue
        closing = next((index for index in range(cursor + 1, len(delimiters)) if delimiters[index][0] == opening[0]), None)
        if closing is None:
            cursor += 1
            continue
        for index in range(opening.start(), delimiters[closing].end()):
            if masked[index] != "\n":
                masked[index] = " "
        cursor = closing + 1
    return "".join(masked)


def rewrite_html_hyperlinks(content: str, *, capstone_docs_public_parent: bool = False) -> str:
    """Project relative Markdown hyperlinks onto the catalog's directory URLs."""
    line_offsets = [0]
    for match in re.finditer("\n", content):
        line_offsets.append(match.end())
    replacements = []
    attribute = re.compile(r"(?P<name>[^\s/=>]+)\s*=\s*(?:([\"'])(.*?)\2|([^\s>]+))", re.DOTALL)

    def public_href(value: str) -> str:
        decoded = unescape(value)
        if any(ord(char) < 32 or ord(char) == 127 for char in decoded):
            raise ValueError("catalog HTML href contains control characters")
        parsed = urlsplit(decoded)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
            return value
        path = unquote(parsed.path, errors="strict")
        reparsed = urlsplit(path)
        if reparsed.scheme or reparsed.netloc or path.startswith("/"):
            return value
        if any(ord(char) < 32 or ord(char) == 127 for char in path):
            raise ValueError("catalog HTML href contains encoded control characters")
        if not path.endswith(".md"):
            return value
        projected = rewrite_link_target(path, capstone_docs_public_parent=capstone_docs_public_parent)
        route = projected[:-8] if projected.endswith("index.md") else projected[:-3] + "/"
        route = quote(route or "./", safe="/.-_~")
        return escape(urlunsplit(("", "", route, parsed.query, parsed.fragment)), quote=True)

    class Hyperlinks(HTMLParser):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.ancestors = []
            self.code_ancestors = []

        def handle_starttag(self, tag, attrs):
            line, column = self.getpos()
            code = any(self.code_ancestors) or any(parent in ("pre", "code") for parent in self.ancestors)
            block = any(parent in ("div", "section", "table", "ul", "ol", "li", "details", "article") for parent in self.ancestors)
            if tag not in ("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"):
                self.ancestors.append(tag)
                self.code_ancestors.append(code or (column >= 4 and not block))
            if tag not in ("a", "area") or code or (column >= 4 and not block):
                return
            start = line_offsets[line - 1] + column
            raw = content[start:start + len(self.get_starttag_text())]
            hrefs = [match for match in attribute.finditer(raw) if match['name'].lower() == 'href']
            if len(hrefs) > 1:
                raise ValueError("catalog HTML hyperlink contains duplicate href attributes")
            for match in hrefs:
                group = 3 if match[2] else 4
                original = match[group]
                projected = public_href(original)
                if projected != original:
                    replacements.append((start + match.start(group), start + match.end(group), projected))

        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
            self.handle_endtag(tag)

        def handle_endtag(self, tag):
            if tag in self.ancestors:
                position = len(self.ancestors) - 1 - self.ancestors[::-1].index(tag)
                del self.ancestors[position:]
                del self.code_ancestors[position:]

    parser = Hyperlinks(convert_charrefs=False)
    parser.feed(_code_mask(content))
    parser.close()
    for start, end, replacement in reversed(replacements):
        content = content[:start] + replacement + content[end:]
    return content



def rewrite_markdown_links(
    content: str,
    *,
    capstone_docs_public_parent: bool = False,
) -> str:
    content = rewrite_html_hyperlinks(content, capstone_docs_public_parent=capstone_docs_public_parent)
    return MARKDOWN_LINK_RE.sub(
        lambda match: (
            f"{match.group(1)}"
            f"{rewrite_link_target(match.group(2), capstone_docs_public_parent=capstone_docs_public_parent)}"
            f"{match.group(3)}"
        ),
        content,
    )

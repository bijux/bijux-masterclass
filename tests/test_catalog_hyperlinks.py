import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('catalog_projection',ROOT/'scripts/sync_series_docs.py')
projection=importlib.util.module_from_spec(spec);spec.loader.exec_module(projection)

class CatalogHyperlinks(unittest.TestCase):
 def test_actual_catalog_raw_buttons_match_public_routes(self):
  source=(ROOT/'programs/README.md').read_text();result=projection.rewrite_markdown_links(source)
  self.assertIn('href="python-programming/"',result)
  self.assertIn('href="python-programming/python-object-oriented-programming/"',result)
  self.assertNotIn('href="python-programming/README.md"',result)
  self.assertNotIn('href="python-programming/python-object-oriented-programming/course-book/index.md"',result)
 def test_quote_case_entities_query_and_fragment(self):
  text="<A class='reader' HREF = 'course-book/chapter.md?q=a&amp;b=2#deep%20anchor'>Keep &amp; this</A>"
  self.assertEqual(projection.rewrite_html_hyperlinks(text),"<A class='reader' HREF = 'chapter/?q=a&amp;b=2#deep%20anchor'>Keep &amp; this</A>")
 def test_unquoted_relative_href_is_projected_safely(self):
  self.assertEqual(projection.rewrite_html_hyperlinks('<a href=course-book/a%20b.md>Read</a>'),'<a href=a%20b/>Read</a>')
 def test_html_attributes_that_contain_href_text_are_preserved(self):
  text='<a data-href="README.md" title="href=\'README.md\'" href="README.md">Read</a>'
  self.assertEqual(projection.rewrite_html_hyperlinks(text),'<a data-href="README.md" title="href=\'README.md\'" href="./">Read</a>')
 def test_external_absolute_fragment_and_non_markdown_preserved(self):
  for target in ['https://example.org/README.md','//example.org/README.md','mailto:reader@example.org','javascript:alert(1)','/another-product/README.md','#section','?q=README.md','asset.png']:
   text=f'<a href="{target}">unchanged</a>';self.assertEqual(projection.rewrite_html_hyperlinks(text),text)
 def test_percent_encoded_path_does_not_create_scheme_or_host(self):
  for target in ['https%3A%2F%2Fexample.org%2FREADME.md','%2F%2Fexample.org/README.md']:
   text=f'<a href="{target}">Keep</a>';self.assertEqual(projection.rewrite_html_hyperlinks(text),text)
 def test_encoded_filename_and_html_quoting(self):
  self.assertEqual(projection.rewrite_html_hyperlinks('<a href="course-book/a%20b%22c.md">Read</a>'),'<a href="a%20b%22c/">Read</a>')
 def test_capstone_parent_is_owned_public_route(self):
  self.assertEqual(projection.rewrite_html_hyperlinks('<a href="../README.md">Read</a>',capstone_docs_public_parent=True),'<a href="../capstone/">Read</a>')
 def test_fenced_and_inline_code_are_preserved(self):
  code='```html\n<a href="README.md">example</a>\n```\n`<a href="README.md">example</a>`\n~~~html\n<a href="README.md">example</a>\n~~~\n'
  self.assertEqual(projection.rewrite_html_hyperlinks(code),code)
 def test_indented_and_pre_code_are_preserved(self):
  for code in ['    <div>\n    <a href="README.md">example</a>\n    </div>\n','    <a href="README.md">example</a>\n','<pre><code><a href="README.md">example</a></code></pre>']:
   self.assertEqual(projection.rewrite_html_hyperlinks(code),code)
 def test_nested_real_html_indentation_is_converted(self):
  self.assertEqual(projection.rewrite_html_hyperlinks('<div>\n    <a href="README.md">Read</a>\n</div>'),'<div>\n    <a href="./">Read</a>\n</div>')
 def test_duplicate_href_refused(self):
  with self.assertRaisesRegex(ValueError,'duplicate href'):projection.rewrite_html_hyperlinks('<a href="README.md" href="other.md">Ambiguous</a>')
 def test_encoded_control_character_refused(self):
  with self.assertRaisesRegex(ValueError,'control characters'):projection.rewrite_html_hyperlinks('<a href="course-book/a%0A.md">Unsafe</a>')
 def test_malformed_html_does_not_rewrite_text(self):
  text='<a href="README.md';self.assertEqual(projection.rewrite_html_hyperlinks(text),text)
 def test_projection_is_idempotent(self):
  source=(ROOT/'programs/README.md').read_text();once=projection.rewrite_markdown_links(source);self.assertEqual(projection.rewrite_markdown_links(once),once)

if __name__=='__main__':unittest.main()

import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('catalog_site',ROOT/'scripts/verify_catalog_site.py')
site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)

class CatalogSite(unittest.TestCase):
 def setUp(self):
  outputs=ROOT/'artifacts/tests/catalog-links';outputs.mkdir(parents=True,exist_ok=True)
  self.folder=tempfile.TemporaryDirectory(dir=outputs);self.root=Path(self.folder.name);self.catalog=self.root/'site';self.catalog.mkdir()
 def tearDown(self):self.folder.cleanup()
 def report(self):return site.inspect_catalog(self.catalog,'https://bijux.io/bijux-masterclass/')
 def test_good_owned_route_and_anchor_pass(self):
  (self.catalog/'index.html').write_text('<article><a href="chapter/#topic">Read</a></article>');(self.catalog/'chapter').mkdir();(self.catalog/'chapter/index.html').write_text('<article><h1 id="topic">Topic</h1></article>')
  self.assertTrue(self.report()['passed'])
 def test_stale_repository_markdown_href_fails(self):
  (self.catalog/'index.html').write_text('<article><a href="course-book/index.md">Read</a></article>');r=self.report();self.assertFalse(r['passed']);self.assertEqual(r['errors'][0]['reason'],'missing public destination')
 def test_missing_anchor_fails(self):
  (self.catalog/'index.html').write_text('<article><a href="#missing">Read</a></article>');self.assertEqual(self.report()['errors'][0]['reason'],'missing public anchor')
 def test_external_source_and_cross_product_links_preserved(self):
  (self.catalog/'index.html').write_text('<article><a href="https://github.com/bijux/bijux-masterclass">Source</a><a href="https://bijux.io/bijux-core/">Core</a></article>');self.assertTrue(self.report()['passed'])
 def test_encoded_escape_is_rejected(self):
  (self.catalog/'index.html').write_text('<article><a href="%2e%2e/secret.html">Bad</a></article>');self.assertEqual(self.report()['errors'][0]['reason'],'destination escapes selected catalog')
 def test_no_root_artifact_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'root page'):self.report()
 def test_artifact_identity_changes_with_modified_payload(self):
  (self.catalog/'index.html').write_text('<article><h1 id="topic">First</h1></article>');before=self.report()['bundle_sha256'];(self.catalog/'index.html').write_text('<article><h1 id="topic">Changed</h1></article>');self.assertNotEqual(before,self.report()['bundle_sha256'])

if __name__=='__main__':unittest.main()

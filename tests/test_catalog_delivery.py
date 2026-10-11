"""Keep catalogue orchestration failures visible and Pages privileges scoped."""
from pathlib import Path
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
STAGES = ['venv', 'bootstrap', 'dependencies', 'shared', 'sources', 'config', 'build', 'verify']
CONTROL = '''import json,os,sys
from pathlib import Path
stage=sys.argv[1]
if stage=="pip":stage="bootstrap" if "-U" in sys.argv else "dependencies"
p=Path(os.environ["DELIVERY_TRACE"])
with p.open("a") as stream:stream.write(json.dumps(dict(stage=stage,args=sys.argv[2:]))+"\\n")
raise SystemExit(17 if stage==os.environ.get("DELIVERY_FAIL") else 0)
'''


class CatalogDeliveryTests(unittest.TestCase):
    def setUp(self):
        controls=ROOT/'artifacts/docs/catalogue-delivery-tests'
        controls.mkdir(parents=True,exist_ok=True)
        directory=tempfile.TemporaryDirectory(dir=controls)
        self.addCleanup(directory.cleanup)
        self.directory=Path(directory.name)
        self.trace=self.directory/'trace.jsonl'
        self.control=self.directory/'delivery_control.py';self.control.write_text(CONTROL)
        self.makefile=self.directory/'Makefile'
        def command(stage):
            return ' '.join(shlex.quote(value) for value in [sys.executable,str(self.control),stage])
        self.makefile.write_text('\n'.join([
            'SHELL := /bin/sh', '.SHELLFLAGS := -eu -c',
            'PYTHON := '+command('venv'), 'PIP := '+command('pip'),
            'VENV_DIR := artifacts/catalog-controlled-environment',
            'DOCS_REQUIREMENTS := configs/docs/requirements-docs.txt',
            'SYNC_SERIES_DOCS := '+command('sources'),
            'RENDER_ROOT_MKDOCS := '+command('config'),
            'MKDOCS := '+command('build'), 'VENV_PY := '+command('verify'),
            'ROOT_MKDOCS_FILE := artifacts/mkdocs.root.yml', 'DOCS_ENV :=',
            'include '+str(ROOT/'makes/series-docs.mk'),
            '.PHONY: bijux-docs-sync', 'bijux-docs-sync:', '\t@'+command('shared'),'',
        ]))

    def run_pipeline(self, failure=None):
        environment={**os.environ,'DELIVERY_TRACE':str(self.trace)}
        if failure:environment['DELIVERY_FAIL']=failure
        else:environment.pop('DELIVERY_FAIL',None)
        result=subprocess.run(['make','-f',str(self.makefile),'series-docs-build'],cwd=self.directory,
                              env=environment,capture_output=True,text=True)
        rows=[json.loads(line) for line in self.trace.read_text().splitlines()]
        return result,rows

    def assert_failure(self, stage):
        result,rows=self.run_pipeline(stage)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual([row['stage'] for row in rows],STAGES[:STAGES.index(stage)+1])
        self.assertIn('Error 17',result.stderr)

    def test_environment_creation_failure_stops_build(self):self.assert_failure('venv')
    def test_dependency_bootstrap_failure_stops_build(self):self.assert_failure('bootstrap')
    def test_dependency_install_failure_stops_build(self):self.assert_failure('dependencies')
    def test_shared_projection_failure_stops_build(self):self.assert_failure('shared')
    def test_authored_projection_failure_stops_build(self):self.assert_failure('sources')
    def test_effective_configuration_failure_stops_build(self):self.assert_failure('config')
    def test_strict_renderer_failure_stops_verification(self):self.assert_failure('build')
    def test_article_verifier_failure_stops_candidate_success(self):self.assert_failure('verify')

    def test_success_keeps_strict_renderer_and_selected_config_verification(self):
        result,rows=self.run_pipeline()
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual([row['stage'] for row in rows],STAGES)
        self.assertIn('--strict',rows[-2]['args'])
        self.assertEqual(rows[-1]['args'],['scripts/verify_catalog_site.py','--config','artifacts/mkdocs.root.yml','--output','artifacts/docs/catalog-links.json'])

    def test_verification_install_is_separate_from_production_prerequisites(self):
        text=(ROOT/'makes/series-docs.mk').read_text()
        self.assertIn('series-docs-verification-install:',text)
        self.assertIn('DOCS_VERIFICATION_ENV ?= $(ARTIFACTS_DIR)/venv/catalog-verification',text)
        self.assertIn('series-docs-install: series-docs-venv',text)
        self.assertNotIn('series-docs-build: series-docs-verification-install',text)

    def test_documentation_build_receives_no_publication_credentials(self):
        workflow=yaml.safe_load((ROOT/'.github/workflows/deploy-docs.yml').read_text())
        self.assertEqual(workflow['permissions'],{'contents':'read'})
        self.assertEqual(workflow['jobs']['build']['permissions'],{'contents':'read'})
        self.assertEqual(workflow['jobs']['deploy']['permissions'],{'pages':'write','id-token':'write'})
        trigger=workflow.get('on',workflow.get(True))
        self.assertEqual(set(trigger),{'workflow_dispatch'})
        self.assertTrue(trigger['workflow_dispatch']['inputs']['accepted_commit']['required'])
        self.assertFalse((ROOT/'.github/workflows/pages.yml').exists())
        admission=workflow['jobs']['publication_admission']
        self.assertIn('publication_admission.py',str(admission['steps']))
        self.assertIn('publication_admission',workflow['jobs']['build']['needs'])

    def test_pages_configuration_and_deployment_stay_in_deploy_job(self):
        workflow=yaml.safe_load((ROOT/'.github/workflows/deploy-docs.yml').read_text())
        build=workflow['jobs']['build']['steps'];deploy=workflow['jobs']['deploy']['steps']
        self.assertFalse(any('actions/configure-pages@' in step.get('uses','') for step in build))
        self.assertTrue(any('actions/configure-pages@' in step.get('uses','') for step in deploy))
        self.assertTrue(any('actions/deploy-pages@' in step.get('uses','') for step in deploy))
        self.assertEqual(set(workflow['jobs']['deploy']['needs']),{'publication_admission','build'})
        self.assertEqual(workflow['jobs']['deploy']['environment']['name'],'github-pages')
        self.assertIn("github.event_name == 'workflow_dispatch'",workflow['jobs']['deploy']['if'])
        self.assertIn("github.ref == 'refs/heads/main'",workflow['jobs']['deploy']['if'])


if __name__=='__main__':unittest.main()

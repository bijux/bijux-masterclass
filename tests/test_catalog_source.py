"""Verify original-source planning and reject unsafe or unbound derived catalogue data."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.catalogue.files import (
    capture_sources,
    verify_outputs,
    verify_sources,
    write_configuration,
    write_documents,
    write_program_documents,
)
from scripts.catalogue.source_plan import PlanError, build_plan

ROOT = Path(__file__).resolve().parents[1]


def original_fixture():
    return {
        'mkdocs.yml': b'INHERIT: mkdocs.shared.yml\nsite_url: !ENV [SITE_URL, https://example.org/catalogue/]\nnav:\n  - Home: index.md\n  - Family: family/index.md\n',
        'mkdocs.shared.yml': b'theme:\n  name: material\n',
        'programs/README.md': b'# Catalogue\n[Family](family/README.md)\n',
        'programs/family/README.md': b'# Family\n[Course](course/course-book/index.md)\n',
        'programs/family/course/mkdocs.yml': b'site_name: Course\nnav:\n  - Home: index.md\n  - Chapter: chapter.md\n',
        'programs/family/course/course-book/index.md': b'# Course\n[Chapter](chapter.md)\n',
        'programs/family/course/course-book/chapter.md': b'# Chapter\n[Home](index.md)\n',
        'scripts/sync_series_docs.py': b'# captured document generator\n',
        'scripts/render_root_mkdocs.py': b'# captured config generator\n',
        'scripts/docs_nav.py': b'# captured navigation policy\n',
    }


class CatalogueSourceTests(unittest.TestCase):
    def setUp(self):
        folder = ROOT / 'artifacts/tests/catalogue-source'
        folder.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=folder)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.originals = original_fixture()
        for name, content in self.originals.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.plan = build_plan(self.originals)

    def materialize(self):
        write_documents(self.plan, self.root)
        write_configuration(self.plan, self.root)

    def test_planned_content_is_outside_publication_inputs(self):
        original = capture_sources(self.root)
        planned = self.root / 'programs-planned/computing-reference'
        planned.mkdir(parents=True)
        (planned / 'mkdocs.yml').write_text('unfinished: [invalid configuration')
        (planned / 'README.md').write_text('[Unfinished](missing.md)\n')
        self.assertEqual(capture_sources(self.root), original)
        (planned / 'README.md').write_text('Changed unfinished content\n')
        verify_sources(self.plan, self.root)
        self.assertEqual(build_plan(capture_sources(self.root)), self.plan)

    def test_pure_plan_needs_no_files_environment_process_or_clock(self):
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('filesystem input')), patch('os.getenv', side_effect=AssertionError('hidden environment')):
            self.assertEqual(build_plan(list(reversed(list(self.originals.items())))), self.plan)

    def test_explicit_environment_and_original_owner_are_distinct_from_output(self):
        plan = build_plan(self.originals, environment={'SITE_URL': 'https://reader.example/catalogue/'})
        config = yaml.safe_load(plan.configuration.content)
        self.assertEqual(config['site_url'], 'https://reader.example/catalogue/')
        self.assertEqual(plan.configuration.environment, (('SITE_URL', 'https://reader.example/catalogue/'),))
        self.assertEqual(plan.configuration.owner, 'mkdocs.yml')
        self.assertEqual(plan.configuration.destination, 'artifacts/mkdocs.root.yml')
        self.assertEqual(plan.configuration.inputs, tuple(sorted(self.originals)))
        self.assertEqual(plan.configuration.navigation_configs, ('programs/family/course/mkdocs.yml',))
        self.assertNotIn('artifacts/mkdocs.root.yml', dict(plan.source_hashes))
        self.assertNotIn('docs/index.md', dict(plan.source_hashes))

    def test_every_document_has_an_original_and_public_byte_projection(self):
        self.assertEqual(len(self.plan.documents), 4)
        self.assertEqual(self.plan.output_bytes()['docs/index.md'], b'# Catalogue\n[Family](family/index.md)\n')
        self.materialize()
        verify_outputs(self.plan, self.root)

    def test_configuration_has_no_uncaptured_navigation_override(self):
        with self.assertRaises(TypeError):
            build_plan(self.originals, source_nav=[{'Home': 'other.md'}])

    def test_unreferenced_environment_is_not_captured(self):
        plan = build_plan(self.originals, environment={'UNRELATED_SECRET': 'not-a-build-input'})
        self.assertEqual(plan, self.plan)
        self.assertNotIn('UNRELATED_SECRET', dict(plan.configuration.environment))

    def test_duplicate_original_is_rejected(self):
        with self.assertRaisesRegex(PlanError, 'duplicate original'):
            build_plan([*self.originals.items(), ('mkdocs.yml', b'other')])

    def test_unsafe_original_names_are_rejected(self):
        for name in ['../escape.md', '/escape.md', 'a//b.md', 'a/./b.md', 'a\\b.md', 'a\x00b.md']:
            with self.subTest(name=name), self.assertRaisesRegex(PlanError, 'unsafe catalogue path'):
                build_plan({**self.originals, name: b'unsafe'})

    def test_duplicate_public_destination_is_rejected(self):
        originals = {**self.originals, 'programs/family/course/course-book/capstone-docs/index.md': b'# First',
                     'programs/family/course/capstone/docs/index.md': b'# Second'}
        with self.assertRaisesRegex(PlanError, 'duplicate public destination'):
            build_plan(originals)

    def test_missing_family_original_is_rejected(self):
        del self.originals['programs/family/README.md']
        with self.assertRaisesRegex(PlanError, 'missing original source'):
            build_plan(self.originals)

    def test_missing_explicit_course_config_is_rejected(self):
        del self.originals['programs/family/course/mkdocs.yml']
        with self.assertRaisesRegex(PlanError, 'missing original source'):
            build_plan(self.originals)

    def test_missing_navigation_document_is_rejected(self):
        del self.originals['programs/family/course/course-book/chapter.md']
        with self.assertRaisesRegex(PlanError, 'navigation has no planned document'):
            build_plan(self.originals)

    def test_duplicate_configuration_key_is_rejected(self):
        self.originals['mkdocs.yml'] += b'nav: []\n'
        with self.assertRaisesRegex(PlanError, 'duplicate configuration key'):
            build_plan(self.originals)

    def test_configuration_cannot_select_uncaptured_inheritance(self):
        self.originals['mkdocs.yml'] = self.originals['mkdocs.yml'].replace(b'mkdocs.shared.yml', b'other.yml')
        with self.assertRaisesRegex(PlanError, 'captured mkdocs.shared'):
            build_plan(self.originals)

    def test_source_change_is_rejected_before_existing_output_deletion(self):
        self.materialize()
        output = self.root / 'docs/index.md'
        before = output.read_bytes()
        (self.root / 'programs/README.md').write_bytes(b'# Changed original')
        with self.assertRaisesRegex(PlanError, 'inputs changed'):
            write_documents(self.plan, self.root)
        self.assertEqual(output.read_bytes(), before)

    def test_generator_source_change_is_not_hidden_from_binding(self):
        (self.root / 'scripts/docs_nav.py').write_bytes(b'# changed policy')
        with self.assertRaisesRegex(PlanError, 'inputs changed'):
            verify_sources(self.plan, self.root)

    def test_original_file_symlink_is_rejected(self):
        original = self.root / 'programs/README.md'
        original.unlink()
        original.symlink_to(self.root / 'mkdocs.yml')
        with self.assertRaisesRegex(PlanError, 'symlink'):
            capture_sources(self.root)

    def test_original_directory_symlink_is_rejected(self):
        (self.root / 'programs/alias').symlink_to(self.root / 'programs/family', target_is_directory=True)
        with self.assertRaisesRegex(PlanError, 'symlink'):
            capture_sources(self.root)

    def test_destination_symlink_is_rejected_without_following_it(self):
        (self.root / 'docs').mkdir()
        (self.root / 'docs/index.md').symlink_to(self.root / 'programs/README.md')
        before = (self.root / 'programs/README.md').read_bytes()
        with self.assertRaisesRegex(PlanError, 'symlink'):
            write_documents(self.plan, self.root)
        self.assertEqual((self.root / 'programs/README.md').read_bytes(), before)

    def test_generated_document_tampering_is_rejected(self):
        self.materialize()
        (self.root / 'docs/family/index.md').write_bytes(b'# Forged ordering\n[Course](course/index.md)\n')
        with self.assertRaisesRegex(PlanError, 'derived catalogue documents'):
            write_configuration(self.plan, self.root)

    def test_missing_generated_document_is_rejected(self):
        self.materialize()
        (self.root / 'docs/family/course/chapter.md').unlink()
        with self.assertRaisesRegex(PlanError, 'derived catalogue documents'):
            verify_outputs(self.plan, self.root)

    def test_unexpected_generated_document_is_rejected(self):
        self.materialize()
        (self.root / 'docs/family/course/extra.md').write_bytes(b'# Injected')
        with self.assertRaisesRegex(PlanError, 'derived catalogue documents'):
            verify_outputs(self.plan, self.root)

    def test_wrong_and_missing_derived_configuration_are_rejected(self):
        self.materialize()
        path = self.root / 'artifacts/mkdocs.root.yml'
        for content in [b'nav: []\n', None]:
            if content is None: path.unlink()
            else: path.write_bytes(content)
            with self.assertRaisesRegex(PlanError, 'captured owner'):
                verify_outputs(self.plan, self.root)

    def test_config_generation_requires_complete_generated_documents(self):
        with self.assertRaisesRegex(PlanError, 'derived catalogue documents'):
            write_configuration(self.plan, self.root)
        self.assertFalse((self.root / 'artifacts/mkdocs.root.yml').exists())

    def test_configuration_hardlink_is_rejected_before_original_damage(self):
        write_documents(self.plan, self.root)
        original = self.root / 'mkdocs.yml'
        before = original.read_bytes()
        output = self.root / 'artifacts/mkdocs.root.yml'
        output.parent.mkdir()
        os.link(original, output)
        with self.assertRaisesRegex(PlanError, 'hardlink'):
            write_configuration(self.plan, self.root)
        self.assertEqual(original.read_bytes(), before)
        self.assertEqual(output.read_bytes(), before)
        self.assertTrue(os.path.samefile(original, output))

    def test_failed_atomic_configuration_write_preserves_existing_bytes(self):
        self.materialize()
        output = self.root / 'artifacts/mkdocs.root.yml'
        before = output.read_bytes()
        original = (self.root / 'mkdocs.yml').read_bytes()
        with patch('scripts.catalogue.files.os.replace', side_effect=OSError('replace unavailable')), self.assertRaisesRegex(OSError, 'replace unavailable'):
            write_configuration(self.plan, self.root)
        self.assertEqual(output.read_bytes(), before)
        self.assertEqual((self.root / 'mkdocs.yml').read_bytes(), original)
        self.assertEqual(list(output.parent.glob('.catalogue-*')), [])

    def test_configuration_repeated_atomic_write_keeps_source_and_output_bound(self):
        self.materialize()
        before = capture_sources(self.root)
        write_configuration(self.plan, self.root)
        verify_outputs(self.plan, self.root)
        self.assertEqual(capture_sources(self.root), before)
        self.assertEqual(list((self.root / 'artifacts').glob('.catalogue-*')), [])

    def test_document_hardlink_replacement_preserves_original(self):
        self.materialize()
        original = self.root / 'programs/README.md'
        before = original.read_bytes()
        output = self.root / 'docs/index.md'
        output.unlink()
        os.link(original, output)
        write_documents(self.plan, self.root)
        self.assertEqual(original.read_bytes(), before)
        self.assertFalse(os.path.samefile(original, output))
        self.assertEqual(output.read_bytes(), self.plan.output_bytes()['docs/index.md'])

    def test_unknown_family_output_is_rejected_before_any_deletion(self):
        self.materialize()
        output = self.root / 'docs/family/course/reader-notes.md'
        output.write_bytes(b'# Authored notes')
        before = {str(path): path.read_bytes() for path in (self.root / 'docs').rglob('*.md')}
        with self.assertRaisesRegex(PlanError, 'unowned catalogue output'):
            write_documents(self.plan, self.root)
        self.assertEqual({str(path): path.read_bytes() for path in (self.root / 'docs').rglob('*.md')}, before)
        verify_sources(self.plan, self.root)

    def test_unknown_legacy_output_is_rejected_before_any_deletion(self):
        self.materialize()
        output = self.root / 'docs/library/reader-notes.md'
        output.parent.mkdir()
        output.write_bytes(b'# Legacy authored notes')
        before = (self.root / 'docs/index.md').read_bytes()
        with self.assertRaisesRegex(PlanError, 'unowned catalogue output'):
            write_documents(self.plan, self.root)
        self.assertEqual(output.read_bytes(), b'# Legacy authored notes')
        self.assertEqual((self.root / 'docs/index.md').read_bytes(), before)

    def test_reviewed_previous_bytes_allow_owned_retired_path_removal(self):
        self.materialize()
        output = self.root / 'docs/family/course/retired.md'
        output.write_bytes(b'# Previously generated route')
        write_documents(self.plan, self.root, previous_outputs={
            'docs/family/course/retired.md': b'# Previously generated route'})
        self.assertFalse(output.exists())
        verify_outputs(self.plan, self.root)

    def test_changed_previous_bytes_cannot_authorize_removal(self):
        self.materialize()
        output = self.root / 'docs/family/course/retired.md'
        output.write_bytes(b'# New authored bytes')
        with self.assertRaisesRegex(PlanError, 'unowned catalogue output'):
            write_documents(self.plan, self.root, previous_outputs={
                'docs/family/course/retired.md': b'# Old generated bytes'})
        self.assertEqual(output.read_bytes(), b'# New authored bytes')

    def test_prior_ownership_paths_are_validated_before_output_mutation(self):
        self.materialize()
        before = (self.root / 'docs/index.md').read_bytes()
        with self.assertRaisesRegex(PlanError, 'unsafe catalogue path'):
            write_documents(self.plan, self.root, previous_outputs={'../escape.md': b'old'})
        self.assertEqual((self.root / 'docs/index.md').read_bytes(), before)

    def test_directory_at_index_output_is_rejected_before_family_deletion(self):
        self.materialize()
        index = self.root / 'docs/index.md'
        index.unlink()
        index.mkdir()
        before = (self.root / 'docs/family/index.md').read_bytes()
        with self.assertRaisesRegex(PlanError, 'not a regular file'):
            write_documents(self.plan, self.root)
        self.assertEqual((self.root / 'docs/family/index.md').read_bytes(), before)
        self.assertTrue(index.is_dir())

    def test_absent_environment_preserves_each_owner_fallback_on_replay(self):
        originals = dict(self.originals)
        owner = 'programs/family/course/mkdocs.yml'
        originals[owner] = originals[owner].replace(b'site_name: Course', b'site_name: !ENV [SITE_URL, Course]')
        plan = build_plan(originals, environment={})
        self.assertEqual(plan.configuration.environment, ())
        self.assertEqual(build_plan(originals, environment=dict(plan.configuration.environment)), plan)
        self.assertEqual(yaml.safe_load(plan.configuration.content)['site_url'], 'https://example.org/catalogue/')

    def test_explicit_environment_replays_shared_variable_without_defaults(self):
        originals = dict(self.originals)
        owner = 'programs/family/course/mkdocs.yml'
        originals[owner] = originals[owner].replace(b'site_name: Course', b'site_name: !ENV [SITE_URL, Course]')
        plan = build_plan(originals, environment={'SITE_URL': 'https://reader.example/'})
        self.assertEqual(plan.configuration.environment, (('SITE_URL', 'https://reader.example/'),))
        self.assertEqual(build_plan(originals, environment=dict(plan.configuration.environment)), plan)

    def test_explicit_empty_environment_remains_distinct_from_absent(self):
        plan = build_plan(self.originals, environment={'SITE_URL': ''})
        self.assertEqual(plan.configuration.environment, (('SITE_URL', ''),))
        self.assertEqual(yaml.safe_load(plan.configuration.content)['site_url'], '')
        self.assertNotEqual(plan.configuration.content, self.plan.configuration.content)
        self.assertEqual(build_plan(self.originals, environment=dict(plan.configuration.environment)), plan)

    def test_environment_requires_string_names_and_values(self):
        for environment in [{'SITE_URL': None}, {1: 'value'}]:
            with self.subTest(environment=environment), self.assertRaisesRegex(PlanError, 'string names and values'):
                build_plan(self.originals, environment=environment)

    def test_unknown_fifo_is_rejected_before_generated_output_deletion(self):
        self.materialize()
        output = self.root / 'docs/family/course/reader-channel'
        os.mkfifo(output)
        before = (self.root / 'docs/index.md').read_bytes()
        with self.assertRaisesRegex(PlanError, 'unsupported catalogue output'):
            write_documents(self.plan, self.root)
        self.assertEqual((self.root / 'docs/index.md').read_bytes(), before)
        self.assertTrue(output.exists())

    def test_reviewed_previous_bytes_allow_legacy_generated_path_removal(self):
        self.materialize()
        output = self.root / 'docs/library/previous.md'
        output.parent.mkdir()
        output.write_bytes(b'# Previously generated library route')
        write_documents(self.plan, self.root, previous_outputs={
            'docs/library/previous.md': b'# Previously generated library route'})
        self.assertFalse(output.parent.exists())
        verify_outputs(self.plan, self.root)

    def test_failed_document_atomic_write_preserves_all_originals(self):
        self.materialize()
        original = self.root / 'programs/README.md'
        index = self.root / 'docs/index.md'
        index.unlink()
        os.link(original, index)
        before = capture_sources(self.root)
        with patch('scripts.catalogue.files.os.replace', side_effect=OSError('document replace unavailable')), self.assertRaisesRegex(OSError, 'document replace unavailable'):
            write_documents(self.plan, self.root)
        self.assertEqual(capture_sources(self.root), before)
        self.assertEqual(list((self.root / 'docs').rglob('.catalogue-*')), [])


    def test_atomic_configuration_replacement_preserves_existing_permissions(self):
        self.materialize()
        output = self.root / 'artifacts/mkdocs.root.yml'
        output.chmod(0o640)
        write_configuration(self.plan, self.root)
        self.assertEqual(output.stat().st_mode & 0o777, 0o640)
        verify_outputs(self.plan, self.root)


    def test_program_staging_uses_exact_planned_bytes_without_series_outputs(self):
        target = 'artifacts/program-docs/family/course'
        write_program_documents(self.plan, self.root, 'programs/family/course', target)
        expected = {item.destination.removeprefix('docs/family/course/'): item.content
                    for item in self.plan.documents if item.destination.startswith('docs/family/course/')}
        actual = {path.relative_to(self.root / target).as_posix(): path.read_bytes()
                  for path in (self.root / target).rglob('*') if path.is_file()}
        self.assertEqual(actual, expected)
        self.assertFalse((self.root / 'docs').exists())
        self.assertEqual(capture_sources(self.root), self.originals)

    def test_program_staging_refuses_unknown_courses_and_wrong_targets(self):
        for program, target in [('programs/family/missing', 'artifacts/program-docs/family/missing'),
                                ('programs/family/course', 'docs/family/course'),
                                ('programs/family/course', 'artifacts/program-docs/family/other'),
                                ('programs/family/course/course-book', 'artifacts/program-docs/family/course')]:
            with self.subTest(program=program, target=target), self.assertRaises(PlanError):
                write_program_documents(self.plan, self.root, program, target)
        self.assertFalse((self.root / 'artifacts').exists())

    def test_program_staging_checks_sources_before_and_after_materialization(self):
        target = 'artifacts/program-docs/family/course'
        (self.root / 'programs/README.md').write_bytes(b'# Changed source')
        with self.assertRaisesRegex(PlanError, 'inputs changed'):
            write_program_documents(self.plan, self.root, 'programs/family/course', target)
        self.assertFalse((self.root / target).exists())
        (self.root / 'programs/README.md').write_bytes(self.originals['programs/README.md'])
        from scripts.catalogue.files import _atomic_write
        def changed_write(root, relative, content):
            _atomic_write(root, relative, content)
            (root / 'programs/README.md').write_bytes(b'# Concurrent source change')
        with patch('scripts.catalogue.files._atomic_write', side_effect=changed_write), self.assertRaisesRegex(PlanError, 'inputs changed'):
            write_program_documents(self.plan, self.root, 'programs/family/course', target)

    def test_program_staging_preserves_unowned_bytes_and_refuses_aliases(self):
        target = self.root / 'artifacts/program-docs/family/course'
        target.mkdir(parents=True)
        unknown = target / 'unreviewed.md'
        unknown.write_bytes(b'# User work')
        with self.assertRaisesRegex(PlanError, 'unowned program staging output'):
            write_program_documents(self.plan, self.root, 'programs/family/course', target.relative_to(self.root).as_posix())
        self.assertEqual(unknown.read_bytes(), b'# User work')
        unknown.unlink()
        original = self.root / 'programs/family/course/course-book/index.md'
        alias = target / 'index.md'
        for kind in ['symlink', 'hardlink']:
            if kind == 'symlink': alias.symlink_to(original)
            else: os.link(original, alias)
            with self.subTest(kind=kind), self.assertRaises(PlanError):
                write_program_documents(self.plan, self.root, 'programs/family/course', target.relative_to(self.root).as_posix())
            self.assertEqual(original.read_bytes(), self.originals['programs/family/course/course-book/index.md'])
            alias.unlink()


if __name__ == '__main__':
    unittest.main()

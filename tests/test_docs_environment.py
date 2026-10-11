"""Exercise owned environment reuse and fail-closed lock/runtime boundaries."""
from pathlib import Path
import importlib.util
import json
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('docs_environment', ROOT / 'scripts/docs_environment.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class DocsEnvironmentTests(unittest.TestCase):
    def setUp(self):
        artifacts = ROOT / 'artifacts/qualification/docs-installer/controls'
        artifacts.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(dir=artifacts)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.lock = self.root / 'requirements.lock'
        self.requirements = self.root / 'requirements.txt'
        shutil.copy2(ROOT / 'configs/docs/requirements-docs.lock', self.lock)
        shutil.copy2(ROOT / 'configs/docs/requirements-docs.txt', self.requirements)
        self.packages = installer.locked_packages(self.lock)
        self.target = self.root / 'artifacts/docs/environment'
        self.receipt = self.root / 'artifacts/docs/receipt.json'
        self.python = self.root / 'base-python'
        self.python.write_bytes(b'controlled interpreter bytes')
        self.uv = self.root / 'uv'
        self.uv.write_bytes(b'controlled uv bytes')
        self.runtime = {**installer.VERIFICATION_RUNTIME, 'prefix': str(self.root / 'base'), 'base_prefix': str(self.root / 'base')}
        self.rows = list(self.packages.items())
        self.calls = []
        self.fail_sync = False
        self.wrong_venv = False
        self.uv_version = 'uv 0.11.17 (reviewed build metadata)'
        path_patch = mock.patch.object(installer.shutil, 'which', side_effect=lambda name: str(self.python if name == 'python-selected' else self.uv))
        path_patch.start(); self.addCleanup(path_patch.stop)
        command_patch = mock.patch.object(installer, 'run', side_effect=self.command)
        command_patch.start(); self.addCleanup(command_patch.stop)

    def command(self, args, *, environment):
        self.calls.append(args)
        self.assertTrue(Path(environment['UV_CACHE_DIR']).is_relative_to(self.root / 'artifacts'))
        self.assertEqual(environment['UV_PYTHON_DOWNLOADS'], 'never')
        if args[-1] == installer.PROBE:
            if args[0] == str(self.python):
                return json.dumps(self.runtime)
            return json.dumps({**self.runtime, 'prefix': str(self.root / 'wrong' if self.wrong_venv else self.target)})
        if args[-1] == '--version':
            return self.uv_version
        if 'venv' in args:
            (self.target / 'bin').mkdir()
            (self.target / 'bin/python').symlink_to(self.python)
            self.assertIn('--without-pip', args)
            return ''
        if 'sync' in args:
            self.assertIn('--require-hashes', args)
            self.assertIn('--no-config', args)
            if self.fail_sync:
                raise RuntimeError('controlled interrupted install')
            return ''
        if args[-1] == installer.PACKAGES:
            return json.dumps(self.rows)
        if 'check' in args:
            return ''
        raise AssertionError(args)

    def prepare(self, *, install=True):
        return installer.prepare(self.root, 'python-selected', self.target, self.lock,
                                 self.requirements, 'uv-selected', self.receipt, install=install)

    def test_new_environment_uses_stdlib_without_pip_and_hashed_sync(self):
        receipt = self.prepare()
        self.assertEqual(receipt['status'], 'ready')
        self.assertEqual(receipt['package_count'], 43)
        self.assertFalse(receipt['publication_approved'])
        self.assertEqual(sum('venv' in args for args in self.calls), 1)
        self.assertEqual(sum('sync' in args for args in self.calls), 1)
        self.assertEqual(json.loads(self.receipt.read_text()), receipt)

    def test_ready_environment_reuses_without_recreation_or_upgrade(self):
        self.prepare()
        self.calls.clear()
        before = (self.target / installer.MARKER).read_bytes()
        self.prepare()
        self.assertFalse(any('venv' in args or 'sync' in args for args in self.calls))
        self.assertEqual((self.target / installer.MARKER).read_bytes(), before)

    def test_prepare_only_defers_install_and_is_resumable(self):
        self.assertEqual(self.prepare(install=False)['status'], 'preparing')
        self.assertFalse(any('sync' in args for args in self.calls))
        self.calls.clear()
        self.assertEqual(self.prepare()['status'], 'ready')
        self.assertFalse(any('venv' in args for args in self.calls))

    def test_interrupted_owned_install_resumes_without_deleting_environment(self):
        self.fail_sync = True
        with self.assertRaisesRegex(RuntimeError, 'interrupted install'):
            self.prepare()
        sentinel = self.target / 'retained-output'
        sentinel.write_bytes(b'preserved')
        self.fail_sync = False
        self.calls.clear()
        self.prepare()
        self.assertEqual(sentinel.read_bytes(), b'preserved')
        self.assertFalse(any('venv' in args for args in self.calls))

    def test_existing_unowned_environment_is_not_modified(self):
        self.target.mkdir(parents=True)
        sentinel = self.target / 'user-content';sentinel.write_bytes(b'user data')
        with self.assertRaisesRegex(RuntimeError, 'unowned environment'):
            self.prepare()
        self.assertEqual(list(self.target.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b'user data')
        self.assertFalse(any('venv' in args or 'sync' in args for args in self.calls))

    def test_stale_lock_or_declared_ranges_never_mutate_owned_environment(self):
        self.prepare()
        for path in (self.lock, self.requirements):
            before = path.read_bytes();path.write_bytes(before + b'\n# changed source\n')
            self.calls.clear()
            with self.subTest(path=path), self.assertRaisesRegex(RuntimeError, 'stale documentation environment'):
                self.prepare()
            self.assertFalse(any('venv' in args or 'sync' in args for args in self.calls))
            path.write_bytes(before)

    def test_wrong_runtime_or_nonbase_interpreter_rejects_before_environment_creation(self):
        original = dict(self.runtime)
        for changes in ({'version':'3.11.0'}, {'system':'Linux'}, {'prefix':str(self.root/'another-venv')}):
            self.runtime = {**original, **changes}
            with self.subTest(changes=changes), self.assertRaisesRegex(RuntimeError, 'base CPython'):
                self.prepare()
            self.assertFalse(self.target.exists())

    def test_uv_version_mismatch_rejects_before_environment_creation(self):
        self.uv_version = 'uv 0.11.18'
        with self.assertRaisesRegex(RuntimeError, 'requires uv 0.11.17'):
            self.prepare()
        self.assertFalse(self.target.exists())

    def test_wrong_ready_interpreter_does_not_trigger_repair(self):
        self.prepare();self.wrong_venv = True;self.calls.clear()
        with self.assertRaisesRegex(RuntimeError, 'mismatched interpreter'):
            self.prepare()
        self.assertFalse(any('venv' in args or 'sync' in args for args in self.calls))

    def test_missing_ready_interpreter_is_not_recreated(self):
        self.prepare();(self.target/'bin/python').unlink();self.calls.clear()
        with self.assertRaisesRegex(RuntimeError, 'interpreter is missing'):
            self.prepare()
        self.assertFalse(any('venv' in args or 'sync' in args for args in self.calls))

    def test_package_drift_missing_extra_or_duplicate_is_not_silently_resynced(self):
        self.prepare();original=list(self.rows)
        for rows in (original[1:], [*original, ('author-package','1.0')], [*original, original[0]], [(original[0][0],'0.0'),*original[1:]]):
            self.rows=rows;self.calls.clear()
            with self.subTest(rows=len(rows)), self.assertRaisesRegex(RuntimeError, 'installed packages'):
                self.prepare()
            self.assertFalse(any('sync' in args for args in self.calls))

    def test_preparing_environment_retains_user_package_changes(self):
        self.prepare(install=False)
        self.rows.append(('author-package', '1.0'))
        self.calls.clear()
        with self.assertRaisesRegex(RuntimeError, 'must not remove user changes'):
            self.prepare()
        self.assertFalse(any('sync' in args for args in self.calls))
        self.assertEqual(json.loads((self.target / installer.MARKER).read_text())['status'], 'preparing')

    def test_missing_or_malformed_download_hashes_reject_before_environment_creation(self):
        before=self.lock.read_text()
        for contents in ('mkdocs==1.6.1\n', before.replace('--hash=sha256:', '--hash=sha1:', 1), before+'\\'):
            self.lock.write_text(contents)
            with self.subTest(contents=contents[:40]), self.assertRaises(RuntimeError):
                self.prepare()
            self.assertFalse(self.target.exists())

    def test_authored_plugin_and_version_ranges_are_preserved(self):
        before=self.requirements.read_text()
        for contents in (before.replace('mkdocs-material>=9.7.7,<10','mkdocs-material>=9.8,<10'),before+'mkdocs-extra-plugin>=1,<2\n',before.replace('mkdocs-autorefs>=1.4.4,<2\n','')):
            self.requirements.write_text(contents)
            with self.subTest(contents=contents), self.assertRaises(RuntimeError):
                self.prepare()
            self.assertFalse(self.target.exists())

    def test_symlink_and_outside_artifact_paths_reject(self):
        outside=self.root/'outside';outside.mkdir()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(outside,target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError,'symlinked'):
            self.prepare()
        self.target.unlink();self.target=outside
        with self.assertRaisesRegex(RuntimeError,'inside repository artifacts'):
            self.prepare()
        self.assertEqual(list(outside.iterdir()),[])

    def test_receipt_cannot_overwrite_environment_marker(self):
        self.receipt=self.target/installer.MARKER
        with self.assertRaisesRegex(RuntimeError,'overwrite environment content'):
            self.prepare()
        self.assertFalse(self.target.exists())


if __name__ == '__main__':
    unittest.main()

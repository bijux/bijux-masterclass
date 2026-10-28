import subprocess
import tempfile
import unittest
from pathlib import Path
from atlas_delivery.gitrepo import commit, current_commit, graph, run_git

class GitHistoryTests(unittest.TestCase):
    def test_local_history_and_revert(self):
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d)
            subprocess.run(['git','init','-q',repo],check=True)
            run_git(repo,'config','user.email','course@example.invalid')
            run_git(repo,'config','user.name','Course')
            (repo/'release.txt').write_text('v1\n')
            first=commit(repo,'release v1')
            (repo/'release.txt').write_text('v2\n')
            second=commit(repo,'release v2')
            self.assertNotEqual(first,second)
            self.assertEqual(current_commit(repo),second)
            run_git(repo,'revert','--no-edit',second)
            self.assertEqual((repo/'release.txt').read_text(),'v1\n')
            self.assertIn('revert',graph(repo).lower())

if __name__=='__main__': unittest.main()

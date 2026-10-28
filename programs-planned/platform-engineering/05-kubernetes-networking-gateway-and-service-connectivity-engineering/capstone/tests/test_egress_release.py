import unittest
from atlas_net.egress import classify,validate_destination,validate_redirect
from atlas_net.release import Gate,classify as release_classify

class EgressReleaseTests(unittest.TestCase):
    def test_classification(self):
        self.assertEqual(classify('127.0.0.1'),'loopback'); self.assertEqual(classify('169.254.169.254'),'link-local')
    def test_safe_destination(self):
        d=validate_destination('https://updates.example.invalid/a',['203.0.113.9'],'203.0.113.9',allowed_hosts={'updates.example.invalid'})
        # Documentation prefixes are reserved, so course fixture must be explicitly allowed.
        self.assertFalse(d.allowed)
        d=validate_destination('https://updates.example.invalid/a',['203.0.113.9'],'203.0.113.9',allowed_hosts={'updates.example.invalid'},allowed_private={'203.0.113.9'})
        self.assertTrue(d.allowed)
    def test_peer_mismatch(self):
        d=validate_destination('https://updates.example.invalid/a',['198.51.100.2'],'127.0.0.1',allowed_hosts={'updates.example.invalid'})
        self.assertFalse(d.allowed)
    def test_redirect(self):
        self.assertFalse(validate_redirect('https://updates.example.invalid/a','http://127.0.0.1/x',allowed_hosts={'updates.example.invalid'}).allowed)
    def test_release_states(self):
        self.assertEqual(release_classify([Gate('a','pass')]),'accepted')
        self.assertEqual(release_classify([Gate('a','fail')]),'rejected')
        self.assertEqual(release_classify([Gate('a','not-executed')]),'not-executed')
        self.assertEqual(release_classify([Gate('a','not-executed',False)]),'accepted')

if __name__=='__main__': unittest.main()

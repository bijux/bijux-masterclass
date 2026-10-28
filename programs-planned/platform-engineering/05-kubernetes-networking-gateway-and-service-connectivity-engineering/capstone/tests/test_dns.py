import unittest
from atlas_net.dns import DNSAuthority,DNSCache,expand_name

class DNSTests(unittest.TestCase):
    def test_negative_cache(self):
        authority=DNSAuthority(); cache=DNSCache(authority)
        first=cache.query('atlas-api.atlas-system.svc.cluster.local','A',0); self.assertEqual(first.rcode,'NXDOMAIN')
        authority.set('atlas-api.atlas-system.svc.cluster.local','A',['10.96.0.10'],30)
        self.assertEqual(cache.query('atlas-api.atlas-system.svc.cluster.local','A',5).rcode,'NXDOMAIN')
        self.assertEqual(cache.query('atlas-api.atlas-system.svc.cluster.local','A',11).values,('10.96.0.10',))
    def test_search(self):
        values=expand_name('atlas-api',['atlas-system.svc.cluster.local','svc.cluster.local'],5)
        self.assertEqual(values[0],'atlas-api.atlas-system.svc.cluster.local')
    def test_absolute(self): self.assertEqual(expand_name('atlas-api.example.',['x'],5),['atlas-api.example'])

if __name__=='__main__': unittest.main()

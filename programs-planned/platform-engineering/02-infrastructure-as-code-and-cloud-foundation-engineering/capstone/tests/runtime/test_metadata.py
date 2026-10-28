from __future__ import annotations

import unittest

from atlas_host.metadata import MetadataEndpoint, MetadataPolicyError, PROFILES, validate_metadata_endpoint


class MetadataTests(unittest.TestCase):
    def test_official_profiles_are_allowed(self) -> None:
        for profile in PROFILES.values():
            validate_metadata_endpoint(profile)

    def test_arbitrary_link_local_or_public_endpoint_is_rejected(self) -> None:
        with self.assertRaises(MetadataPolicyError):
            validate_metadata_endpoint(MetadataEndpoint("bad", "http://169.254.1.1/", None, False))
        with self.assertRaises(MetadataPolicyError):
            validate_metadata_endpoint(MetadataEndpoint("bad", "https://example.com/metadata", None, False))

    def test_userinfo_is_rejected(self) -> None:
        with self.assertRaises(MetadataPolicyError):
            validate_metadata_endpoint(MetadataEndpoint("bad", "http://user@169.254.169.254/", None, False))


if __name__ == "__main__":
    unittest.main()

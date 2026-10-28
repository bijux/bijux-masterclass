# Service-to-service security profile

Course 8 uses two complementary mechanisms:

1. **Workload identity** authenticates the calling deployment. A production system would normally derive this identity from mutually authenticated transport and an operated trust domain.
2. **A narrowly scoped capability** authorizes one artifact upload for one tenant, run, attempt, checksum, size limit, audience, and time interval.

The capability format in this capstone is a deliberately small course profile, not JWT, PASETO, OAuth, or an Internet standard. Its value is that every security property is visible and testable in both implementation tracks. The exact byte profile is defined in `capability-profile.yaml`, and the cross-language golden token is stored in `../shared/vectors/capability.json`.

The profile does not replace transport authentication. Possession of a capability is necessary for the delegated upload, while the authenticated workload identity remains necessary to reach the Artifact Service.

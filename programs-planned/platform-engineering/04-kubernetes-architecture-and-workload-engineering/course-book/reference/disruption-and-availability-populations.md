# Disruption and availability populations

Availability reasoning fails when populations are unnamed. Distinguish desired, current, updated, ready, available, healthy, endpoint-eligible, and successfully serving instances.

A PDB calculates voluntary disruption allowance from its selected healthy population and desired scale. It does not cover involuntary failures. It can block eviction but cannot make a replacement schedule or become ready.

Rollout unavailability and PDB unavailability are separate controls that can interact. A node drain during rollout may be blocked, or a permissive combination may reduce capacity more than intended. Test them together.

Availability also depends on failure domains. Three replicas on one Node are three processes but one node-level failure domain. Course 4 records placement intent; Courses 5, 6, and 9 prove network, storage, and fleet availability.

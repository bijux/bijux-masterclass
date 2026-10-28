# Tool and language strategy

Platform engineering uses the native expression of each responsibility. Course 6 uses Kubernetes and snapshot API YAML for desired state, Python for transparent controller and recovery models, Go for a filesystem durability probe, SQL and database-aware examples for transactional state, and guarded kind/CSI lanes for implementation-backed evidence. The learner is not asked to build a storage system from scratch or rewrite one mechanism in multiple application frameworks.

The governing sequence is always concept → ownership → mechanism → failure → evidence → reference implementation. Tools are selected because they expose those ideas; the curriculum does not define the ideas by one vendor tool.

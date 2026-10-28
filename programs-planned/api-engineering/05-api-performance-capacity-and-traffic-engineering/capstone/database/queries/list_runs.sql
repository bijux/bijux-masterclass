-- Stable owner-authorized, status-filtered, high-water keyset traversal.
SELECT
    id,
    project_id,
    dataset_id,
    owner_id,
    status,
    progress,
    version,
    created_at,
    updated_at,
    result_summary
FROM analysis_runs
WHERE owner_id = %(owner_id)s
  AND status = %(status)s
  AND (created_at, id) < (%(boundary_created_at)s, %(boundary_id)s)
  AND (created_at, id) <= (%(snapshot_created_at)s, %(snapshot_id)s)
ORDER BY created_at DESC, id DESC
LIMIT %(page_size)s;

-- Backfill: deterministic and idempotent for already-completed runs.
UPDATE analysis_runs AS run
SET result_summary = jsonb_build_object(
    'algorithm', run.parameters->>'algorithm',
    'artifactCount', (
        SELECT count(*)
        FROM artifacts AS artifact
        WHERE artifact.run_id = run.id
    )
)
WHERE run.status = 'completed'
  AND run.result_summary IS NULL;

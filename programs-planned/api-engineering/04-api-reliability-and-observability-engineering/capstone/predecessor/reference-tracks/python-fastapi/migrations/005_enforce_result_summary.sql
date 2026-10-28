-- Enforcement phase: run only after old writers are drained and the backfill is complete.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM analysis_runs
        WHERE status = 'completed'
          AND result_summary IS NULL
    ) THEN
        RAISE EXCEPTION
            'enforcement phase blocked: completed rows without result_summary remain';
    END IF;
END
$$;

ALTER TABLE analysis_runs
    ADD CONSTRAINT result_summary_matches_run_state
    CHECK (
        (status <> 'completed' AND result_summary IS NULL)
        OR
        (
            status = 'completed'
            AND jsonb_typeof(result_summary) = 'object'
            AND result_summary ? 'algorithm'
            AND result_summary ? 'artifactCount'
            AND result_summary->>'algorithm' IN (
                'quality-summary',
                'line-count',
                'checksum'
            )
            AND result_summary->>'artifactCount' ~ '^[0-9]+$'
            AND (result_summary->>'artifactCount')::bigint >= 0
            AND jsonb_object_length(result_summary) = 2
        )
    ) NOT VALID;

ALTER TABLE analysis_runs
    VALIDATE CONSTRAINT result_summary_matches_run_state;

CREATE INDEX analysis_runs_result_algorithm_idx
    ON analysis_runs ((result_summary->>'algorithm'))
    WHERE result_summary IS NOT NULL;

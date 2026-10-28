-- Expand: service 1.0 processes implementing API 1.1.0 remain valid.
ALTER TABLE analysis_runs
    ADD COLUMN result_summary jsonb;

COMMENT ON COLUMN analysis_runs.result_summary IS
    'Nullable during service 1.0/service 1.1 coexistence; written by service 1.1.';

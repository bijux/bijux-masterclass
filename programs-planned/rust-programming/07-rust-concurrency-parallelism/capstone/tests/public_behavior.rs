use batchweave::{
    EngineConfig, FailurePolicy, Job, JobId, Operation, OutcomeKind, parse_manifest,
    render_report, run_jobs,
};

#[test]
fn public_pipeline_preserves_manifest_order_across_worker_counts() {
    let input = "BATCHWEAVE-V1\na\tprime-count\t50000\nb\tword-count\tone two\nc\tsort-integers\t8,1,4\n";
    let jobs = parse_manifest(input).expect("manifest");
    let serial = run_jobs(
        jobs.clone(),
        EngineConfig::new(1, 1, 1, FailurePolicy::Continue).expect("config"),
    )
    .expect("serial run");
    let concurrent = run_jobs(
        jobs,
        EngineConfig::new(3, 2, 2, FailurePolicy::Continue).expect("config"),
    )
    .expect("concurrent run");
    assert_eq!(serial.outcomes, concurrent.outcomes);
    assert_eq!(render_report(&serial), render_report(&concurrent));
}

#[test]
fn validation_rejects_duplicate_ids_before_spawning_workers() {
    let duplicate = JobId::new("same").expect("id");
    let jobs = vec![
        Job {
            index: 0,
            id: duplicate.clone(),
            operation: Operation::Checksum,
            payload: "a".to_owned(),
        },
        Job {
            index: 1,
            id: duplicate,
            operation: Operation::Checksum,
            payload: "b".to_owned(),
        },
    ];
    let error = run_jobs(jobs, EngineConfig::default()).expect_err("duplicate rejected");
    assert!(error.to_string().contains("duplicate job id"));
}

#[test]
fn continue_policy_records_domain_failures_without_losing_later_jobs() {
    let input = "BATCHWEAVE-V1\nbad\tsort-integers\t1,nope\ngood\tchecksum\tstill processed\n";
    let report = run_jobs(
        parse_manifest(input).expect("manifest"),
        EngineConfig::new(2, 1, 1, FailurePolicy::Continue).expect("config"),
    )
    .expect("run");
    assert!(matches!(&report.outcomes[0].kind, OutcomeKind::DomainFailed(_)));
    assert!(matches!(&report.outcomes[1].kind, OutcomeKind::Completed(_)));
}

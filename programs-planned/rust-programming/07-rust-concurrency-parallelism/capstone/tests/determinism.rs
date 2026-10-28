use batchweave::{
    EngineConfig, FailurePolicy, parse_manifest, render_report, run_jobs,
};

#[test]
fn report_is_identical_for_multiple_supported_schedules() {
    let input = "BATCHWEAVE-V1\na\tprime-count\t75000\nb\tchecksum\talpha\nc\tword-count\tone two three\nd\tsort-integers\t5,4,3,2,1\ne\tprime-count\t30000\n";
    let jobs = parse_manifest(input).expect("manifest");
    let mut reports = Vec::new();
    for (workers, queue, report_threads) in [(1, 1, 1), (2, 1, 2), (4, 3, 3)] {
        let report = run_jobs(
            jobs.clone(),
            EngineConfig::new(
                workers,
                queue,
                report_threads,
                FailurePolicy::Continue,
            )
            .expect("config"),
        )
        .expect("run");
        reports.push(render_report(&report));
    }
    assert!(reports.windows(2).all(|pair| pair[0] == pair[1]));
}


#[test]
fn parallel_report_path_matches_across_pool_widths() {
    let mut input = String::from("BATCHWEAVE-V1\n");
    for index in 0..256 {
        input.push_str(&format!("job-{index}\tchecksum\tpayload-{index}\n"));
    }
    let jobs = parse_manifest(&input).expect("manifest");
    let one = run_jobs(
        jobs.clone(),
        EngineConfig::new(4, 8, 1, FailurePolicy::Continue).expect("config"),
    )
    .expect("run");
    let many = run_jobs(
        jobs,
        EngineConfig::new(4, 8, 4, FailurePolicy::Continue).expect("config"),
    )
    .expect("run");
    assert_eq!(one.outcomes, many.outcomes);
    assert_eq!(one.summary, many.summary);
}

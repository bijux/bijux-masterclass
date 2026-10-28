use metricrail::config::Config;
use metricrail::load::{LoadOptions, LoadOutcome, run};
use metricrail::server;
use std::time::Duration;

#[tokio::test]
async fn load_runner_bounds_concurrency_and_preserves_source_order() {
    let server = server::spawn("127.0.0.1:0", Config::default())
        .await
        .expect("server");
    let records = vec![
        "b\tm\t1\t1".to_owned(),
        "a\tm\t1\t2".to_owned(),
        "c\tm\t1\t3".to_owned(),
    ];
    let report = run(
        &server.address.to_string(),
        records,
        LoadOptions {
            connections: 2,
            request_timeout: Duration::from_secs(2),
            max_line_bytes: 4096,
        },
    )
    .await
    .expect("load report");

    assert_eq!(report.offered, 3);
    assert_eq!(report.completed, 3);
    let indices: Vec<_> = report
        .outcomes
        .iter()
        .map(|outcome| match outcome {
            LoadOutcome::Completed { index, .. }
            | LoadOutcome::Rejected { index, .. }
            | LoadOutcome::Failed { index, .. } => *index,
        })
        .collect();
    assert_eq!(indices, vec![0, 1, 2]);
    server.shutdown().await.expect("shutdown");
}

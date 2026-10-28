use jobwire::{start_service, Config, JobWireClient, Operation};
use std::time::Duration;

#[tokio::test]
async fn duplicate_while_in_progress_shares_terminal_outcome() {
    let config = Config {
        tcp_addr: "127.0.0.1:0".parse().unwrap(),
        http_addr: "127.0.0.1:0".parse().unwrap(),
        max_active_jobs: 1,
        max_sleep: Duration::from_secs(1),
        ..Config::default()
    };
    let service = start_service(config).await.unwrap();
    let address = service.tcp_addr;

    let first = async move {
        let mut client = JobWireClient::connect(address, 64 * 1024, Duration::from_secs(2))
            .await
            .unwrap();
        client
            .submit(
                "r-1".to_owned(),
                "same-key".to_owned(),
                Operation::SleepMs,
                "50".to_owned(),
            )
            .await
            .unwrap()
    };
    let second = async move {
        tokio::task::yield_now().await;
        let mut client = JobWireClient::connect(address, 64 * 1024, Duration::from_secs(2))
            .await
            .unwrap();
        client
            .submit(
                "r-2".to_owned(),
                "same-key".to_owned(),
                Operation::SleepMs,
                "50".to_owned(),
            )
            .await
            .unwrap()
    };
    let (a, b) = tokio::join!(first, second);
    assert_eq!(a, b);
    service.shutdown().await.unwrap();
}

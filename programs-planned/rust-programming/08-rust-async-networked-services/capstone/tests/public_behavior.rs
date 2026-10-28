use jobwire::{start_service, Config, JobWireClient, Operation};
use std::time::Duration;

fn test_config() -> Config {
    Config {
        tcp_addr: "127.0.0.1:0".parse().unwrap(),
        http_addr: "127.0.0.1:0".parse().unwrap(),
        request_timeout: Duration::from_secs(2),
        shutdown_grace: Duration::from_secs(1),
        ..Config::default()
    }
}

#[tokio::test]
async fn submit_and_replay_one_semantic_result() {
    let service = start_service(test_config()).await.unwrap();
    let mut first = JobWireClient::connect(service.tcp_addr, 64 * 1024, Duration::from_secs(2))
        .await
        .unwrap();
    let result = first
        .submit(
            "r-1".to_owned(),
            "key-1".to_owned(),
            Operation::Uppercase,
            "hello".to_owned(),
        )
        .await
        .unwrap();
    assert_eq!(result.value, "HELLO");

    let mut second = JobWireClient::connect(service.tcp_addr, 64 * 1024, Duration::from_secs(2))
        .await
        .unwrap();
    let replay = second
        .submit(
            "r-2".to_owned(),
            "key-1".to_owned(),
            Operation::Uppercase,
            "hello".to_owned(),
        )
        .await
        .unwrap();
    assert_eq!(replay, result);
    service.shutdown().await.unwrap();
}

#[tokio::test]
async fn key_reuse_with_changed_content_is_rejected() {
    let service = start_service(test_config()).await.unwrap();
    let mut client = JobWireClient::connect(service.tcp_addr, 64 * 1024, Duration::from_secs(2))
        .await
        .unwrap();
    client
        .submit(
            "r-1".to_owned(),
            "key-1".to_owned(),
            Operation::Uppercase,
            "hello".to_owned(),
        )
        .await
        .unwrap();
    let error = client
        .submit(
            "r-2".to_owned(),
            "key-1".to_owned(),
            Operation::Uppercase,
            "changed".to_owned(),
        )
        .await
        .unwrap_err();
    assert!(error.to_string().contains("IDEMPOTENCY_CONFLICT"));
    service.shutdown().await.unwrap();
}

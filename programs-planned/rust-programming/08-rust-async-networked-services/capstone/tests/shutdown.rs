use jobwire::{start_service, Config, JobWireClient};
use std::time::Duration;

#[tokio::test]
async fn shutdown_terminates_idle_connections_and_joins_service_tasks() {
    let service = start_service(Config {
        tcp_addr: "127.0.0.1:0".parse().unwrap(),
        http_addr: "127.0.0.1:0".parse().unwrap(),
        shutdown_grace: Duration::from_millis(100),
        ..Config::default()
    }).await.unwrap();
    let _idle = JobWireClient::connect(service.tcp_addr, 64 * 1024, Duration::from_secs(1))
        .await
        .unwrap();
    tokio::time::timeout(Duration::from_secs(1), service.shutdown())
        .await
        .expect("shutdown should be bounded")
        .unwrap();
}

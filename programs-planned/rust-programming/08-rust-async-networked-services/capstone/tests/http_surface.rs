use jobwire::{start_service, Config};
use tokio::{io::{AsyncReadExt, AsyncWriteExt}, net::TcpStream};

#[tokio::test]
async fn health_and_stats_are_deterministic_operational_surfaces() {
    let service = start_service(Config {
        tcp_addr: "127.0.0.1:0".parse().unwrap(),
        http_addr: "127.0.0.1:0".parse().unwrap(),
        ..Config::default()
    }).await.unwrap();

    let health = get(service.http_addr, "/health").await;
    assert!(health.starts_with("HTTP/1.1 200"));
    assert!(health.ends_with("state=ready\n"));

    let stats = get(service.http_addr, "/stats").await;
    assert!(stats.starts_with("HTTP/1.1 200"));
    assert!(stats.contains("active_jobs=0\n"));
    assert!(stats.contains("queued_jobs=0\n"));
    service.shutdown().await.unwrap();
}

async fn get(address: std::net::SocketAddr, path: &str) -> String {
    let mut stream = TcpStream::connect(address).await.unwrap();
    let request = format!("GET {path} HTTP/1.1\r\nHost: test\r\nConnection: close\r\n\r\n");
    stream.write_all(request.as_bytes()).await.unwrap();
    let mut response = Vec::new();
    stream.read_to_end(&mut response).await.unwrap();
    String::from_utf8(response).unwrap()
}

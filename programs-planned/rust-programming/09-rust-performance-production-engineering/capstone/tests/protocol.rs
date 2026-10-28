use metricrail::config::Config;
use metricrail::server;
use std::time::Duration;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpStream;
use tokio::time::timeout;

async fn read_line(reader: &mut BufReader<tokio::net::tcp::OwnedReadHalf>) -> String {
    let mut line = String::new();
    timeout(Duration::from_secs(2), reader.read_line(&mut line))
        .await
        .expect("response deadline")
        .expect("response read");
    line
}

#[tokio::test]
async fn service_ingests_and_returns_a_snapshot() {
    let server = server::spawn("127.0.0.1:0", Config::default())
        .await
        .expect("server");
    let stream = TcpStream::connect(server.address).await.expect("connect");
    let (read, mut write) = stream.into_split();
    let mut reader = BufReader::new(read);

    write
        .write_all(b"INGEST\tacme\trequests\t1\t2\n")
        .await
        .expect("write ingest");
    let mut line = read_line(&mut reader).await;
    assert_eq!(line.trim_end(), "OK");

    write
        .write_all(b"SNAPSHOT\n")
        .await
        .expect("write snapshot");
    line = read_line(&mut reader).await;
    assert_eq!(line.trim_end(), "SNAPSHOT-BEGIN\t1");
    line = read_line(&mut reader).await;
    assert!(line.starts_with("acme\trequests\t1\t2"));
    line = read_line(&mut reader).await;
    assert_eq!(line.trim_end(), "SNAPSHOT-END");

    write.write_all(b"QUIT\n").await.expect("write quit");
    line = read_line(&mut reader).await;
    assert_eq!(line.trim_end(), "BYE");
    server.shutdown().await.expect("shutdown");
}

#[tokio::test]
async fn invalid_input_is_not_echoed() {
    let server = server::spawn("127.0.0.1:0", Config::default())
        .await
        .expect("server");
    let stream = TcpStream::connect(server.address).await.expect("connect");
    let (read, mut write) = stream.into_split();
    let mut reader = BufReader::new(read);
    write
        .write_all(b"SECRET-PAYLOAD\n")
        .await
        .expect("write");
    let line = read_line(&mut reader).await;
    assert_eq!(
        line.trim_end(),
        "ERR\tUNKNOWN_COMMAND\tunsupported command"
    );
    assert!(!line.contains("SECRET-PAYLOAD"));
    drop(write);
    server.shutdown().await.expect("shutdown");
}

#[tokio::test]
async fn health_reports_authoritative_series_count() {
    let server = server::spawn("127.0.0.1:0", Config::default())
        .await
        .expect("server");
    let stream = TcpStream::connect(server.address).await.expect("connect");
    let (read, mut write) = stream.into_split();
    let mut reader = BufReader::new(read);

    write
        .write_all(b"INGEST\ta\tb\t1\t1\nHEALTH\n")
        .await
        .expect("write");
    assert_eq!(read_line(&mut reader).await.trim_end(), "OK");
    let health = read_line(&mut reader).await;
    assert!(health.starts_with("HEALTHY\t"));
    assert!(health.ends_with("\t1\n"));

    drop(write);
    server.shutdown().await.expect("shutdown");
}

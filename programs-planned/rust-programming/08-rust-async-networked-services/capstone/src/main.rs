use jobwire::{
    client::submit_with_retry,
    start_service,
    Config,
    JobWireClient,
    Operation,
};
use std::{env, error::Error, net::SocketAddr, process::ExitCode};
use tokio::{io::{AsyncReadExt, AsyncWriteExt}, net::TcpStream};

#[tokio::main]
async fn main() -> ExitCode {
    match run().await {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("jobwire: {error}");
            ExitCode::from(2)
        }
    }
}

async fn run() -> Result<(), Box<dyn Error>> {
    let mut args = env::args().skip(1);
    match args.next().as_deref() {
        Some("serve") => serve(args.collect()).await,
        Some("submit") => {
            let address = parse_addr(args.next(), "address")?;
            let request_id = required(args.next(), "request id")?;
            let key = required(args.next(), "idempotency key")?;
            let operation: Operation = required(args.next(), "operation")?
                .parse()
                .map_err(|message: &'static str| std::io::Error::new(std::io::ErrorKind::InvalidInput, message))?;
            let payload = required(args.next(), "payload")?;
            let mut client = JobWireClient::connect(address, 64 * 1024, std::time::Duration::from_secs(3)).await?;
            let result = client.submit(request_id, key, operation, payload).await?;
            println!("{}", result.value);
            Ok(())
        }
        Some("retry-submit") => {
            let address = parse_addr(args.next(), "address")?;
            let key = required(args.next(), "idempotency key")?;
            let operation: Operation = required(args.next(), "operation")?
                .parse()
                .map_err(|message: &'static str| std::io::Error::new(std::io::ErrorKind::InvalidInput, message))?;
            let payload = required(args.next(), "payload")?;
            let result = submit_with_retry(
                address,
                64 * 1024,
                key,
                operation,
                payload,
                Default::default(),
            ).await?;
            println!("{}", result.value);
            Ok(())
        }
        Some("stats") => {
            let address = parse_addr(args.next(), "address")?;
            let request_id = required(args.next(), "request id")?;
            let mut client = JobWireClient::connect(address, 64 * 1024, std::time::Duration::from_secs(3)).await?;
            let stats = client.stats(request_id).await?;
            println!("active_jobs={}", stats.active_jobs);
            println!("queued_jobs={}", stats.queued_jobs);
            println!("records={}", stats.records);
            println!("completed_jobs={}", stats.completed_jobs);
            println!("failed_jobs={}", stats.failed_jobs);
            Ok(())
        }
        Some("ping") => {
            let address = parse_addr(args.next(), "address")?;
            let request_id = required(args.next(), "request id")?;
            let mut client = JobWireClient::connect(address, 64 * 1024, std::time::Duration::from_secs(3)).await?;
            client.ping(request_id).await?;
            println!("pong");
            Ok(())
        }
        Some("health") => {
            let address = parse_addr(args.next(), "HTTP address")?;
            print_http_health(address).await
        }
        Some("demo") => demo().await,
        Some("version") => {
            println!("jobwire {}", env!("CARGO_PKG_VERSION"));
            Ok(())
        }
        Some("help") | None => {
            print_help();
            Ok(())
        }
        Some(other) => Err(format!("unknown command {other:?}; run jobwire help").into()),
    }
}

async fn serve(arguments: Vec<String>) -> Result<(), Box<dyn Error>> {
    let mut config = Config::default();
    let mut index = 0;
    while index < arguments.len() {
        match arguments[index].as_str() {
            "--tcp" if index + 1 < arguments.len() => {
                config.tcp_addr = arguments[index + 1].parse()?;
                index += 2;
            }
            "--http" if index + 1 < arguments.len() => {
                config.http_addr = arguments[index + 1].parse()?;
                index += 2;
            }
            other => return Err(format!("invalid serve argument {other:?}").into()),
        }
    }
    let service = start_service(config).await?;
    println!("TCP {}", service.tcp_addr);
    println!("HTTP {}", service.http_addr);
    tokio::signal::ctrl_c().await?;
    service.shutdown().await?;
    Ok(())
}

async fn print_http_health(address: SocketAddr) -> Result<(), Box<dyn Error>> {
    let mut stream = TcpStream::connect(address).await?;
    let request = format!(
        "GET /health HTTP/1.1\r\nHost: {address}\r\nConnection: close\r\n\r\n"
    );
    stream.write_all(request.as_bytes()).await?;
    let mut response = Vec::new();
    stream.read_to_end(&mut response).await?;
    print!("{}", String::from_utf8_lossy(&response));
    Ok(())
}

async fn demo() -> Result<(), Box<dyn Error>> {
    let config = Config {
        tcp_addr: "127.0.0.1:0".parse()?,
        http_addr: "127.0.0.1:0".parse()?,
        ..Config::default()
    };
    let service = start_service(config).await?;
    let mut client = JobWireClient::connect(
        service.tcp_addr,
        64 * 1024,
        std::time::Duration::from_secs(3),
    )
    .await?;
    let result = client
        .submit(
            "demo-1".to_owned(),
            "demo-key".to_owned(),
            Operation::Uppercase,
            "hello async rust".to_owned(),
        )
        .await?;
    println!("result={}", result.value);
    let stats = client.stats("demo-2".to_owned()).await?;
    println!("completed_jobs={}", stats.completed_jobs);
    client.quit().await?;
    service.shutdown().await?;
    Ok(())
}

fn parse_addr(value: Option<String>, name: &str) -> Result<SocketAddr, Box<dyn Error>> {
    Ok(required(value, name)?.parse()?)
}

fn required(value: Option<String>, name: &str) -> Result<String, Box<dyn Error>> {
    value.ok_or_else(|| format!("missing {name}").into())
}

fn print_help() {
    println!("jobwire serve [--tcp ADDRESS] [--http ADDRESS]");
    println!("jobwire submit ADDRESS REQUEST_ID IDEMPOTENCY_KEY OPERATION PAYLOAD");
    println!("jobwire retry-submit ADDRESS IDEMPOTENCY_KEY OPERATION PAYLOAD");
    println!("jobwire stats ADDRESS REQUEST_ID");
    println!("jobwire ping ADDRESS REQUEST_ID");
    println!("jobwire health HTTP_ADDRESS");
    println!("jobwire demo | help | version");
}

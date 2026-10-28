use std::{io, net::SocketAddr, sync::Arc, time::Duration};
use tokio::{
    io::{AsyncReadExt, AsyncWriteExt},
    net::{TcpListener, TcpStream},
    sync::Semaphore,
    task::{JoinHandle, JoinSet},
    time,
};
use tokio_util::sync::CancellationToken;

#[derive(Debug, Clone)]
pub struct EchoLimits {
    pub max_connections: usize,
    pub idle: Duration,
    pub write_stall: Duration,
    pub shutdown_grace: Duration,
}

impl EchoLimits {
    pub fn validate(&self) -> io::Result<()> {
        if !(1..=16).contains(&self.max_connections) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "max_connections must be in 1..=16",
            ));
        }
        for (name, value) in [
            ("idle", self.idle),
            ("write_stall", self.write_stall),
            ("shutdown_grace", self.shutdown_grace),
        ] {
            if value.is_zero() {
                return Err(io::Error::new(
                    io::ErrorKind::InvalidInput,
                    format!("{name} must be nonzero"),
                ));
            }
        }
        Ok(())
    }
}

pub struct EchoService {
    pub address: SocketAddr,
    cancellation: CancellationToken,
    task: JoinHandle<io::Result<()>>,
}

impl EchoService {
    pub async fn shutdown(self) -> io::Result<()> {
        self.cancellation.cancel();
        self.task.await.map_err(io::Error::other)?
    }
}

pub async fn start(limits: EchoLimits) -> io::Result<EchoService> {
    limits.validate()?;
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let address = listener.local_addr()?;
    let cancellation = CancellationToken::new();
    let child = cancellation.clone();
    let task = tokio::spawn(async move { run(listener, limits, child).await });
    Ok(EchoService {
        address,
        cancellation,
        task,
    })
}

async fn run(
    listener: TcpListener,
    limits: EchoLimits,
    cancellation: CancellationToken,
) -> io::Result<()> {
    let permits = Arc::new(Semaphore::new(limits.max_connections));
    let mut connections = JoinSet::new();
    let mut fatal = None;

    loop {
        let permit = tokio::select! {
            () = cancellation.cancelled() => break,
            acquired = Arc::clone(&permits).acquire_owned() => match acquired {
                Ok(permit) => permit,
                Err(_) => break,
            },
        };

        let accepted = tokio::select! {
            () = cancellation.cancelled() => {
                drop(permit);
                break;
            }
            accepted = listener.accept() => accepted,
        };

        match accepted {
            Ok((stream, _peer)) => {
                let child = cancellation.child_token();
                let idle = limits.idle;
                let write_stall = limits.write_stall;
                let _abort_handle = connections.spawn(async move {
                    let _permit = permit;
                    serve_connection(stream, idle, write_stall, child).await
                });
            }
            Err(error) => {
                drop(permit);
                fatal = Some(error);
                break;
            }
        }
    }

    cancellation.cancel();
    let drained = time::timeout(limits.shutdown_grace, async {
        while connections.join_next().await.is_some() {}
    })
    .await;
    if drained.is_err() {
        connections.abort_all();
        while connections.join_next().await.is_some() {}
    }

    match fatal {
        Some(error) => Err(error),
        None => Ok(()),
    }
}

async fn serve_connection(
    mut stream: TcpStream,
    idle: Duration,
    write_stall: Duration,
    cancellation: CancellationToken,
) -> io::Result<()> {
    let mut buffer = [0_u8; 1024];
    loop {
        let count = tokio::select! {
            () = cancellation.cancelled() => return Ok(()),
            read = time::timeout(idle, stream.read(&mut buffer)) => {
                read.map_err(|_| io::Error::new(io::ErrorKind::TimedOut, "idle read deadline"))??
            }
        };
        if count == 0 {
            return Ok(());
        }
        time::timeout(write_stall, stream.write_all(&buffer[..count]))
            .await
            .map_err(|_| io::Error::new(io::ErrorKind::TimedOut, "write deadline"))??;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn limits() -> EchoLimits {
        EchoLimits {
            max_connections: 2,
            idle: Duration::from_millis(100),
            write_stall: Duration::from_millis(100),
            shutdown_grace: Duration::from_millis(200),
        }
    }

    #[test]
    fn zero_connection_limit_is_rejected() {
        let mut invalid = limits();
        invalid.max_connections = 0;
        assert_eq!(
            invalid.validate().unwrap_err().kind(),
            io::ErrorKind::InvalidInput
        );
    }

    #[tokio::test]
    async fn echoes_arbitrary_stream_chunks_and_shuts_down() {
        let service = start(limits()).await.unwrap();
        let mut stream = TcpStream::connect(service.address).await.unwrap();
        stream.write_all(b"abc").await.unwrap();
        let mut output = [0_u8; 3];
        stream.read_exact(&mut output).await.unwrap();
        assert_eq!(&output, b"abc");
        drop(stream);
        service.shutdown().await.unwrap();
    }

    #[tokio::test]
    async fn idle_connection_is_closed_by_the_server() {
        let service = start(limits()).await.unwrap();
        let mut stream = TcpStream::connect(service.address).await.unwrap();
        let mut byte = [0_u8; 1];
        let count = time::timeout(Duration::from_secs(1), stream.read(&mut byte))
            .await
            .unwrap()
            .unwrap();
        assert_eq!(count, 0);
        service.shutdown().await.unwrap();
    }
}

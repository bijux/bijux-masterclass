use crate::{
    broker::start_broker,
    config::Config,
    error::ServiceError,
    http::serve_http,
    server::serve_tcp,
};
use std::net::SocketAddr;
use tokio::{net::TcpListener, task::{JoinHandle, JoinSet}};
use tokio_util::sync::CancellationToken;

pub struct RunningService {
    pub tcp_addr: SocketAddr,
    pub http_addr: SocketAddr,
    shutdown: CancellationToken,
    task: JoinHandle<Result<(), ServiceError>>,
}

impl RunningService {
    pub fn cancellation_token(&self) -> CancellationToken {
        self.shutdown.clone()
    }

    pub async fn shutdown(self) -> Result<(), ServiceError> {
        self.shutdown.cancel();
        self.task
            .await
            .map_err(|error| ServiceError::Task(format!("service supervisor join failed: {error}")))?
    }
}

pub async fn start_service(config: Config) -> Result<RunningService, ServiceError> {
    config.validate().map_err(ServiceError::Configuration)?;
    let tcp_listener = TcpListener::bind(config.tcp_addr).await?;
    let http_listener = TcpListener::bind(config.http_addr).await?;
    let tcp_addr = tcp_listener.local_addr()?;
    let http_addr = http_listener.local_addr()?;
    let shutdown = CancellationToken::new();
    let supervisor_token = shutdown.clone();
    let task = tokio::spawn(async move {
        let (broker, mut broker_task) = start_broker(config.clone(), supervisor_token.child_token());
        let mut services = JoinSet::new();
        let _tcp_abort = services.spawn(serve_tcp(
            tcp_listener,
            broker.clone(),
            config.clone(),
            supervisor_token.child_token(),
        ));
        let _http_abort = services.spawn(serve_http(
            http_listener,
            broker,
            config,
            supervisor_token.child_token(),
        ));

        let mut first_error = None;
        let mut broker_finished = false;
        tokio::select! {
            () = supervisor_token.cancelled() => {}
            broker_result = &mut broker_task => {
                broker_finished = true;
                match broker_result {
                    Ok(()) if !supervisor_token.is_cancelled() => {
                        first_error = Some(ServiceError::Task("broker task exited unexpectedly".to_owned()));
                    }
                    Ok(()) => {}
                    Err(error) => {
                        first_error = Some(ServiceError::Task(format!("broker task panicked or was cancelled: {error}")));
                    }
                }
                supervisor_token.cancel();
            }
            joined = services.join_next() => {
                match joined {
                    Some(Ok(Ok(()))) => {
                        first_error = Some(ServiceError::Task("service task exited unexpectedly".to_owned()));
                    }
                    Some(Ok(Err(error))) => first_error = Some(error),
                    Some(Err(error)) => {
                        first_error = Some(ServiceError::Task(format!("service task panicked or was cancelled: {error}")));
                    }
                    None => {
                        first_error = Some(ServiceError::Task("all service tasks exited unexpectedly".to_owned()));
                    }
                }
                supervisor_token.cancel();
            }
        }

        while let Some(joined) = services.join_next().await {
            match joined {
                Ok(Ok(())) => {}
                Ok(Err(error)) if first_error.is_none() => first_error = Some(error),
                Err(error) if first_error.is_none() => {
                    first_error = Some(ServiceError::Task(format!("service task join failed: {error}")));
                }
                _ => {}
            }
        }

        if !broker_finished {
            broker_task
                .await
                .map_err(|error| ServiceError::Task(format!("broker task join failed: {error}")))?;
        }
        match first_error {
            Some(error) => Err(error),
            None => Ok(()),
        }
    });

    Ok(RunningService {
        tcp_addr,
        http_addr,
        shutdown,
        task,
    })
}

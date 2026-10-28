use crate::domain::Record;
use crate::metrics::Metrics;
use crate::store::{Snapshot, Store, StoreError};
use std::fmt;
use std::sync::Arc;
use tokio::sync::{mpsc, oneshot, Semaphore};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BrokerError {
    Overloaded,
    Closed,
    Store(StoreError),
}

impl fmt::Display for BrokerError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Overloaded => formatter.write_str("broker is at capacity"),
            Self::Closed => formatter.write_str("broker is closed"),
            Self::Store(error) => write!(formatter, "{error}"),
        }
    }
}

impl std::error::Error for BrokerError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Store(error) => Some(error),
            Self::Overloaded | Self::Closed => None,
        }
    }
}

impl From<StoreError> for BrokerError {
    fn from(value: StoreError) -> Self {
        Self::Store(value)
    }
}

enum Command {
    Ingest {
        record: Record,
        reply: oneshot::Sender<Result<(), StoreError>>,
    },
    Snapshot {
        reply: oneshot::Sender<Snapshot>,
    },
    SeriesCount {
        reply: oneshot::Sender<usize>,
    },
    Shutdown,
}

#[derive(Clone)]
pub struct BrokerHandle {
    sender: mpsc::Sender<Command>,
    mailbox_capacity: usize,
    metrics: Arc<Metrics>,
    active_ingest: Arc<Semaphore>,
}

pub struct BrokerTask {
    receiver: mpsc::Receiver<Command>,
    store: Store,
    metrics: Arc<Metrics>,
}

pub fn channel(
    mailbox_capacity: usize,
    max_active_ingest: usize,
    store: Store,
    metrics: Arc<Metrics>,
) -> (BrokerHandle, BrokerTask) {
    let (sender, receiver) = mpsc::channel(mailbox_capacity);
    (
        BrokerHandle {
            sender,
            mailbox_capacity,
            metrics: Arc::clone(&metrics),
            active_ingest: Arc::new(Semaphore::new(max_active_ingest)),
        },
        BrokerTask { receiver, store, metrics },
    )
}

impl BrokerHandle {
    fn observe_depth(&self) {
        self.metrics
            .set_queue_depth(self.mailbox_capacity.saturating_sub(self.sender.capacity()));
    }

    pub async fn ingest(&self, record: Record) -> Result<(), BrokerError> {
        let _permit = Arc::clone(&self.active_ingest)
            .try_acquire_owned()
            .map_err(|_| {
                self.metrics.overloaded();
                BrokerError::Overloaded
            })?;
        let (reply, receive) = oneshot::channel();
        self.sender
            .try_send(Command::Ingest { record, reply })
            .map_err(|error| {
                if error.is_full() {
                    self.metrics.overloaded();
                    BrokerError::Overloaded
                } else {
                    BrokerError::Closed
                }
            })?;
        self.observe_depth();
        receive.await.map_err(|_| BrokerError::Closed)??;
        self.metrics.accepted();
        Ok(())
    }

    pub async fn snapshot(&self) -> Result<Snapshot, BrokerError> {
        let (reply, receive) = oneshot::channel();
        self.sender
            .try_send(Command::Snapshot { reply })
            .map_err(|error| {
                if error.is_full() {
                    self.metrics.overloaded();
                    BrokerError::Overloaded
                } else {
                    BrokerError::Closed
                }
            })?;
        self.observe_depth();
        receive.await.map_err(|_| BrokerError::Closed)
    }

    pub async fn series_count(&self) -> Result<usize, BrokerError> {
        let (reply, receive) = oneshot::channel();
        self.sender
            .try_send(Command::SeriesCount { reply })
            .map_err(|error| {
                if error.is_full() {
                    self.metrics.overloaded();
                    BrokerError::Overloaded
                } else {
                    BrokerError::Closed
                }
            })?;
        self.observe_depth();
        receive.await.map_err(|_| BrokerError::Closed)
    }

    pub async fn shutdown(&self) -> Result<(), BrokerError> {
        self.sender
            .send(Command::Shutdown)
            .await
            .map_err(|_| BrokerError::Closed)
    }
}

impl BrokerTask {
    pub async fn run(mut self) -> Store {
        while let Some(command) = self.receiver.recv().await {
            self.metrics.set_queue_depth(self.receiver.len());
            match command {
                Command::Ingest { record, reply } => {
                    let _ = reply.send(self.store.apply(record));
                }
                Command::Snapshot { reply } => {
                    let _ = reply.send(self.store.snapshot());
                }
                Command::SeriesCount { reply } => {
                    let _ = reply.send(self.store.len());
                }
                Command::Shutdown => break,
            }
        }
        self.store
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::{MetricName, Tenant};

    fn record() -> Record {
        Record::new(
            Tenant::parse("acme", 32).expect("tenant"),
            MetricName::parse("requests", 32).expect("metric"),
            1,
            1.0,
        )
        .expect("record")
    }

    #[tokio::test]
    async fn broker_owns_semantic_commit() {
        let metrics = Arc::new(Metrics::default());
        let (handle, task) = channel(8, 2, Store::new(8, 1024), metrics);
        let join = tokio::spawn(task.run());
        handle.ingest(record()).await.expect("ingest");
        assert_eq!(handle.series_count().await, Ok(1));
        handle.shutdown().await.expect("shutdown");
        let store = join.await.expect("broker task");
        assert_eq!(store.len(), 1);
    }
}

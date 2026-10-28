//! JobWire: a bounded async job service used by Course 8.

pub mod app;
pub mod broker;
pub mod client;
pub mod codec;
pub mod config;
pub mod domain;
pub mod error;
pub mod http;
pub mod protocol;
pub mod server;

pub use app::{RunningService, start_service};
pub use client::JobWireClient;
pub use config::Config;
pub use domain::{HealthState, Operation, StatusSnapshot};
pub use error::{ClientError, ServiceError};

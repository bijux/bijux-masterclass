#![allow(dead_code)]
#[derive(Clone)] struct ServiceConfig { max_connections: usize, queue_capacity: usize }
fn validate(config: ServiceConfig) -> Result<ServiceConfig, &'static str> { if config.max_connections == 0 || config.queue_capacity == 0 { Err("limits must be nonzero") } else { Ok(config) } }
fn main() { assert!(validate(ServiceConfig { max_connections: 8, queue_capacity: 16 }).is_ok()); }

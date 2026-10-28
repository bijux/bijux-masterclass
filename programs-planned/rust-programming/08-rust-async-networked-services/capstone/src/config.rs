use std::{net::SocketAddr, time::Duration};

#[derive(Debug, Clone)]
pub struct Config {
    pub tcp_addr: SocketAddr,
    pub http_addr: SocketAddr,
    pub max_connections: usize,
    pub max_http_connections: usize,
    pub max_frame_bytes: usize,
    pub broker_capacity: usize,
    pub max_queued_jobs: usize,
    pub max_active_jobs: usize,
    pub max_result_bytes: usize,
    pub max_idempotency_records: usize,
    pub max_waiters_per_key: usize,
    pub handshake_timeout: Duration,
    pub request_timeout: Duration,
    pub write_timeout: Duration,
    pub shutdown_grace: Duration,
    pub max_sleep: Duration,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            tcp_addr: "127.0.0.1:7800".parse().expect("static TCP address"),
            http_addr: "127.0.0.1:7801".parse().expect("static HTTP address"),
            max_connections: 128,
            max_http_connections: 32,
            max_frame_bytes: 64 * 1024,
            broker_capacity: 128,
            max_queued_jobs: 64,
            max_active_jobs: 8,
            max_result_bytes: 60 * 1024,
            max_idempotency_records: 10_000,
            max_waiters_per_key: 16,
            handshake_timeout: Duration::from_secs(5),
            request_timeout: Duration::from_secs(10),
            write_timeout: Duration::from_secs(5),
            shutdown_grace: Duration::from_secs(5),
            max_sleep: Duration::from_secs(2),
        }
    }
}

impl Config {
    pub fn validate(&self) -> Result<(), &'static str> {
        let values = [
            ("max_connections", self.max_connections),
            ("max_http_connections", self.max_http_connections),
            ("max_frame_bytes", self.max_frame_bytes),
            ("broker_capacity", self.broker_capacity),
            ("max_queued_jobs", self.max_queued_jobs),
            ("max_active_jobs", self.max_active_jobs),
            ("max_result_bytes", self.max_result_bytes),
            ("max_idempotency_records", self.max_idempotency_records),
            ("max_waiters_per_key", self.max_waiters_per_key),
        ];
        for (name, value) in values {
            if value == 0 {
                return Err(name);
            }
        }
        if self.max_frame_bytes > u32::MAX as usize {
            return Err("max_frame_bytes");
        }

        // A successful response adds protocol fields around the result. Keep a
        // conservative envelope so an admitted job cannot produce a value that
        // the configured frame codec is then unable to transmit.
        const RESPONSE_ENVELOPE_BYTES: usize = 128;
        if self.max_frame_bytes <= RESPONSE_ENVELOPE_BYTES
            || self.max_result_bytes
                > self.max_frame_bytes.saturating_sub(RESPONSE_ENVELOPE_BYTES)
        {
            return Err("max_result_bytes");
        }

        let durations = [
            ("handshake_timeout", self.handshake_timeout),
            ("request_timeout", self.request_timeout),
            ("write_timeout", self.write_timeout),
            ("shutdown_grace", self.shutdown_grace),
        ];
        for (name, duration) in durations {
            if duration.is_zero() {
                return Err(name);
            }
        }
        Ok(())
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_configuration_preserves_wire_and_resource_bounds() {
        assert!(Config::default().validate().is_ok());
    }

    #[test]
    fn result_limit_must_leave_room_for_response_fields() {
        let config = Config {
            max_frame_bytes: 1024,
            max_result_bytes: 1024,
            ..Config::default()
        };
        assert_eq!(config.validate(), Err("max_result_bytes"));
    }

    #[test]
    fn operational_deadlines_must_be_nonzero() {
        let config = Config {
            request_timeout: Duration::ZERO,
            ..Config::default()
        };
        assert_eq!(config.validate(), Err("request_timeout"));
    }
}

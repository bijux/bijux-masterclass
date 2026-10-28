use std::fmt;

#[derive(Debug, Clone)]
pub struct Config {
    pub max_line_bytes: usize,
    pub max_identifier_bytes: usize,
    pub max_connections: usize,
    pub mailbox_capacity: usize,
    pub max_active_ingest: usize,
    pub max_series: usize,
    pub max_identifier_storage_bytes: usize,
    pub max_snapshot_bytes: usize,
    pub max_offline_records: usize,
    pub max_offline_bytes: usize,
    pub connection_idle_timeout_ms: u64,
    pub write_timeout_ms: u64,
    pub load_request_timeout_ms: u64,
    pub shutdown_grace_ms: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ConfigError {
    Zero(&'static str),
    Inconsistent(&'static str),
}

impl fmt::Display for ConfigError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Zero(name) => write!(formatter, "{name} must be nonzero"),
            Self::Inconsistent(message) => formatter.write_str(message),
        }
    }
}

impl std::error::Error for ConfigError {}

impl Default for Config {
    fn default() -> Self {
        Self {
            max_line_bytes: 4096,
            max_identifier_bytes: 128,
            max_connections: 128,
            mailbox_capacity: 1024,
            max_active_ingest: 64,
            max_series: 100_000,
            max_identifier_storage_bytes: 16 * 1024 * 1024,
            max_snapshot_bytes: 8 * 1024 * 1024,
            max_offline_records: 1_000_000,
            max_offline_bytes: 256 * 1024 * 1024,
            connection_idle_timeout_ms: 30_000,
            write_timeout_ms: 5_000,
            load_request_timeout_ms: 5_000,
            shutdown_grace_ms: 5_000,
        }
    }
}

impl Config {
    pub fn validate(&self) -> Result<(), ConfigError> {
        for (name, value) in [
            ("max_line_bytes", self.max_line_bytes),
            ("max_identifier_bytes", self.max_identifier_bytes),
            ("max_connections", self.max_connections),
            ("mailbox_capacity", self.mailbox_capacity),
            ("max_active_ingest", self.max_active_ingest),
            ("max_series", self.max_series),
            (
                "max_identifier_storage_bytes",
                self.max_identifier_storage_bytes,
            ),
            ("max_snapshot_bytes", self.max_snapshot_bytes),
            ("max_offline_records", self.max_offline_records),
            ("max_offline_bytes", self.max_offline_bytes),
        ] {
            if value == 0 {
                return Err(ConfigError::Zero(name));
            }
        }

        for (name, value) in [
            (
                "connection_idle_timeout_ms",
                self.connection_idle_timeout_ms,
            ),
            ("write_timeout_ms", self.write_timeout_ms),
            ("load_request_timeout_ms", self.load_request_timeout_ms),
            ("shutdown_grace_ms", self.shutdown_grace_ms),
        ] {
            if value == 0 {
                return Err(ConfigError::Zero(name));
            }
        }

        if self.max_identifier_bytes > self.max_line_bytes {
            return Err(ConfigError::Inconsistent(
                "identifier limit cannot exceed line limit",
            ));
        }
        if self.max_active_ingest > self.mailbox_capacity {
            return Err(ConfigError::Inconsistent(
                "active ingest limit cannot exceed mailbox capacity",
            ));
        }
        if self.max_line_bytes > self.max_offline_bytes {
            return Err(ConfigError::Inconsistent(
                "line limit cannot exceed offline byte limit",
            ));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_configuration_is_valid() {
        assert_eq!(Config::default().validate(), Ok(()));
    }

    #[test]
    fn zero_capacity_is_rejected() {
        let mut config = Config::default();
        config.mailbox_capacity = 0;
        assert_eq!(
            config.validate(),
            Err(ConfigError::Zero("mailbox_capacity"))
        );
    }

    #[test]
    fn active_ingest_cannot_exceed_mailbox_capacity() {
        let mut config = Config::default();
        config.mailbox_capacity = 2;
        config.max_active_ingest = 3;
        assert_eq!(
            config.validate(),
            Err(ConfigError::Inconsistent(
                "active ingest limit cannot exceed mailbox capacity"
            ))
        );
    }
}

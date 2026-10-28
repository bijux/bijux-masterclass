use std::{io, time::Duration};

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
        if self.idle.is_zero() || self.write_stall.is_zero() || self.shutdown_grace.is_zero() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "all deadlines must be nonzero",
            ));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn limits_are_explicit() {
        assert!(EchoLimits {
            max_connections: 4,
            idle: Duration::from_secs(1),
            write_stall: Duration::from_secs(1),
            shutdown_grace: Duration::from_secs(1),
        }
        .validate()
        .is_ok());
    }
}

#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Level {
    Debug,
    Info,
    Warn,
    Error,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LogEntry {
    pub level: Level,
    pub message: String,
}

impl LogEntry {
    pub fn new(level: Level, message: impl Into<String>) -> Self {
        Self {
            level,
            message: message.into(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Level;

    #[test]
    fn severity_order_is_part_of_the_starter_contract() {
        assert!(Level::Error > Level::Info);
    }
}

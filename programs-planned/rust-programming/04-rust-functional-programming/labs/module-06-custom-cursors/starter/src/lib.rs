#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    pub id: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct EventLog {
    events: Vec<Event>,
}

impl EventLog {
    pub fn new(events: Vec<Event>) -> Self {
        Self { events }
    }

    pub fn len(&self) -> usize {
        self.events.len()
    }

    pub fn is_empty(&self) -> bool {
        self.events.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::{Event, EventLog};

    #[test]
    fn starter_keeps_representation_private() {
        let log = EventLog::new(vec![Event { id: 1 }]);
        assert_eq!(log.len(), 1);
    }
}

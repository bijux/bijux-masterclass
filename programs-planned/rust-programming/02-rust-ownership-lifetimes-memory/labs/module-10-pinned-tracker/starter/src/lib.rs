//! Movable tracker baseline before address-sensitive initialization.

/// Ordinary movable value whose semantics do not depend on its address.
#[derive(Debug)]
pub struct Tracker {
    label: String,
    observations: u64,
}

impl Tracker {
    /// Creates a movable tracker.
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            observations: 0,
        }
    }

    /// Records an observation through ordinary mutable access.
    pub fn observe(&mut self) {
        self.observations += 1;
    }

    /// Borrows the label.
    pub fn label(&self) -> &str {
        &self.label
    }

    /// Returns the observation count.
    pub const fn observations(&self) -> u64 {
        self.observations
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_can_move_without_invalidating_semantics() {
        let mut first = Tracker::new("movable");
        first.observe();
        let second = first;
        assert_eq!(second.label(), "movable");
        assert_eq!(second.observations(), 1);
    }
}

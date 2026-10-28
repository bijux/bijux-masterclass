#![forbid(unsafe_code)]

use std::sync::Mutex;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Snapshot {
    pub capacity: u64,
    pub available: u64,
    pub reserved: u64,
}

impl Snapshot {
    #[must_use]
    pub fn invariant_holds(self) -> bool {
        self.available <= self.capacity
            && self.reserved <= self.capacity
            && self.available.checked_add(self.reserved) == Some(self.capacity)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InventoryError {
    Insufficient { requested: u64, available: u64 },
    InvalidRelease { requested: u64, reserved: u64 },
    Interrupted,
}

#[derive(Debug)]
struct State { available: u64, reserved: u64 }

#[derive(Debug)]
pub struct Inventory {
    capacity: u64,
    state: Mutex<State>,
}

impl Inventory {
    #[must_use]
    pub fn new(capacity: u64) -> Self {
        Self { capacity, state: Mutex::new(State { available: capacity, reserved: 0 }) }
    }

    pub fn reserve(&self, amount: u64) -> Result<Snapshot, InventoryError> {
        let mut state = self.state.lock().map_err(|_| InventoryError::Interrupted)?;
        if amount > state.available {
            return Err(InventoryError::Insufficient { requested: amount, available: state.available });
        }
        state.available -= amount;
        state.reserved += amount;
        Ok(self.snapshot_from(&state))
    }

    pub fn release(&self, amount: u64) -> Result<Snapshot, InventoryError> {
        let mut state = self.state.lock().map_err(|_| InventoryError::Interrupted)?;
        if amount > state.reserved {
            return Err(InventoryError::InvalidRelease { requested: amount, reserved: state.reserved });
        }
        state.reserved -= amount;
        state.available += amount;
        Ok(self.snapshot_from(&state))
    }

    pub fn snapshot(&self) -> Result<Snapshot, InventoryError> {
        let state = self.state.lock().map_err(|_| InventoryError::Interrupted)?;
        Ok(self.snapshot_from(&state))
    }

    pub fn reserve_then<F>(&self, amount: u64, observer: F) -> Result<Snapshot, InventoryError>
    where F: FnOnce(Snapshot) {
        let snapshot = self.reserve(amount)?;
        observer(snapshot);
        Ok(snapshot)
    }

    fn snapshot_from(&self, state: &State) -> Snapshot {
        let snapshot = Snapshot { capacity: self.capacity, available: state.available, reserved: state.reserved };
        debug_assert!(snapshot.invariant_holds());
        snapshot
    }
}

#[cfg(test)]
mod tests {
    use super::{Inventory, InventoryError};
    use std::sync::{Arc, Barrier};
    use std::thread;

    #[test]
    fn failed_transition_leaves_state_unchanged() {
        let inventory = Inventory::new(2);
        assert!(matches!(inventory.reserve(3), Err(InventoryError::Insufficient { .. })));
        assert_eq!(inventory.snapshot().expect("not poisoned").available, 2);
    }

    #[test]
    fn zero_transitions_are_successful_no_ops() {
        let inventory = Inventory::new(2);
        let before = inventory.snapshot().expect("not poisoned");
        assert_eq!(inventory.reserve(0), Ok(before));
        assert_eq!(inventory.release(0), Ok(before));
        assert_eq!(inventory.snapshot(), Ok(before));
    }

    #[test]
    fn exactly_one_contender_gets_the_last_unit() {
        let inventory = Arc::new(Inventory::new(1));
        let barrier = Arc::new(Barrier::new(3));
        let handles: Vec<_> = (0..2).map(|_| {
            let inventory = Arc::clone(&inventory);
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || { barrier.wait(); inventory.reserve(1) })
        }).collect();
        barrier.wait();
        let successes = handles.into_iter()
            .filter(|handle| handle.join().expect("worker joins").is_ok())
            .count();
        assert_eq!(successes, 1);
        assert!(inventory.snapshot().expect("not poisoned").invariant_holds());
    }

    #[test]
    fn observer_runs_after_unlock_and_can_reenter() {
        let inventory = Inventory::new(4);
        inventory.reserve_then(1, |_| {
            assert!(inventory.snapshot().expect("guard was released").invariant_holds());
        }).expect("reservation succeeds");
    }
}

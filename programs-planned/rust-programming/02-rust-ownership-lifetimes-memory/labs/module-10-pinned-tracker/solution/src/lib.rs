//! A safe-facing `!Unpin` tracker using its address only as an opaque token.
use std::cell::Cell;
use std::fmt;
use std::marker::PhantomPinned;
use std::pin::Pin;
use std::ptr::NonNull;
#[derive(Debug)]
pub struct PinnedTracker {
    label: String,
    initialized_at: Cell<Option<NonNull<PinnedTracker>>>,
    observations: Cell<u64>,
    _pin: PhantomPinned,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TrackerError {
    AlreadyInitialized, NotInitialized, AddressChanged, CounterOverflow
}
impl fmt::Display for TrackerError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let text = match self {
            Self::AlreadyInitialized => "already initialized",
            Self::NotInitialized => "not initialized",
            Self::AddressChanged => "address changed",
            Self::CounterOverflow => "counter overflow",
        };
        write!(f, "{text}")
    }
}
impl std::error::Error for TrackerError {
}
impl PinnedTracker {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(), initialized_at: Cell::new(None), observations: Cell::new(0), _pin: PhantomPinned
        }
    }
    pub fn initialize(self: Pin<&Self>) -> Result<(), TrackerError> {
        if self.initialized_at.get().is_some() {
            return Err(TrackerError::AlreadyInitialized);
        }
        self.initialized_at.set(Some(NonNull::from(self.get_ref())));
        Ok(())
    }
    pub fn observe(self: Pin<&Self>) -> Result<u64, TrackerError> {
        let expected = self.initialized_at.get().ok_or(TrackerError::NotInitialized)?;
        if expected != NonNull::from(self.get_ref()) {
            return Err(TrackerError::AddressChanged);
        }
        let next = self.observations.get().checked_add(1).ok_or(TrackerError::CounterOverflow)?;
        self.observations.set(next);
        Ok(next)
    }
    pub fn label(self: Pin<&Self>) -> &str {
        &self.get_ref().label
    }
    pub fn observations(self: Pin<&Self>) -> u64 {
        self.get_ref().observations.get()
    }
    pub fn address(self: Pin<&Self>) -> NonNull<PinnedTracker> {
        NonNull::from(self.get_ref())
    }
}
/// A `!Unpin` tracker does not expose unrestricted mutable access after pinning.
///
/// ```compile_fail
/// use rust_olm_lab_10_pinned_tracker::PinnedTracker;
/// let mut tracker = Box::pin(PinnedTracker::new("x"));
/// let _ordinary: &mut PinnedTracker = tracker.as_mut().get_mut();
/// ```
pub fn pinned_contract() {
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::pin::pin;
    #[test]
    fn heap_pinning_preserves_observed_address() {
        let tracker = Box::pin(PinnedTracker::new("heap"));
        assert_eq!(tracker.as_ref().initialize(), Ok(()));
        let address = tracker.as_ref().address();
        assert_eq!(tracker.as_ref().observe(), Ok(1));
        assert_eq!(tracker.as_ref().address(), address);
        assert_eq!(tracker.as_ref().label(), "heap");
    }
    #[test]
    fn stack_pinning_is_scoped_and_safe() {
        let tracker = pin!(PinnedTracker::new("stack"));
        assert_eq!(tracker.as_ref().initialize(), Ok(()));
        assert_eq!(tracker.as_ref().observe(), Ok(1));
        assert_eq!(tracker.as_ref().observations(), 1);
    }
    #[test]
    fn initialization_protocol_is_enforced() {
        let tracker = Box::pin(PinnedTracker::new("x"));
        assert_eq!(tracker.as_ref().observe(), Err(TrackerError::NotInitialized));
        assert_eq!(tracker.as_ref().initialize(), Ok(()));
        assert_eq!(tracker.as_ref().initialize(), Err(TrackerError::AlreadyInitialized));
    }
}

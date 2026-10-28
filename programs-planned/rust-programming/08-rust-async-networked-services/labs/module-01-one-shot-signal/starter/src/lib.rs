use std::task::Waker;

#[derive(Debug)]
pub struct SignalState<T> {
    value: Option<T>,
    waker: Option<Waker>,
    receiver_alive: bool,
    sender_alive: bool,
}


impl<T> Default for SignalState<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> SignalState<T> {
    pub fn new() -> Self {
        Self {
            value: None,
            waker: None,
            receiver_alive: true,
            sender_alive: true,
        }
    }

    pub fn receiver_alive(&self) -> bool {
        self.receiver_alive
    }

    pub fn sender_alive(&self) -> bool {
        self.sender_alive
    }

    pub fn is_complete(&self) -> bool {
        self.value.is_some()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fresh_model_has_two_live_endpoints() {
        let state = SignalState::<u64>::new();
        assert!(state.receiver_alive());
        assert!(state.sender_alive());
        assert!(!state.is_complete());
    }
}

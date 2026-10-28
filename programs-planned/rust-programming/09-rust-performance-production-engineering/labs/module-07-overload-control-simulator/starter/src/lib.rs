#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    Accept,
    Reject,
}

pub fn decide(queue_len: usize, capacity: usize) -> Decision {
    if queue_len < capacity { Decision::Accept } else { Decision::Reject }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn full_queue_is_rejected() {
        assert_eq!(decide(4, 4), Decision::Reject);
    }
}

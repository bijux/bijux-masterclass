#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Publication {
    Draft,
    Review,
    Published,
}

impl Publication {
    pub const fn can_transition(self, next: Self) -> bool {
        matches!(
            (self, next),
            (Self::Draft, Self::Review)
                | (Self::Review, Self::Draft)
                | (Self::Review, Self::Published)
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_edge_is_explicit() {
        assert!(Publication::Draft.can_transition(Publication::Review));
    }
}

//! Minimal safe layout observation without claim classification.

/// Current target's measured size and alignment for one type.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Observation {
    /// Human-readable type label supplied by the caller.
    pub name: &'static str,
    /// Inline size observed on the current target.
    pub size: usize,
    /// Alignment observed on the current target.
    pub alignment: usize,
}

/// Measures one type on the current compilation target.
pub fn observe<T>(name: &'static str) -> Observation {
    Observation {
        name,
        size: std::mem::size_of::<T>(),
        alignment: std::mem::align_of::<T>(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_records_an_observation_not_an_abi_promise() {
        let value = observe::<u32>("u32");
        assert_eq!(value.name, "u32");
        assert_eq!(value.size, std::mem::size_of::<u32>());
        assert_eq!(value.alignment, std::mem::align_of::<u32>());
    }
}

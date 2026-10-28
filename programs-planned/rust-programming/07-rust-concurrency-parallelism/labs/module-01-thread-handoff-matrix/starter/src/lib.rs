#![forbid(unsafe_code)]

pub const MAX_INPUTS: usize = 32;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Behavior {
    Normal,
    Yield(usize),
    Panic,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DigestInput {
    pub bytes: Vec<u8>,
    pub behavior: Behavior,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ThreadOutcome {
    Digest(u64),
    Panicked,
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf_29ce_4842_2325, |hash, byte| {
        (hash ^ u64::from(*byte)).wrapping_mul(0x100_0000_01b3)
    })
}

#[must_use]
pub fn sequential(inputs: &[DigestInput]) -> Vec<u64> {
    inputs.iter().map(|input| fnv1a(&input.bytes)).collect()
}

#[cfg(test)]
mod tests {
    use super::{Behavior, DigestInput, fnv1a, sequential};

    #[test]
    fn baseline_digest_is_stable() {
        assert_eq!(fnv1a(b"abc"), fnv1a(b"abc"));
    }

    #[test]
    fn sequential_preserves_source_order() {
        let inputs = vec![
            DigestInput { bytes: b"b".to_vec(), behavior: Behavior::Normal },
            DigestInput { bytes: b"a".to_vec(), behavior: Behavior::Normal },
        ];
        assert_eq!(sequential(&inputs), vec![fnv1a(b"b"), fnv1a(b"a")]);
    }
}

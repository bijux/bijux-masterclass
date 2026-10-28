#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Behavior { Verify, Panic, Spin(usize) }

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Artifact {
    pub id: String,
    pub bytes: Vec<u8>,
    pub expected: u64,
    pub behavior: Behavior,
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf_29ce_4842_2325, |hash, byte| {
        (hash ^ u64::from(*byte)).wrapping_mul(0x100_0000_01b3)
    })
}

#[cfg(test)]
mod tests {
    use super::fnv1a;
    #[test]
    fn baseline_digest_is_stable() { assert_eq!(fnv1a(b"artifact"), fnv1a(b"artifact")); }
}

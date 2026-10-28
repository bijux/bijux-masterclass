
#![forbid(unsafe_code)]

pub const MAGIC: [u8; 4] = *b"PKT1";

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u32 {
    bytes.iter().fold(0x811c_9dc5, |hash, byte| {
        (hash ^ u32::from(*byte)).wrapping_mul(0x0100_0193)
    })
}

#[cfg(test)]
mod tests {
    use super::fnv1a;

    #[test]
    fn checksum_baseline_is_order_sensitive() {
        assert_ne!(fnv1a(b"a"), fnv1a(b"b"));
        assert_ne!(fnv1a(b"ab"), fnv1a(b"ba"));
    }
}

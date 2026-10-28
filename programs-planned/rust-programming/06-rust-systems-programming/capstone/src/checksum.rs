
//! A small deterministic checksum used to detect accidental corruption.
//!
//! FNV-1a is not cryptographic. FrameVault never presents this value as an
//! authenticity proof, a signature, or protection against a malicious writer.

/// Compute a 32-bit FNV-1a checksum.
#[must_use]
pub fn checksum32(bytes: &[u8]) -> u32 {
    let mut state = 0x811c_9dc5_u32;
    for byte in bytes {
        state ^= u32::from(*byte);
        state = state.wrapping_mul(0x0100_0193);
    }
    state
}

#[cfg(test)]
mod tests {
    use super::checksum32;

    #[test]
    fn checksum_is_deterministic_and_order_sensitive() {
        assert_eq!(checksum32(b"frame"), checksum32(b"frame"));
        assert_ne!(checksum32(b"frame"), checksum32(b"farem"));
    }
}

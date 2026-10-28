
#![forbid(unsafe_code)]

pub const MAGIC: [u8; 4] = *b"BFC1";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Frame {
    pub kind: u8,
    pub payload: Vec<u8>,
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u32 {
    bytes.iter().fold(0x811c_9dc5, |hash, byte| {
        (hash ^ u32::from(*byte)).wrapping_mul(0x0100_0193)
    })
}

#[must_use]
pub fn header(frame_count: u16) -> [u8; 6] {
    let mut result = [0_u8; 6];
    result[..4].copy_from_slice(&MAGIC);
    result[4..].copy_from_slice(&frame_count.to_le_bytes());
    result
}

#[cfg(test)]
mod tests {
    use super::{fnv1a, header};

    #[test]
    fn baseline_header_is_canonical() {
        assert_eq!(header(2), [b'B', b'F', b'C', b'1', 2, 0]);
    }

    #[test]
    fn checksum_is_deterministic() {
        assert_eq!(fnv1a(b"abc"), fnv1a(b"abc"));
    }
}

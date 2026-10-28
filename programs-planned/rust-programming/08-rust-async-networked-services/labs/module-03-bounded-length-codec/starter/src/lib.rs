use std::io;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FrameConfig {
    pub max_payload: usize,
}

impl FrameConfig {
    pub fn validate(self) -> io::Result<Self> {
        if self.max_payload == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "maximum payload must be nonzero",
            ));
        }
        if self.max_payload > u32::MAX as usize {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "maximum payload must fit the four-byte prefix",
            ));
        }
        Ok(self)
    }

    pub fn encoded_len(self, payload_len: usize) -> io::Result<usize> {
        let config = self.validate()?;
        if payload_len > config.max_payload {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "payload exceeds the configured maximum",
            ));
        }
        4_usize.checked_add(payload_len).ok_or_else(|| {
            io::Error::new(io::ErrorKind::InvalidInput, "encoded length overflow")
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validates_representation_and_total_length_bounds() {
        let config = FrameConfig { max_payload: 1024 };
        assert_eq!(config.encoded_len(12).unwrap(), 16);
        assert!(config.encoded_len(1025).is_err());
        assert!(FrameConfig { max_payload: 0 }.validate().is_err());
    }
}

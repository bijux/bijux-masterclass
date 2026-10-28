
#![forbid(unsafe_code)]

use std::fmt;

pub const MAGIC: [u8; 4] = *b"BFC1";
pub const MAX_FRAMES: usize = 64;
pub const MAX_TOTAL_PAYLOAD: usize = 1024 * 1024;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Frame {
    pub kind: u8,
    pub payload: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CodecError {
    BadMagic,
    UnexpectedEnd {
        offset: usize,
        needed: usize,
        remaining: usize,
    },
    TooManyFrames {
        declared: usize,
    },
    UnsupportedKind {
        offset: usize,
        value: u8,
    },
    LengthOverflow {
        offset: usize,
    },
    TotalTooLarge {
        declared: usize,
        limit: usize,
    },
    ChecksumMismatch {
        frame: usize,
        offset: usize,
        expected: u32,
        actual: u32,
    },
    TrailingBytes {
        offset: usize,
        count: usize,
    },
    TooManyFramesToEncode {
        count: usize,
    },
    PayloadTooLargeToEncode {
        length: usize,
    },
}

impl fmt::Display for CodecError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for CodecError {}

#[derive(Clone, Copy)]
struct Cursor<'a> {
    remaining: &'a [u8],
    offset: usize,
}

impl<'a> Cursor<'a> {
    const fn new(bytes: &'a [u8]) -> Self {
        Self {
            remaining: bytes,
            offset: 0,
        }
    }

    fn take(&mut self, count: usize) -> Result<&'a [u8], CodecError> {
        let bytes = self
            .remaining
            .get(..count)
            .ok_or(CodecError::UnexpectedEnd {
                offset: self.offset,
                needed: count,
                remaining: self.remaining.len(),
            })?;
        self.remaining = &self.remaining[count..];
        self.offset += count;
        Ok(bytes)
    }

    fn read_u8(&mut self) -> Result<u8, CodecError> {
        Ok(self.take(1)?[0])
    }

    fn read_u16(&mut self) -> Result<u16, CodecError> {
        let bytes = self.take(2)?;
        Ok(u16::from_le_bytes([bytes[0], bytes[1]]))
    }

    fn read_u32(&mut self) -> Result<u32, CodecError> {
        let bytes = self.take(4)?;
        Ok(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u32 {
    bytes.iter().fold(0x811c_9dc5, |hash, byte| {
        (hash ^ u32::from(*byte)).wrapping_mul(0x0100_0193)
    })
}

pub fn decode(bytes: &[u8]) -> Result<Vec<Frame>, CodecError> {
    let mut cursor = Cursor::new(bytes);
    if cursor.take(MAGIC.len())? != MAGIC {
        return Err(CodecError::BadMagic);
    }

    let frame_count = usize::from(cursor.read_u16()?);
    if frame_count > MAX_FRAMES {
        return Err(CodecError::TooManyFrames {
            declared: frame_count,
        });
    }

    let mut total_payload = 0_usize;
    let mut frames = Vec::new();
    frames
        .try_reserve_exact(frame_count)
        .map_err(|_| CodecError::TotalTooLarge {
            declared: frame_count,
            limit: MAX_FRAMES,
        })?;

    for frame_index in 0..frame_count {
        let kind_offset = cursor.offset;
        let kind = cursor.read_u8()?;
        if !matches!(kind, 1 | 2) {
            return Err(CodecError::UnsupportedKind {
                offset: kind_offset,
                value: kind,
            });
        }

        let length_offset = cursor.offset;
        let length = usize::try_from(cursor.read_u32()?)
            .map_err(|_| CodecError::LengthOverflow {
                offset: length_offset,
            })?;
        total_payload = total_payload
            .checked_add(length)
            .ok_or(CodecError::LengthOverflow {
                offset: length_offset,
            })?;
        if total_payload > MAX_TOTAL_PAYLOAD {
            return Err(CodecError::TotalTooLarge {
                declared: total_payload,
                limit: MAX_TOTAL_PAYLOAD,
            });
        }

        let expected = cursor.read_u32()?;
        let payload_offset = cursor.offset;
        let payload = cursor.take(length)?;
        let actual = fnv1a(payload);
        if actual != expected {
            return Err(CodecError::ChecksumMismatch {
                frame: frame_index,
                offset: payload_offset,
                expected,
                actual,
            });
        }
        frames.push(Frame {
            kind,
            payload: payload.to_vec(),
        });
    }

    if !cursor.remaining.is_empty() {
        return Err(CodecError::TrailingBytes {
            offset: cursor.offset,
            count: cursor.remaining.len(),
        });
    }
    Ok(frames)
}

pub fn encode(frames: &[Frame]) -> Result<Vec<u8>, CodecError> {
    if frames.len() > MAX_FRAMES {
        return Err(CodecError::TooManyFramesToEncode {
            count: frames.len(),
        });
    }
    let frame_count = u16::try_from(frames.len()).map_err(|_| {
        CodecError::TooManyFramesToEncode {
            count: frames.len(),
        }
    })?;
    let total_payload = frames.iter().try_fold(0_usize, |sum, frame| {
        sum.checked_add(frame.payload.len())
    });
    let total_payload = total_payload.ok_or(CodecError::LengthOverflow { offset: 0 })?;
    if total_payload > MAX_TOTAL_PAYLOAD {
        return Err(CodecError::TotalTooLarge {
            declared: total_payload,
            limit: MAX_TOTAL_PAYLOAD,
        });
    }

    let mut output = Vec::new();
    output.extend_from_slice(&MAGIC);
    output.extend_from_slice(&frame_count.to_le_bytes());
    for frame in frames {
        if !matches!(frame.kind, 1 | 2) {
            return Err(CodecError::UnsupportedKind {
                offset: output.len(),
                value: frame.kind,
            });
        }
        let length = u32::try_from(frame.payload.len()).map_err(|_| {
            CodecError::PayloadTooLargeToEncode {
                length: frame.payload.len(),
            }
        })?;
        output.push(frame.kind);
        output.extend_from_slice(&length.to_le_bytes());
        output.extend_from_slice(&fnv1a(&frame.payload).to_le_bytes());
        output.extend_from_slice(&frame.payload);
    }
    Ok(output)
}

#[cfg(test)]
mod tests {
    use super::{CodecError, Frame, decode, encode};

    #[test]
    fn round_trip_and_every_truncation_fails() {
        let frames = vec![
            Frame {
                kind: 1,
                payload: b"alpha".to_vec(),
            },
            Frame {
                kind: 2,
                payload: vec![0, 255],
            },
        ];
        let encoded = encode(&frames).expect("fixture encodes");
        assert_eq!(decode(&encoded).expect("fixture decodes"), frames);
        for cut in 0..encoded.len() {
            assert!(decode(&encoded[..cut]).is_err(), "cut={cut}");
        }
    }

    #[test]
    fn rejects_trailing_data() {
        let mut bytes = encode(&[]).expect("empty archive encodes");
        bytes.push(0);
        assert!(matches!(
            decode(&bytes),
            Err(CodecError::TrailingBytes { .. })
        ));
    }
}

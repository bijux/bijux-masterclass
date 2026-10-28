use bytes::{Buf, BufMut, Bytes, BytesMut};
use std::io;
use tokio_util::codec::{Decoder, Encoder};

#[derive(Debug, Clone)]
pub struct LengthCodec {
    max_payload: usize,
}

impl LengthCodec {
    pub fn new(max_payload: usize) -> io::Result<Self> {
        if max_payload == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "maximum payload must be nonzero",
            ));
        }
        if max_payload > u32::MAX as usize {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "maximum payload must fit the four-byte prefix",
            ));
        }
        Ok(Self { max_payload })
    }

    pub const fn max_payload(&self) -> usize {
        self.max_payload
    }
}

impl Decoder for LengthCodec {
    type Item = Bytes;
    type Error = io::Error;

    fn decode(&mut self, src: &mut BytesMut) -> io::Result<Option<Self::Item>> {
        const PREFIX: usize = 4;
        if src.len() < PREFIX {
            return Ok(None);
        }
        let prefix: [u8; PREFIX] = src[..PREFIX]
            .try_into()
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "invalid frame prefix"))?;
        let length = usize::try_from(u32::from_be_bytes(prefix))
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "frame length does not fit usize"))?;
        if length > self.max_payload {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                format!("frame length {length} exceeds maximum {}", self.max_payload),
            ));
        }
        let total = PREFIX
            .checked_add(length)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "frame length overflow"))?;
        if src.len() < total {
            src.reserve(total - src.len());
            return Ok(None);
        }
        src.advance(PREFIX);
        Ok(Some(src.split_to(length).freeze()))
    }

    fn decode_eof(&mut self, src: &mut BytesMut) -> io::Result<Option<Self::Item>> {
        if let Some(frame) = self.decode(src)? {
            return Ok(Some(frame));
        }
        if src.is_empty() {
            Ok(None)
        } else {
            Err(io::Error::new(io::ErrorKind::UnexpectedEof, "truncated frame"))
        }
    }
}

impl Encoder<Bytes> for LengthCodec {
    type Error = io::Error;

    fn encode(&mut self, item: Bytes, dst: &mut BytesMut) -> io::Result<()> {
        if item.len() > self.max_payload || item.len() > u32::MAX as usize {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "frame exceeds configured maximum",
            ));
        }
        let length = u32::try_from(item.len())
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidInput, "frame length does not fit u32"))?;
        let encoded_len = 4_usize.checked_add(item.len()).ok_or_else(|| {
            io::Error::new(io::ErrorKind::InvalidInput, "encoded length overflow")
        })?;
        dst.reserve(encoded_len);
        dst.put_u32(length);
        dst.extend_from_slice(&item);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_split_points_decode_identically() {
        let payload = Bytes::from_static(b"hello");
        let mut encoded = BytesMut::new();
        LengthCodec::new(16).unwrap().encode(payload.clone(), &mut encoded).unwrap();
        for split in 0..=encoded.len() {
            let mut decoder = LengthCodec::new(16).unwrap();
            let mut buffer = BytesMut::new();
            buffer.extend_from_slice(&encoded[..split]);
            let first = decoder.decode(&mut buffer).unwrap();
            buffer.extend_from_slice(&encoded[split..]);
            let second = decoder.decode(&mut buffer).unwrap();
            assert_eq!(first.or(second), Some(payload.clone()));
            assert!(buffer.is_empty());
        }
    }

    #[test]
    fn rejects_oversized_prefix_before_payload() {
        let mut buffer = BytesMut::from(&u32::MAX.to_be_bytes()[..]);
        let error = LengthCodec::new(1024).unwrap().decode(&mut buffer).unwrap_err();
        assert_eq!(error.kind(), io::ErrorKind::InvalidData);
    }

    #[test]
    fn reports_truncated_eof() {
        let mut buffer = BytesMut::from(&[0, 0, 0, 3, b'a'][..]);
        let error = LengthCodec::new(16).unwrap().decode_eof(&mut buffer).unwrap_err();
        assert_eq!(error.kind(), io::ErrorKind::UnexpectedEof);
    }

    #[test]
    fn coalesced_frames_leave_the_next_frame_available() {
        let mut encoded = BytesMut::new();
        let mut encoder = LengthCodec::new(16).unwrap();
        encoder
            .encode(Bytes::from_static(b"one"), &mut encoded)
            .unwrap();
        encoder
            .encode(Bytes::from_static(b"two"), &mut encoded)
            .unwrap();

        let mut decoder = LengthCodec::new(16).unwrap();
        assert_eq!(
            decoder.decode(&mut encoded).unwrap(),
            Some(Bytes::from_static(b"one"))
        );
        assert_eq!(
            decoder.decode(&mut encoded).unwrap(),
            Some(Bytes::from_static(b"two"))
        );
        assert!(encoded.is_empty());
    }

    #[test]
    fn zero_maximum_is_rejected_at_construction() {
        assert!(LengthCodec::new(0).is_err());
    }

}

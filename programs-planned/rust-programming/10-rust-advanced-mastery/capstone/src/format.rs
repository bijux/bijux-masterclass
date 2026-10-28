use crate::{domain::validate_record_parts, Record, StoreError};

pub(crate) const MAGIC: [u8; 8] = *b"AXIOM01\0";
const HEADER_LEN: usize = 12;
const CHECKSUM_LEN: usize = 4;
const MIN_ENCODED_RECORD_LEN: usize = 8;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct RecordView<'a> {
    key: &'a str,
    value: &'a str,
}

impl<'a> RecordView<'a> {
    pub fn key(self) -> &'a str {
        self.key
    }

    pub fn value(self) -> &'a str {
        self.value
    }

    pub fn to_owned(&self) -> Result<Record, StoreError> {
        Record::new(self.key, self.value)
    }
}

pub(crate) trait RecordCodec<const MAX_RECORD: usize> {
    type View<'a>
    where
        Self: 'a;

    type DecodeError;

    fn decode<'a>(
        bytes: &'a [u8],
        offset: usize,
    ) -> Result<(Self::View<'a>, usize), Self::DecodeError>;

    fn encode(record: &Record, output: &mut Vec<u8>) -> Result<(), StoreError>;
}

pub(crate) struct Axiom01;

impl<const MAX_RECORD: usize> RecordCodec<MAX_RECORD> for Axiom01 {
    type View<'a>
        = RecordView<'a>
    where
        Self: 'a;

    type DecodeError = StoreError;

    fn decode<'a>(
        bytes: &'a [u8],
        offset: usize,
    ) -> Result<(Self::View<'a>, usize), Self::DecodeError> {
        let mut cursor = ByteCursor::at(bytes, offset)?;
        let start = cursor.position();

        let key_len = usize::try_from(cursor.u32()?).map_err(|_| StoreError::Format {
            offset: start,
            message: "key length does not fit usize".into(),
        })?;
        let minimum = 4_usize
            .checked_add(key_len)
            .and_then(|size| size.checked_add(4))
            .ok_or_else(|| StoreError::Format {
                offset: start,
                message: "record length overflows usize".into(),
            })?;
        if minimum > MAX_RECORD {
            return Err(StoreError::Format {
                offset: start,
                message: format!(
                    "declared key requires at least {minimum} record bytes; limit is {MAX_RECORD}"
                ),
            });
        }

        let key_offset = cursor.position();
        let key_bytes = cursor.take(key_len)?;
        let value_len = usize::try_from(cursor.u32()?).map_err(|_| StoreError::Format {
            offset: cursor.position().saturating_sub(4),
            message: "value length does not fit usize".into(),
        })?;
        let encoded_len = minimum
            .checked_add(value_len)
            .ok_or_else(|| StoreError::Format {
                offset: start,
                message: "record length overflows usize".into(),
            })?;
        if encoded_len > MAX_RECORD {
            return Err(StoreError::Format {
                offset: start,
                message: format!(
                    "declared record has {encoded_len} bytes; limit is {MAX_RECORD}"
                ),
            });
        }

        let value_offset = cursor.position();
        let value_bytes = cursor.take(value_len)?;
        let key = std::str::from_utf8(key_bytes).map_err(|error| StoreError::Format {
            offset: key_offset + error.valid_up_to(),
            message: "key is not valid UTF-8".into(),
        })?;
        let value = std::str::from_utf8(value_bytes).map_err(|error| StoreError::Format {
            offset: value_offset + error.valid_up_to(),
            message: "value is not valid UTF-8".into(),
        })?;

        validate_record_parts(key, value).map_err(|error| StoreError::Format {
            offset: start,
            message: error.to_string(),
        })?;

        Ok((RecordView { key, value }, cursor.position()))
    }

    fn encode(record: &Record, output: &mut Vec<u8>) -> Result<(), StoreError> {
        let encoded_len = 8_usize
            .checked_add(record.key().len())
            .and_then(|size| size.checked_add(record.value().len()))
            .ok_or_else(|| {
                StoreError::InvalidRecord("encoded record size overflows usize".into())
            })?;
        if encoded_len > MAX_RECORD {
            return Err(StoreError::InvalidRecord(format!(
                "encoded record has {encoded_len} bytes; limit is {MAX_RECORD}"
            )));
        }

        push_len(record.key().len(), output)?;
        output.extend_from_slice(record.key().as_bytes());
        push_len(record.value().len(), output)?;
        output.extend_from_slice(record.value().as_bytes());
        Ok(())
    }
}

pub(crate) fn encode_archive<const MAX_RECORD: usize>(
    records: &[Record],
) -> Result<Vec<u8>, StoreError> {
    let count = u32::try_from(records.len())
        .map_err(|_| StoreError::InvalidRecord("too many records".into()))?;
    let estimated_capacity = HEADER_LEN
        .saturating_add(records.len().saturating_mul(32))
        .saturating_add(CHECKSUM_LEN);
    let mut output = Vec::with_capacity(estimated_capacity);
    output.extend_from_slice(&MAGIC);
    output.extend_from_slice(&count.to_be_bytes());

    let mut previous: Option<&str> = None;
    for record in records {
        if previous.is_some_and(|key| key >= record.key()) {
            return Err(StoreError::InvalidRecord(
                "records must be strictly ordered by key".into(),
            ));
        }
        <Axiom01 as RecordCodec<MAX_RECORD>>::encode(record, &mut output)?;
        previous = Some(record.key());
    }

    let digest = checksum(&output);
    output.extend_from_slice(&digest.to_be_bytes());
    Ok(output)
}

pub(crate) fn verify_archive<const MAX_RECORD: usize>(
    bytes: &[u8],
) -> Result<usize, StoreError> {
    let checksum_start = bytes
        .len()
        .checked_sub(CHECKSUM_LEN)
        .ok_or_else(|| StoreError::Format {
            offset: 0,
            message: "archive is shorter than its checksum".into(),
        })?;
    if checksum_start < HEADER_LEN {
        return Err(StoreError::Format {
            offset: 0,
            message: "archive header is truncated".into(),
        });
    }

    if bytes.get(..MAGIC.len()) != Some(MAGIC.as_slice()) {
        let observed = bytes
            .get(..bytes.len().min(MAGIC.len()))
            .map(|prefix| {
                prefix
                    .iter()
                    .map(|byte| format!("{byte:02x}"))
                    .collect::<Vec<_>>()
                    .join("")
            })
            .unwrap_or_default();
        return Err(StoreError::UnsupportedVersion(observed));
    }

    let expected_bytes: [u8; 4] = bytes
        .get(checksum_start..)
        .ok_or_else(|| StoreError::Format {
            offset: checksum_start,
            message: "checksum is truncated".into(),
        })?
        .try_into()
        .map_err(|_| StoreError::Format {
            offset: checksum_start,
            message: "checksum has the wrong length".into(),
        })?;
    let expected = u32::from_be_bytes(expected_bytes);
    let actual = checksum(&bytes[..checksum_start]);
    if actual != expected {
        return Err(StoreError::Checksum { expected, actual });
    }

    let count_bytes: [u8; 4] = bytes
        .get(8..HEADER_LEN)
        .ok_or_else(|| StoreError::Format {
            offset: 8,
            message: "record count is truncated".into(),
        })?
        .try_into()
        .map_err(|_| StoreError::Format {
            offset: 8,
            message: "record count has the wrong length".into(),
        })?;
    let count = usize::try_from(u32::from_be_bytes(count_bytes)).map_err(|_| {
        StoreError::Format {
            offset: 8,
            message: "record count does not fit usize".into(),
        }
    })?;

    let available = checksum_start - HEADER_LEN;
    if count > available / MIN_ENCODED_RECORD_LEN {
        return Err(StoreError::Format {
            offset: 8,
            message: format!(
                "record count {count} cannot fit in {available} bytes"
            ),
        });
    }

    let mut offset = HEADER_LEN;
    let mut previous: Option<&str> = None;
    for _ in 0..count {
        let (view, next) = <Axiom01 as RecordCodec<MAX_RECORD>>::decode(bytes, offset)?;
        if previous.is_some_and(|key| key >= view.key()) {
            return Err(StoreError::Format {
                offset,
                message: "records are not strictly ordered by key".into(),
            });
        }
        previous = Some(view.key());
        offset = next;
    }

    if offset != checksum_start {
        return Err(StoreError::Format {
            offset,
            message: "archive contains trailing or unaccounted bytes".into(),
        });
    }
    Ok(count)
}

pub(crate) fn decode_owned<const MAX_RECORD: usize>(
    bytes: &[u8],
) -> Result<Vec<Record>, StoreError> {
    let count = verify_archive::<MAX_RECORD>(bytes)?;
    let mut records = Vec::with_capacity(count);
    let mut offset = HEADER_LEN;
    for _ in 0..count {
        let (view, next) = <Axiom01 as RecordCodec<MAX_RECORD>>::decode(bytes, offset)?;
        records.push(view.to_owned()?);
        offset = next;
    }
    Ok(records)
}

pub(crate) fn record_at<const MAX_RECORD: usize>(
    bytes: &[u8],
    offset: usize,
) -> Result<(RecordView<'_>, usize), StoreError> {
    <Axiom01 as RecordCodec<MAX_RECORD>>::decode(bytes, offset)
}

pub(crate) fn first_record_offset() -> usize {
    HEADER_LEN
}

fn push_len(length: usize, output: &mut Vec<u8>) -> Result<(), StoreError> {
    let length = u32::try_from(length)
        .map_err(|_| StoreError::InvalidRecord("field is too large to encode".into()))?;
    output.extend_from_slice(&length.to_be_bytes());
    Ok(())
}

fn checksum(bytes: &[u8]) -> u32 {
    bytes.iter().fold(2_166_136_261_u32, |hash, byte| {
        (hash ^ u32::from(*byte)).wrapping_mul(16_777_619)
    })
}

struct ByteCursor<'a> {
    bytes: &'a [u8],
    position: usize,
}

impl<'a> ByteCursor<'a> {
    fn at(bytes: &'a [u8], position: usize) -> Result<Self, StoreError> {
        if position > bytes.len() {
            return Err(StoreError::Format {
                offset: position,
                message: "cursor begins beyond input".into(),
            });
        }
        Ok(Self { bytes, position })
    }

    fn position(&self) -> usize {
        self.position
    }

    fn take(&mut self, length: usize) -> Result<&'a [u8], StoreError> {
        let end = self
            .position
            .checked_add(length)
            .ok_or_else(|| StoreError::Format {
                offset: self.position,
                message: "field range overflows usize".into(),
            })?;
        let slice = self
            .bytes
            .get(self.position..end)
            .ok_or_else(|| StoreError::Format {
                offset: self.position,
                message: format!("truncated field: need {length} bytes"),
            })?;
        self.position = end;
        Ok(slice)
    }

    fn u32(&mut self) -> Result<u32, StoreError> {
        let start = self.position;
        let bytes: [u8; 4] = self
            .take(4)?
            .try_into()
            .map_err(|_| StoreError::Format {
                offset: start,
                message: "truncated u32".into(),
            })?;
        Ok(u32::from_be_bytes(bytes))
    }
}

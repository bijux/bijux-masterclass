
#![deny(unsafe_op_in_unsafe_fn)]

use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Write};
use std::path::{Path, PathBuf};

pub const MAGIC: [u8; 4] = *b"PKT1";
pub const MAX_PAYLOAD: usize = 4096;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Packet {
    pub sequence: u32,
    pub payload: Vec<u8>,
}

#[derive(Debug)]
pub enum PacketError {
    UnexpectedEnd {
        offset: usize,
        needed: usize,
        remaining: usize,
    },
    BadMagic,
    TooLarge {
        declared: usize,
    },
    Checksum {
        offset: usize,
        expected: u32,
        actual: u32,
    },
    Trailing {
        offset: usize,
        count: usize,
    },
    Io {
        operation: &'static str,
        path: PathBuf,
        source: io::Error,
    },
}

impl fmt::Display for PacketError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for PacketError {}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u32 {
    bytes.iter().fold(0x811c_9dc5, |hash, byte| {
        (hash ^ u32::from(*byte)).wrapping_mul(0x0100_0193)
    })
}

fn take<'a>(
    bytes: &mut &'a [u8],
    offset: &mut usize,
    count: usize,
) -> Result<&'a [u8], PacketError> {
    let result = bytes.get(..count).ok_or(PacketError::UnexpectedEnd {
        offset: *offset,
        needed: count,
        remaining: bytes.len(),
    })?;
    *bytes = &bytes[count..];
    *offset += count;
    Ok(result)
}

pub fn decode(mut bytes: &[u8]) -> Result<Packet, PacketError> {
    let mut offset = 0_usize;
    if take(&mut bytes, &mut offset, MAGIC.len())? != MAGIC {
        return Err(PacketError::BadMagic);
    }
    let sequence_bytes = take(&mut bytes, &mut offset, 4)?;
    let sequence = u32::from_le_bytes([
        sequence_bytes[0],
        sequence_bytes[1],
        sequence_bytes[2],
        sequence_bytes[3],
    ]);
    let length_bytes = take(&mut bytes, &mut offset, 2)?;
    let length = usize::from(u16::from_le_bytes([length_bytes[0], length_bytes[1]]));
    if length > MAX_PAYLOAD {
        return Err(PacketError::TooLarge { declared: length });
    }
    let checksum_bytes = take(&mut bytes, &mut offset, 4)?;
    let expected = u32::from_le_bytes([
        checksum_bytes[0],
        checksum_bytes[1],
        checksum_bytes[2],
        checksum_bytes[3],
    ]);
    let payload_offset = offset;
    let payload = take(&mut bytes, &mut offset, length)?;
    let actual = fnv1a(payload);
    if actual != expected {
        return Err(PacketError::Checksum {
            offset: payload_offset,
            expected,
            actual,
        });
    }
    if !bytes.is_empty() {
        return Err(PacketError::Trailing {
            offset,
            count: bytes.len(),
        });
    }
    Ok(Packet {
        sequence,
        payload: payload.to_vec(),
    })
}

pub fn encode(packet: &Packet) -> Result<Vec<u8>, PacketError> {
    if packet.payload.len() > MAX_PAYLOAD {
        return Err(PacketError::TooLarge {
            declared: packet.payload.len(),
        });
    }
    let length = u16::try_from(packet.payload.len()).map_err(|_| PacketError::TooLarge {
        declared: packet.payload.len(),
    })?;
    let mut output = Vec::new();
    output.extend_from_slice(&MAGIC);
    output.extend_from_slice(&packet.sequence.to_le_bytes());
    output.extend_from_slice(&length.to_le_bytes());
    output.extend_from_slice(&fnv1a(&packet.payload).to_le_bytes());
    output.extend_from_slice(&packet.payload);
    Ok(output)
}

fn reserve_temporary(path: &Path) -> Result<(PathBuf, File), PacketError> {
    for attempt in 0..64_u32 {
        let temporary = path.with_extension(format!(
            "packet-tmp-{}-{attempt}",
            std::process::id()
        ));
        match OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&temporary)
        {
            Ok(file) => return Ok((temporary, file)),
            Err(error) if error.kind() == io::ErrorKind::AlreadyExists => continue,
            Err(source) => {
                return Err(PacketError::Io {
                    operation: "create temporary packet",
                    path: temporary,
                    source,
                });
            }
        }
    }
    Err(PacketError::Io {
        operation: "reserve temporary packet name",
        path: path.to_path_buf(),
        source: io::Error::new(io::ErrorKind::AlreadyExists, "temporary names exhausted"),
    })
}


fn commit_packet(
    mut file: File,
    temporary: &Path,
    destination: &Path,
    bytes: &[u8],
) -> Result<(), PacketError> {
    file.write_all(bytes).map_err(|source| PacketError::Io {
        operation: "write temporary packet",
        path: temporary.to_path_buf(),
        source,
    })?;
    file.flush().map_err(|source| PacketError::Io {
        operation: "flush temporary packet",
        path: temporary.to_path_buf(),
        source,
    })?;
    file.sync_all().map_err(|source| PacketError::Io {
        operation: "synchronize temporary packet",
        path: temporary.to_path_buf(),
        source,
    })?;
    drop(file);
    fs::rename(temporary, destination).map_err(|source| PacketError::Io {
        operation: "install packet",
        path: destination.to_path_buf(),
        source,
    })
}

pub fn write_packet_atomic(path: &Path, packet: &Packet) -> Result<(), PacketError> {
    let bytes = encode(packet)?;
    let parent = path
        .parent()
        .filter(|candidate| !candidate.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."));
    fs::create_dir_all(parent).map_err(|source| PacketError::Io {
        operation: "create packet directory",
        path: parent.to_path_buf(),
        source,
    })?;
    let (temporary, file) = reserve_temporary(path)?;
    let result = commit_packet(file, &temporary, path, &bytes);
    if result.is_err() {
        let _ = fs::remove_file(&temporary);
    }
    result
}

#[repr(C)]
#[derive(Default)]
pub struct PacketReport {
    pub sequence: u32,
    pub payload_len: u16,
    pub error_offset: usize,
}

/// Validate a packet and fill a C-compatible report.
///
/// # Safety
/// `out` must be non-null, aligned, and writable for one `PacketReport`. For a
/// nonzero `length`, `bytes` must identify a readable live range of that length
/// for the duration of the call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn packet_validate(
    bytes: *const u8,
    length: usize,
    out: *mut PacketReport,
) -> i32 {
    if out.is_null() {
        return 1;
    }
    // SAFETY: the caller provides one writable report and null was rejected.
    unsafe {
        out.write(PacketReport {
            error_offset: usize::MAX,
            ..PacketReport::default()
        });
    }
    let input = if length == 0 {
        &[]
    } else {
        if bytes.is_null() {
            return 1;
        }
        // SAFETY: the caller provides a readable range of the declared length.
        unsafe { std::slice::from_raw_parts(bytes, length) }
    };

    match std::panic::catch_unwind(|| decode(input)) {
        Ok(Ok(packet)) => {
            let payload_len = match u16::try_from(packet.payload.len()) {
                Ok(length) => length,
                Err(_) => return 2,
            };
            // SAFETY: the output report remains writable for this call.
            unsafe {
                out.write(PacketReport {
                    sequence: packet.sequence,
                    payload_len,
                    error_offset: usize::MAX,
                });
            }
            0
        }
        Ok(Err(PacketError::UnexpectedEnd { offset, .. }))
        | Ok(Err(PacketError::Trailing { offset, .. }))
        | Ok(Err(PacketError::Checksum { offset, .. })) => {
            // SAFETY: the report was initialized above and remains writable.
            unsafe { (*out).error_offset = offset };
            2
        }
        Ok(Err(_)) => 2,
        Err(_) => 3,
    }
}

#[cfg(test)]
mod tests {
    use super::{Packet, PacketReport, decode, encode, packet_validate};

    #[test]
    fn golden_prefix_round_trip_and_truncation() {
        let packet = Packet {
            sequence: 7,
            payload: b"abc".to_vec(),
        };
        let bytes = encode(&packet).expect("packet encodes");
        assert_eq!(&bytes[..4], b"PKT1");
        assert_eq!(decode(&bytes).expect("packet decodes"), packet);
        for cut in 0..bytes.len() {
            assert!(decode(&bytes[..cut]).is_err(), "cut={cut}");
        }
    }

    #[test]
    fn ffi_validator_reports_the_packet() {
        let bytes = encode(&Packet {
            sequence: 2,
            payload: Vec::new(),
        })
        .expect("packet encodes");
        let mut report = PacketReport::default();
        // SAFETY: input and output ranges remain live for the call.
        assert_eq!(
            unsafe { packet_validate(bytes.as_ptr(), bytes.len(), &raw mut report) },
            0
        );
        assert_eq!(report.sequence, 2);
    }
}

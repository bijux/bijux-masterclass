
//! A panic-contained C ABI over the safe archive decoder.
//!
//! The C header in `include/framevault.h` is the normative foreign-language
//! contract. Rust references, `String`, `Vec`, and `Result` do not cross this
//! boundary.

use crate::codec::{DecodeError, Limits, decode};
use crate::domain::Archive;
use std::ffi::{c_char, c_void};
use std::panic::{AssertUnwindSafe, catch_unwind};
use std::ptr;

pub const FV_OK: i32 = 0;
pub const FV_INVALID_ARGUMENT: i32 = 1;
pub const FV_INVALID_ARCHIVE: i32 = 2;
pub const FV_CALLBACK_STOPPED: i32 = 3;
pub const FV_PANIC_CONTAINED: i32 = 4;

/// Summary returned by the stateless validator.
#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FvReport {
    pub entry_count: u32,
    pub total_payload_bytes: u64,
    /// `usize::MAX` when no decode error was observed.
    pub error_offset: usize,
}

impl Default for FvReport {
    fn default() -> Self {
        Self {
            entry_count: 0,
            total_payload_bytes: 0,
            error_offset: usize::MAX,
        }
    }
}

/// A borrowed entry view valid only during one callback invocation.
#[repr(C)]
#[derive(Debug, Clone, Copy)]
pub struct FvEntryView {
    pub kind: u8,
    pub name_pointer: *const u8,
    pub name_length: usize,
    pub payload_pointer: *const u8,
    pub payload_length: usize,
}

/// Callback used by `framevault_for_each_entry`.
///
/// A zero return value continues iteration. Any other value stops iteration.
/// The callback must not unwind across the ABI boundary and must not retain the
/// borrowed pointers after it returns.
pub type FvEntryCallback = Option<
    unsafe extern "C" fn(context: *mut c_void, entry: *const FvEntryView) -> i32,
>;

/// Opaque owning session exposed to C only through a pointer.
pub struct FvSession {
    archive: Archive,
}

fn catch_status(action: impl FnOnce() -> i32) -> i32 {
    catch_unwind(AssertUnwindSafe(action)).unwrap_or(FV_PANIC_CONTAINED)
}

/// Borrow one raw byte range after applying the ABI null/length rule.
///
/// # Safety
/// When `length > 0`, `pointer` must be non-null and readable for exactly
/// `length` bytes for the returned lifetime. The memory must not be mutated for
/// the duration of that borrow.
unsafe fn borrowed_bytes<'a>(pointer: *const u8, length: usize) -> Result<&'a [u8], i32> {
    if length == 0 {
        return Ok(&[]);
    }
    if pointer.is_null() {
        return Err(FV_INVALID_ARGUMENT);
    }
    // SAFETY: the caller contract establishes a live readable range of exactly
    // `length` bytes, and the null case was rejected above.
    Ok(unsafe { std::slice::from_raw_parts(pointer, length) })
}

fn report_error(report: *mut FvReport, error: &DecodeError) {
    // SAFETY: every caller of this private helper validates `report` before the
    // helper is reached and keeps exclusive access for the duration of the call.
    unsafe {
        (*report).error_offset = error.offset();
    }
}

static VERSION: &[u8] = b"framevault-0.1.0\0";

/// Return a pointer to a process-lifetime NUL-terminated version string.
#[unsafe(no_mangle)]
pub extern "C" fn framevault_version() -> *const c_char {
    VERSION.as_ptr().cast()
}

/// Validate one complete archive buffer and fill `report`.
///
/// # Safety
/// `report` must be non-null, aligned, and writable for one `FvReport`. When
/// `length > 0`, `bytes` must be non-null and readable for `length` bytes for
/// the duration of the call. The report storage must not overlap the input byte
/// range.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn framevault_validate(
    bytes: *const u8,
    length: usize,
    report: *mut FvReport,
) -> i32 {
    catch_status(|| {
        if report.is_null() {
            return FV_INVALID_ARGUMENT;
        }
        // SAFETY: the public contract requires one writable report object and
        // the null case was rejected immediately above.
        unsafe { report.write(FvReport::default()) };
        // SAFETY: validity of the byte range is part of this function's public
        // safety contract; `borrowed_bytes` additionally enforces null/length.
        let input = match unsafe { borrowed_bytes(bytes, length) } {
            Ok(input) => input,
            Err(status) => return status,
        };
        match decode(input, Limits::default()) {
            Ok(archive) => {
                let count = match u32::try_from(archive.entry_count()) {
                    Ok(count) => count,
                    Err(_) => return FV_INVALID_ARCHIVE,
                };
                // SAFETY: `report` remains valid and exclusively writable for
                // this call, as required by the ABI contract.
                unsafe {
                    report.write(FvReport {
                        entry_count: count,
                        total_payload_bytes: archive.total_payload_bytes(),
                        error_offset: usize::MAX,
                    });
                }
                FV_OK
            }
            Err(error) => {
                report_error(report, &error);
                FV_INVALID_ARCHIVE
            }
        }
    })
}

/// Decode a buffer into an opaque owning session.
///
/// # Safety
/// `out_session` must be non-null, aligned, and writable for one session
/// pointer. When `length > 0`, `bytes` must be non-null and readable for
/// `length` bytes. The output slot must not overlap the input byte range. A
/// successful returned pointer must be released exactly once with
/// `framevault_free`.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn framevault_open(
    bytes: *const u8,
    length: usize,
    out_session: *mut *mut FvSession,
) -> i32 {
    catch_status(|| {
        if out_session.is_null() {
            return FV_INVALID_ARGUMENT;
        }
        // SAFETY: the caller promises a writable output slot and the null case
        // has been rejected.
        unsafe { out_session.write(ptr::null_mut()) };
        // SAFETY: the public function contract establishes the raw input range.
        let input = match unsafe { borrowed_bytes(bytes, length) } {
            Ok(input) => input,
            Err(status) => return status,
        };
        let archive = match decode(input, Limits::default()) {
            Ok(archive) => archive,
            Err(_) => return FV_INVALID_ARCHIVE,
        };
        let session = Box::new(FvSession { archive });
        // SAFETY: `out_session` is a live writable output slot, and ownership of
        // the allocation is transferred to the caller as a raw pointer.
        unsafe { out_session.write(Box::into_raw(session)) };
        FV_OK
    })
}

/// Return the number of entries in an open session.
///
/// # Safety
/// `session` must be a live pointer returned by `framevault_open` and not yet
/// freed. `out_count` must be non-null, aligned, and writable for one `usize`,
/// and its storage must be distinct from the session allocation. The session
/// must not be freed concurrently with this call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn framevault_entry_count(
    session: *const FvSession,
    out_count: *mut usize,
) -> i32 {
    catch_status(|| {
        if session.is_null() || out_count.is_null() {
            return FV_INVALID_ARGUMENT;
        }
        // SAFETY: both pointers are guaranteed live by the public contract and
        // were checked for null above.
        unsafe { out_count.write((*session).archive.entry_count()) };
        FV_OK
    })
}

/// Visit each entry in deterministic archive order.
///
/// # Safety
/// `session` must be a live pointer returned by `framevault_open` and not yet
/// freed. `callback` must be present, must obey its own pointer contract, and
/// must not unwind or retain any `FvEntryView` pointer or borrowed field pointer
/// after the callback returns. The callback must not free the active session;
/// the session must not be freed concurrently with this traversal. `context` is
/// passed through unchanged.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn framevault_for_each_entry(
    session: *const FvSession,
    context: *mut c_void,
    callback: FvEntryCallback,
) -> i32 {
    catch_status(|| {
        if session.is_null() {
            return FV_INVALID_ARGUMENT;
        }
        let Some(callback) = callback else {
            return FV_INVALID_ARGUMENT;
        };
        // SAFETY: the session pointer is live for the duration of this call by
        // the public contract, and no mutable access is created.
        let archive = unsafe { &(*session).archive };
        for entry in archive.entries() {
            let view = FvEntryView {
                kind: entry.kind().code(),
                name_pointer: entry.name().as_str().as_ptr(),
                name_length: entry.name().as_str().len(),
                payload_pointer: entry.payload().as_ptr(),
                payload_length: entry.payload_len(),
            };
            // SAFETY: the callback contract permits invocation with a pointer to
            // this live stack view. All borrowed fields outlive the invocation.
            let result = unsafe { callback(context, &raw const view) };
            if result != 0 {
                return FV_CALLBACK_STOPPED;
            }
        }
        FV_OK
    })
}

/// Release an opaque session. A null pointer is accepted as a no-op.
///
/// # Safety
/// A non-null pointer must have been returned by `framevault_open`, must still
/// be owned by the caller, and must not be passed to this function more than
/// once. No other thread or callback may access it after this call begins.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn framevault_free(session: *mut FvSession) -> i32 {
    catch_status(|| {
        if session.is_null() {
            return FV_OK;
        }
        // SAFETY: the public contract transfers the unique live allocation back
        // exactly once. Reconstructing the Box runs its destructor at scope end.
        unsafe { drop(Box::from_raw(session)) };
        FV_OK
    })
}

#[cfg(test)]
mod tests {
    use super::{
        FV_OK, FvEntryView, FvReport, FvSession, framevault_entry_count,
        framevault_for_each_entry, framevault_free, framevault_open,
        framevault_validate,
    };
    use crate::codec::{Limits, encode};
    use crate::domain::{Archive, Entry, EntryKind, LogicalPath};
    use std::ffi::c_void;
    use std::ptr;

    fn bytes() -> Vec<u8> {
        let archive = Archive::from_entries(vec![Entry::new(
            EntryKind::File,
            LogicalPath::parse("a.txt").expect("valid path"),
            b"a".to_vec(),
        )])
        .expect("unique fixture");
        encode(&archive, Limits::default()).expect("encodable fixture")
    }

    unsafe extern "C" fn count_callback(
        context: *mut c_void,
        entry: *const FvEntryView,
    ) -> i32 {
        if context.is_null() || entry.is_null() {
            return 1;
        }
        // SAFETY: the test passes one live `usize` as context and the FFI driver
        // passes one live view for this callback invocation.
        unsafe {
            let count = &mut *context.cast::<usize>();
            *count += usize::from((*entry).kind != 0);
        }
        0
    }

    #[test]
    fn stateless_and_session_apis_agree() {
        let bytes = bytes();
        let mut report = FvReport::default();
        // SAFETY: the byte slice and report out-pointer remain live for the call.
        assert_eq!(
            unsafe { framevault_validate(bytes.as_ptr(), bytes.len(), &raw mut report) },
            FV_OK
        );
        assert_eq!(report.entry_count, 1);

        let mut session: *mut FvSession = ptr::null_mut();
        // SAFETY: the input slice and session output slot remain live.
        assert_eq!(
            unsafe { framevault_open(bytes.as_ptr(), bytes.len(), &raw mut session) },
            FV_OK
        );
        assert!(!session.is_null());
        let mut count = 0_usize;
        // SAFETY: `session` is live and `count` is a writable output slot.
        assert_eq!(unsafe { framevault_entry_count(session, &raw mut count) }, FV_OK);
        assert_eq!(count, 1);

        let mut callbacks = 0_usize;
        // SAFETY: the session and callback context remain valid for the traversal.
        assert_eq!(
            unsafe {
                framevault_for_each_entry(
                    session,
                    (&raw mut callbacks).cast(),
                    Some(count_callback),
                )
            },
            FV_OK
        );
        assert_eq!(callbacks, 1);
        // SAFETY: ownership of this live session is returned exactly once.
        assert_eq!(unsafe { framevault_free(session) }, FV_OK);
    }
}

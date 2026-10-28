
use framevault::ffi::{
    FV_INVALID_ARGUMENT, FV_OK, FvReport, FvSession, framevault_free, framevault_open,
    framevault_validate,
};
use framevault::{Archive, Entry, EntryKind, Limits, LogicalPath, encode};
use std::ptr;

fn encoded_archive() -> Vec<u8> {
    let archive = Archive::from_entries(vec![Entry::new(
        EntryKind::File,
        LogicalPath::parse("ffi.bin").expect("valid path"),
        b"ffi".to_vec(),
    )])
    .expect("unique fixture");
    encode(&archive, Limits::default()).expect("encode fixture")
}

#[test]
fn zero_length_accepts_null_input_but_not_null_output() {
    let mut report = FvReport::default();
    // SAFETY: a null input is allowed for zero length, and `report` is writable.
    let status = unsafe { framevault_validate(ptr::null(), 0, &raw mut report) };
    assert_ne!(status, FV_INVALID_ARGUMENT);

    // SAFETY: the test deliberately violates only the documented output rule to
    // verify that the function rejects it before writing.
    assert_eq!(
        unsafe { framevault_validate(ptr::null(), 0, ptr::null_mut()) },
        FV_INVALID_ARGUMENT
    );
}

#[test]
fn session_ownership_has_one_explicit_release() {
    let bytes = encoded_archive();
    let mut session: *mut FvSession = ptr::null_mut();
    // SAFETY: input and output ranges remain live for this call.
    assert_eq!(
        unsafe { framevault_open(bytes.as_ptr(), bytes.len(), &raw mut session) },
        FV_OK
    );
    assert!(!session.is_null());
    // SAFETY: ownership of the live session is returned exactly once.
    assert_eq!(unsafe { framevault_free(session) }, FV_OK);
    // SAFETY: null is documented as a no-op.
    assert_eq!(unsafe { framevault_free(ptr::null_mut()) }, FV_OK);
}


#![deny(unsafe_op_in_unsafe_fn)]

use std::ffi::c_void;
use std::panic::{AssertUnwindSafe, catch_unwind};
use std::ptr;

pub struct CounterSession {
    value: i64,
}

pub type VisitCallback = unsafe extern "C" fn(
    context: *mut c_void,
    value: i64,
) -> i32;

pub const OK: i32 = 0;
pub const INVALID: i32 = 1;
pub const OVERFLOW: i32 = 2;
pub const STOPPED: i32 = 3;
pub const PANIC_CONTAINED: i32 = 4;

fn boundary(action: impl FnOnce() -> i32) -> i32 {
    catch_unwind(AssertUnwindSafe(action)).unwrap_or(PANIC_CONTAINED)
}

/// Allocate one opaque counter session.
///
/// # Safety
/// `out` must be non-null, aligned, and writable for one session pointer. On
/// success, the returned pointer is uniquely owned by the caller and must be
/// passed exactly once to `counter_free`.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_open(
    initial: i64,
    out: *mut *mut CounterSession,
) -> i32 {
    boundary(|| {
        if out.is_null() {
            return INVALID;
        }
        // SAFETY: the caller contract supplies one writable output slot.
        unsafe { out.write(ptr::null_mut()) };
        let raw = Box::into_raw(Box::new(CounterSession { value: initial }));
        // SAFETY: the output slot remains valid; ownership transfers to C.
        unsafe { out.write(raw) };
        OK
    })
}

/// Add to a live session without changing it on overflow.
///
/// # Safety
/// `session` must be the unique live pointer returned by `counter_open` and
/// `out` must be non-null, aligned, and writable for one `i64`.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_add(
    session: *mut CounterSession,
    delta: i64,
    out: *mut i64,
) -> i32 {
    boundary(|| {
        if session.is_null() || out.is_null() {
            return INVALID;
        }
        // SAFETY: the public contract grants unique live access for this call.
        let session = unsafe { &mut *session };
        let Some(value) = session.value.checked_add(delta) else {
            return OVERFLOW;
        };
        session.value = value;
        // SAFETY: `out` is a live writable result slot by contract.
        unsafe { out.write(value) };
        OK
    })
}

/// Read the current value from a live session.
///
/// # Safety
/// `session` must be live and readable for this call. `out` must be non-null,
/// aligned, and writable for one `i64`.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_get(
    session: *const CounterSession,
    out: *mut i64,
) -> i32 {
    boundary(|| {
        if session.is_null() || out.is_null() {
            return INVALID;
        }
        // SAFETY: both pointer contracts are established by the caller.
        unsafe { out.write((*session).value) };
        OK
    })
}

/// Invoke a callback synchronously with the current value `count` times.
///
/// # Safety
/// `session` must remain live and immutable during traversal. `callback` must be
/// present, must not unwind, free or mutate the session, or retain borrowed
/// session-derived pointers. `context` is passed through unchanged.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_visit(
    session: *const CounterSession,
    count: u32,
    context: *mut c_void,
    callback: Option<VisitCallback>,
) -> i32 {
    boundary(|| {
        if session.is_null() {
            return INVALID;
        }
        let Some(callback) = callback else {
            return INVALID;
        };
        // SAFETY: the session remains live and readable by public contract.
        let value = unsafe { (*session).value };
        for _ in 0..count {
            // SAFETY: callback validity and synchronous context lifetime are
            // requirements of the public unsafe contract.
            if unsafe { callback(context, value) } != 0 {
                return STOPPED;
            }
        }
        OK
    })
}

/// Release one opaque session. Null is accepted as a no-op.
///
/// # Safety
/// A non-null pointer must be the unique live pointer returned by
/// `counter_open`, and must not have been freed previously.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_free(session: *mut CounterSession) -> i32 {
    boundary(|| {
        if session.is_null() {
            return OK;
        }
        // SAFETY: the caller transfers the unique allocation back exactly once.
        unsafe { drop(Box::from_raw(session)) };
        OK
    })
}

#[cfg(test)]
mod tests {
    use super::{
        OK, OVERFLOW, CounterSession, counter_add, counter_free, counter_get,
        counter_open, counter_visit,
    };
    use std::ffi::c_void;
    use std::ptr;

    unsafe extern "C" fn collect(context: *mut c_void, value: i64) -> i32 {
        if context.is_null() {
            return 1;
        }
        // SAFETY: the test passes a live `Vec<i64>` as callback context.
        unsafe { &mut *context.cast::<Vec<i64>>() }.push(value);
        0
    }

    #[test]
    fn lifecycle_callback_and_checked_update() {
        let mut raw: *mut CounterSession = ptr::null_mut();
        // SAFETY: output slot is writable and remains live.
        assert_eq!(unsafe { counter_open(7, &raw mut raw) }, OK);
        let mut value = 0_i64;
        // SAFETY: session and output remain live for the call.
        assert_eq!(unsafe { counter_add(raw, 2, &raw mut value) }, OK);
        assert_eq!(value, 9);

        let mut values = Vec::new();
        // SAFETY: session and context remain live; callback is synchronous.
        assert_eq!(
            unsafe {
                counter_visit(
                    raw,
                    3,
                    (&raw mut values).cast(),
                    Some(collect),
                )
            },
            OK
        );
        assert_eq!(values, [9, 9, 9]);
        // SAFETY: ownership is returned exactly once.
        assert_eq!(unsafe { counter_free(raw) }, OK);
    }

    #[test]
    fn overflow_preserves_the_old_value() {
        let mut raw: *mut CounterSession = ptr::null_mut();
        // SAFETY: output slot is writable.
        assert_eq!(unsafe { counter_open(i64::MAX, &raw mut raw) }, OK);
        let mut value = 0_i64;
        // SAFETY: live session and output slot.
        assert_eq!(unsafe { counter_add(raw, 1, &raw mut value) }, OVERFLOW);
        // SAFETY: live session and output slot.
        assert_eq!(unsafe { counter_get(raw, &raw mut value) }, OK);
        assert_eq!(value, i64::MAX);
        // SAFETY: one release of the live session.
        assert_eq!(unsafe { counter_free(raw) }, OK);
    }

    #[test]
    fn null_free_is_allowed() {
        // SAFETY: null is explicitly documented as a no-op.
        assert_eq!(unsafe { counter_free(ptr::null_mut()) }, OK);
    }
}

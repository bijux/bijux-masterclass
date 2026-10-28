
#![deny(unsafe_op_in_unsafe_fn)]

#[repr(C)]
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct LineReport {
    pub lines: u32,
    pub bytes: usize,
    /// `usize::MAX` when no UTF-8 error was observed.
    pub invalid_offset: usize,
}

pub const OK: i32 = 0;
pub const INVALID_ARGUMENT: i32 = 1;
pub const INVALID_UTF8: i32 = 2;
pub const PANIC_CONTAINED: i32 = 3;

fn analyze(input: &[u8]) -> Result<LineReport, usize> {
    std::str::from_utf8(input).map_err(|error| error.valid_up_to())?;
    let line_count = if input.is_empty() {
        0
    } else {
        input.iter().filter(|byte| **byte == b'\n').count()
            + usize::from(!input.ends_with(b"\n"))
    };
    Ok(LineReport {
        lines: u32::try_from(line_count).unwrap_or(u32::MAX),
        bytes: input.len(),
        invalid_offset: usize::MAX,
    })
}

/// Fill a line report for one borrowed byte range.
///
/// # Safety
/// `out` must be non-null, aligned, and writable for one `LineReport`. When
/// `length > 0`, `bytes` must be non-null and readable for `length` bytes for
/// the duration of the call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn line_report(
    bytes: *const u8,
    length: usize,
    out: *mut LineReport,
) -> i32 {
    if out.is_null() {
        return INVALID_ARGUMENT;
    }
    // SAFETY: the caller contract supplies one writable aligned report pointer,
    // and the null case was rejected above.
    unsafe {
        out.write(LineReport {
            invalid_offset: usize::MAX,
            ..LineReport::default()
        });
    }

    let input = if length == 0 {
        &[]
    } else {
        if bytes.is_null() {
            return INVALID_ARGUMENT;
        }
        // SAFETY: the caller contract provides one live readable range of the
        // exact requested length, and the null case was rejected.
        unsafe { std::slice::from_raw_parts(bytes, length) }
    };

    match std::panic::catch_unwind(|| analyze(input)) {
        Ok(Ok(report)) => {
            // SAFETY: the same output contract remains valid for this call.
            unsafe { out.write(report) };
            OK
        }
        Ok(Err(offset)) => {
            // SAFETY: the report was initialized above and remains writable.
            unsafe { (*out).invalid_offset = offset };
            INVALID_UTF8
        }
        Err(_) => PANIC_CONTAINED,
    }
}

#[cfg(test)]
mod tests {
    use super::{INVALID_ARGUMENT, OK, LineReport, line_report};
    use std::ptr;

    #[test]
    fn valid_call_reports_lines() {
        let input = b"a\nb";
        let mut report = LineReport::default();
        // SAFETY: input and output ranges remain live for the call.
        let code = unsafe { line_report(input.as_ptr(), input.len(), &raw mut report) };
        assert_eq!(code, OK);
        assert_eq!(report.lines, 2);
    }

    #[test]
    fn null_rules_are_explicit() {
        let mut report = LineReport::default();
        // SAFETY: null is allowed for a zero-length input and report is writable.
        assert_eq!(
            unsafe { line_report(ptr::null(), 0, &raw mut report) },
            OK
        );
        // SAFETY: this deliberately tests the documented null/nonzero rejection.
        assert_eq!(
            unsafe { line_report(ptr::null(), 1, &raw mut report) },
            INVALID_ARGUMENT
        );
        // SAFETY: this deliberately tests null output rejection before writing.
        assert_eq!(
            unsafe { line_report(ptr::null(), 0, ptr::null_mut()) },
            INVALID_ARGUMENT
        );
    }
}

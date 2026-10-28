
#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Analysis {
    pub lines: u32,
    pub bytes: usize,
}

pub fn analyze(input: &[u8]) -> Result<Analysis, usize> {
    std::str::from_utf8(input).map_err(|error| error.valid_up_to())?;
    let line_count = if input.is_empty() {
        0
    } else {
        input.iter().filter(|byte| **byte == b'\n').count()
            + usize::from(!input.ends_with(b"\n"))
    };
    Ok(Analysis {
        lines: u32::try_from(line_count).unwrap_or(u32::MAX),
        bytes: input.len(),
    })
}

#[cfg(test)]
mod tests {
    use super::analyze;

    #[test]
    fn safe_core_counts_lines() {
        assert_eq!(analyze(b"a\nb").expect("valid text").lines, 2);
        assert_eq!(analyze(b"a\n").expect("valid text").lines, 1);
    }
}

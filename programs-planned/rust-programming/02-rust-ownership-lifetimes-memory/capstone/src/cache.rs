use std::ops::Range;

/// Line-index data derived from one exact document revision.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct DocumentCache {
    pub(crate) revision: u64,
    pub(crate) lines: Vec<Range<usize>>,
}

/// Compute byte ranges for logical lines without allocating line strings.
///
/// A trailing line ending does not create an additional empty logical line.
/// Both `\n` and `\r\n` endings are excluded from the returned ranges.
pub(crate) fn line_ranges(text: &str) -> Vec<Range<usize>> {
    if text.is_empty() {
        return Vec::new();
    }

    let mut ranges = Vec::new();
    let mut start = 0;

    for segment in text.split_inclusive('\n') {
        let without_newline = segment.strip_suffix('\n').unwrap_or(segment);
        let content = without_newline
            .strip_suffix('\r')
            .unwrap_or(without_newline);
        ranges.push(start..start + content.len());
        start += segment.len();
    }

    ranges
}

#[cfg(test)]
mod tests {
    use super::line_ranges;

    #[test]
    fn derives_ranges_for_lf_and_crlf_lines() {
        assert_eq!(line_ranges("a\nb\r\nc"), vec![0..1, 2..3, 5..6]);
    }

    #[test]
    fn empty_text_has_no_logical_lines() {
        assert!(line_ranges("").is_empty());
    }
}

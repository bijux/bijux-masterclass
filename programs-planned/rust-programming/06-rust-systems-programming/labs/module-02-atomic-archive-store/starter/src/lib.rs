
#![forbid(unsafe_code)]

use std::path::{Path, PathBuf};

#[must_use]
pub fn candidate_name(destination: &Path, attempt: u32) -> PathBuf {
    let file = destination
        .file_name()
        .unwrap_or_default()
        .to_string_lossy();
    destination.with_file_name(format!(
        ".{file}.{}.{}.tmp",
        std::process::id(),
        attempt
    ))
}

#[must_use]
pub fn encode_lines(lines: &[&str]) -> Vec<u8> {
    let mut output = lines.join("\n").into_bytes();
    output.push(b'\n');
    output
}

#[cfg(test)]
mod tests {
    use super::{candidate_name, encode_lines};
    use std::path::Path;

    #[test]
    fn candidate_stays_beside_destination() {
        let path = Path::new("state/data.bin");
        assert_eq!(candidate_name(path, 2).parent(), path.parent());
    }

    #[test]
    fn line_encoding_is_deterministic() {
        assert_eq!(encode_lines(&["a", "b"]), b"a\nb\n");
    }
}

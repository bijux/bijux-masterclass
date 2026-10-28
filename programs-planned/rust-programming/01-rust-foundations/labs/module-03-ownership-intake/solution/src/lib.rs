//! Reference implementation for an ownership-transferring intake pipeline.

/// Maximum accepted normalized title length in UTF-8 bytes.
pub const MAX_TITLE_BYTES: usize = 80;

/// Consumes and normalizes one title.
pub fn normalize(raw: String) -> String {
    let mut output = String::with_capacity(raw.len());
    let mut pending_space = false;

    for character in raw.chars() {
        if character.is_whitespace() {
            if !output.is_empty() {
                pending_space = true;
            }
            continue;
        }
        if pending_space {
            output.push(' ');
            pending_space = false;
        }
        output.push(character.to_ascii_lowercase());
    }

    output
}

/// Consumes one raw title and moves its normalized value into one output partition.
pub fn ingest(
    mut accepted: Vec<String>,
    mut rejected: Vec<String>,
    raw: String,
) -> (Vec<String>, Vec<String>) {
    let normalized = normalize(raw);
    if normalized.is_empty() || normalized.len() > MAX_TITLE_BYTES {
        rejected.push(normalized);
    } else {
        accepted.push(normalized);
    }
    (accepted, rejected)
}

/// Consumes all incoming titles and preserves their relative order within each partition.
pub fn ingest_all(
    mut accepted: Vec<String>,
    mut rejected: Vec<String>,
    incoming: Vec<String>,
) -> (Vec<String>, Vec<String>) {
    for raw in incoming {
        (accepted, rejected) = ingest(accepted, rejected, raw);
    }
    (accepted, rejected)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn normalization_collapses_unicode_whitespace_and_ascii_case() {
        let raw = String::from(" \tRUST\u{2003}Ownership\nModel ");
        assert_eq!(normalize(raw), "rust ownership model");
    }

    #[test]
    fn empty_normalized_value_is_retained_as_rejection() {
        let (accepted, rejected) = ingest(Vec::new(), Vec::new(), String::from(" \n\t "));
        assert!(accepted.is_empty());
        assert_eq!(rejected, vec![String::new()]);
    }

    #[test]
    fn exact_ascii_boundary_is_accepted() {
        let value = "x".repeat(MAX_TITLE_BYTES);
        let (accepted, rejected) = ingest(Vec::new(), Vec::new(), value.clone());
        assert_eq!(accepted, vec![value]);
        assert!(rejected.is_empty());
    }

    #[test]
    fn boundary_is_measured_in_utf8_bytes() {
        let accepted_value = "é".repeat(40);
        let rejected_value = "é".repeat(41);
        let (accepted, rejected) = ingest_all(
            Vec::new(),
            Vec::new(),
            vec![accepted_value.clone(), rejected_value.clone()],
        );
        assert_eq!(accepted, vec![accepted_value]);
        assert_eq!(rejected, vec![rejected_value]);
    }

    #[test]
    fn partition_preserves_relative_order_and_existing_values() {
        let accepted = vec![String::from("existing accepted")];
        let rejected = vec![String::from("existing rejected")];
        let incoming = vec![
            String::from(" First "),
            String::new(),
            String::from("SECOND"),
            "z".repeat(MAX_TITLE_BYTES + 1),
        ];
        let (accepted, rejected) = ingest_all(accepted, rejected, incoming);
        assert_eq!(accepted, vec!["existing accepted", "first", "second"]);
        assert_eq!(rejected[0], "existing rejected");
        assert_eq!(rejected[1], "");
        assert_eq!(rejected[2], "z".repeat(MAX_TITLE_BYTES + 1));
    }

    #[test]
    fn empty_batch_returns_original_owners() {
        let accepted = vec![String::from("a")];
        let rejected = vec![String::from("b")];
        assert_eq!(
            ingest_all(accepted, rejected, Vec::new()),
            (vec![String::from("a")], vec![String::from("b")])
        );
    }
}

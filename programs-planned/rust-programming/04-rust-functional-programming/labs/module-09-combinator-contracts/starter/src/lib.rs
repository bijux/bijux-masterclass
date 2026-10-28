#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FieldError<E> {
    pub field: &'static str,
    pub source: E,
}

pub fn normalize(value: &str) -> String {
    value
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
        .to_ascii_lowercase()
}

#[cfg(test)]
mod tests {
    use super::normalize;

    #[test]
    fn starter_normalization_is_idempotent_for_a_baseline_case() {
        let once = normalize(" A   B ");
        assert_eq!(normalize(&once), once);
    }
}

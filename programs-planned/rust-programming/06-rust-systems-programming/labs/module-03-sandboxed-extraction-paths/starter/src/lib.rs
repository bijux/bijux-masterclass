
#![forbid(unsafe_code)]

#[must_use]
pub fn split_logical(input: &str) -> Vec<&str> {
    input.split('/').collect()
}

#[must_use]
pub fn contains_forbidden_component(input: &str) -> bool {
    split_logical(input)
        .iter()
        .any(|part| part.is_empty() || matches!(*part, "." | ".."))
}

#[cfg(test)]
mod tests {
    use super::contains_forbidden_component;

    #[test]
    fn sees_parent_component() {
        assert!(contains_forbidden_component("a/../b"));
    }

    #[test]
    fn allows_dots_inside_name() {
        assert!(!contains_forbidden_component("a/report..txt"));
    }
}

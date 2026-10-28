//! Compiling baseline for the borrowed-catalog laboratory.
//!
//! Reference-returning and mutation APIs are intentionally absent because their
//! signatures are the primary design result of this lab.

/// Returns the total UTF-8 byte length of all titles without taking ownership.
pub fn total_bytes(titles: &[String]) -> usize {
    titles.iter().map(String::len).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn catalog() -> Vec<String> {
        vec![
            String::from("Rust"),
            String::from("Ownership"),
            String::from("借用"),
        ]
    }

    #[test]
    fn baseline_traversal_borrows_and_counts_bytes() {
        let titles = catalog();
        let expected = "Rust".len() + "Ownership".len() + "借用".len();
        assert_eq!(total_bytes(&titles), expected);
        assert_eq!(titles.len(), 3);
    }
}

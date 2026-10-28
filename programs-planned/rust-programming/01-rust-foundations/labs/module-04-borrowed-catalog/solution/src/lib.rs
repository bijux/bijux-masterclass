//! Reference implementation for a catalog with capability-narrow borrowing APIs.

/// Reports whether any title exactly matches `query`.
pub fn contains_exact(titles: &[String], query: &str) -> bool {
    titles.iter().any(|title| title == query)
}

/// Borrows the first exactly matching title from the catalog.
pub fn find_first<'a>(titles: &'a [String], query: &str) -> Option<&'a str> {
    titles.iter().find(|title| title.as_str() == query).map(String::as_str)
}

/// Replaces the first match without changing the slice length.
pub fn rename_first(titles: &mut [String], query: &str, replacement: String) -> bool {
    let Some(title) = titles.iter_mut().find(|title| title.as_str() == query) else {
        return false;
    };
    *title = replacement;
    true
}

/// Transfers ownership of one title into the catalog.
pub fn append(titles: &mut Vec<String>, title: String) {
    titles.push(title);
}

/// Returns the total UTF-8 byte length of all titles.
pub fn total_bytes(titles: &[String]) -> usize {
    titles.iter().map(String::len).sum()
}

/// Borrows the first title with maximal UTF-8 byte length.
pub fn longest(titles: &[String]) -> Option<&str> {
    let mut longest: Option<&String> = None;
    for title in titles {
        if longest.is_none_or(|current| title.len() > current.len()) {
            longest = Some(title);
        }
    }
    longest.map(String::as_str)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn catalog() -> Vec<String> {
        vec![String::from("Rust"), String::from("Ownership"), String::from("借用")]
    }

    #[test]
    fn lookup_borrows_original_storage() {
        let titles = catalog();
        let found = find_first(&titles, "Ownership").expect("title exists");
        assert_eq!(found, "Ownership");
        assert_eq!(found.as_ptr(), titles[1].as_ptr());
        assert!(contains_exact(&titles, "借用"));
    }

    #[test]
    fn query_lifetime_is_not_tied_to_result() {
        let titles = catalog();
        let found = {
            let query = String::from("Rust");
            find_first(&titles, &query).expect("title exists")
        };
        assert_eq!(found, "Rust");
    }

    #[test]
    fn rename_changes_one_slot_not_length() {
        let mut titles = catalog();
        let before = titles.len();
        assert!(rename_first(&mut titles, "Rust", String::from("Rust 2024")));
        assert_eq!(titles.len(), before);
        assert_eq!(titles[0], "Rust 2024");
        assert!(!rename_first(&mut titles, "missing", String::from("unused")));
    }

    #[test]
    fn append_changes_length_and_takes_ownership() {
        let mut titles = catalog();
        let title = String::from("Traits");
        append(&mut titles, title);
        assert_eq!(titles.last().map(String::as_str), Some("Traits"));
    }

    #[test]
    fn byte_measurement_handles_non_ascii_without_indexing() {
        let titles = catalog();
        assert_eq!(total_bytes(&titles), "Rust".len() + "Ownership".len() + "借用".len());
    }

    #[test]
    fn longest_selects_first_tie_and_empty_is_none() {
        let titles = vec![String::from("first"), String::from("other")];
        assert_eq!(longest(&titles), Some("first"));
        assert_eq!(longest(&[]), None);
    }
}

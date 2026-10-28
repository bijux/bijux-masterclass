use std::borrow::Cow;

/// Run `operation` with a normalized query whose borrow cannot escape.
///
/// Normalization trims leading and trailing Unicode whitespace and collapses
/// each internal whitespace run to one ASCII space. If the input is already in
/// canonical form, the callback receives a slice borrowed from `raw`; otherwise
/// it receives a slice of temporary owned storage. The higher-ranked callback
/// prevents callers from returning a reference tied to either path.
pub fn with_normalized_query<R>(
    raw: &str,
    operation: impl for<'query> FnOnce(&'query str) -> R,
) -> R {
    let normalized = normalize_query(raw);
    operation(normalized.as_ref())
}

pub(crate) fn normalize_query(raw: &str) -> Cow<'_, str> {
    let trimmed = raw.trim();
    let already_canonical = trimmed
        .chars()
        .try_fold(false, |previous_was_space, character| {
            if character.is_whitespace() {
                if previous_was_space || character != ' ' {
                    None
                } else {
                    Some(true)
                }
            } else {
                Some(false)
            }
        })
        .is_some();

    if already_canonical {
        Cow::Borrowed(trimmed)
    } else {
        Cow::Owned(trimmed.split_whitespace().collect::<Vec<_>>().join(" "))
    }
}

#[cfg(test)]
mod tests {
    use super::{normalize_query, with_normalized_query};
    use std::borrow::Cow;

    #[test]
    fn canonical_input_stays_borrowed() {
        assert!(matches!(normalize_query(" query "), Cow::Borrowed("query")));
    }

    #[test]
    fn noncanonical_input_becomes_owned() {
        assert!(matches!(
            normalize_query("query\twith   gaps"),
            Cow::Owned(value) if value == "query with gaps"
        ));
    }

    #[test]
    fn callback_can_export_owned_results() {
        let result = with_normalized_query(" query ", str::to_owned);
        assert_eq!(result, "query");
    }
}

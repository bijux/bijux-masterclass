#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FieldError<E> {
    pub field: &'static str,
    pub source: E,
}

pub fn both<T, P, Q>(mut first: P, mut second: Q) -> impl FnMut(&T) -> bool
where
    P: FnMut(&T) -> bool,
    Q: FnMut(&T) -> bool,
{
    move |value| first(value) && second(value)
}

pub fn either<T, P, Q>(mut first: P, mut second: Q) -> impl FnMut(&T) -> bool
where
    P: FnMut(&T) -> bool,
    Q: FnMut(&T) -> bool,
{
    move |value| first(value) || second(value)
}

pub fn negate<T, P>(mut predicate: P) -> impl FnMut(&T) -> bool
where
    P: FnMut(&T) -> bool,
{
    move |value| !predicate(value)
}

pub fn compose<A, B, C, F, G>(mut first: F, mut second: G) -> impl FnMut(A) -> C
where
    F: FnMut(A) -> B,
    G: FnMut(B) -> C,
{
    move |value| second(first(value))
}

pub fn on_field<T, U, E, F>(
    field: &'static str,
    mut function: F,
) -> impl FnMut(T) -> Result<U, FieldError<E>>
where
    F: FnMut(T) -> Result<U, E>,
{
    move |value| function(value).map_err(|source| FieldError { field, source })
}

pub fn normalize(value: &str) -> String {
    value
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
        .to_ascii_lowercase()
}

pub fn matching<'a, T, P>(
    items: &'a [T],
    mut predicate: P,
) -> impl Iterator<Item = &'a T> + 'a
where
    P: FnMut(&T) -> bool + 'a,
{
    items.iter().filter(move |item| predicate(*item))
}

pub fn collect_matching<T, P>(items: &[T], predicate: P) -> Vec<T>
where
    T: Clone,
    P: FnMut(&T) -> bool,
{
    matching(items, predicate).cloned().collect()
}

#[cfg(test)]
mod tests {
    use super::{both, collect_matching, compose, matching, normalize, on_field};
    use std::cell::Cell;

    #[test]
    fn boolean_composition_preserves_short_circuit_order() {
        let second_calls = Cell::new(0);
        let mut predicate = both(
            |value: &i32| *value > 0,
            |_: &i32| {
                second_calls.set(second_calls.get() + 1);
                true
            },
        );
        assert!(!predicate(&-1));
        assert_eq!(second_calls.get(), 0);
        assert!(predicate(&1));
        assert_eq!(second_calls.get(), 1);
    }

    #[test]
    fn composition_accepts_stateful_functions() {
        let mut calls = 0;
        let mut function = compose(|value| value + 1, |value| {
            calls += 1;
            value * calls
        });
        assert_eq!(function(2), 3);
        assert_eq!(function(2), 6);
    }

    #[test]
    fn normalization_is_idempotent_over_a_small_domain() {
        for source in ["", " A ", "a  b", "A\tB"] {
            let once = normalize(source);
            assert_eq!(normalize(&once), once);
        }
    }

    #[test]
    fn context_adapter_preserves_typed_source_error() {
        let mut parse = on_field("amount", |text: &str| text.parse::<u64>());
        assert_eq!(parse("x").unwrap_err().field, "amount");
    }

    #[test]
    fn lazy_and_eager_surfaces_are_distinct() {
        let values = [1, 2, 3, 4];
        assert_eq!(
            matching(&values, |value| *value % 2 == 0)
                .copied()
                .collect::<Vec<_>>(),
            vec![2, 4]
        );
        assert_eq!(collect_matching(&values, |value| *value > 2), vec![3, 4]);
    }
}

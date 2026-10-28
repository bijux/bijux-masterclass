
#![forbid(unsafe_code)]

pub fn pair_mut_safe<T>(
    slice: &mut [T],
    first: usize,
    second: usize,
) -> Option<(&mut T, &mut T)> {
    if first == second || first >= slice.len() || second >= slice.len() {
        return None;
    }
    if first < second {
        let (left, right) = slice.split_at_mut(second);
        Some((&mut left[first], &mut right[0]))
    } else {
        let (left, right) = slice.split_at_mut(first);
        Some((&mut right[0], &mut left[second]))
    }
}

#[cfg(test)]
mod tests {
    use super::pair_mut_safe;

    #[test]
    fn safe_baseline_preserves_argument_order() {
        let mut values = [1, 2, 3];
        let (first, second) = pair_mut_safe(&mut values, 2, 0).expect("valid pair");
        *first = 30;
        *second = 10;
        assert_eq!(values, [10, 2, 30]);
    }
}

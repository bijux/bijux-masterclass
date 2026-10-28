
#![deny(unsafe_op_in_unsafe_fn)]

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

pub fn pair_mut<T>(
    slice: &mut [T],
    first: usize,
    second: usize,
) -> Option<(&mut T, &mut T)> {
    if first == second || first >= slice.len() || second >= slice.len() {
        return None;
    }
    let pointer = slice.as_mut_ptr();
    // SAFETY: both indices were checked against this slice's length and are
    // distinct. The input `&mut [T]` grants exclusive access to the allocation
    // for the returned lifetime, so the two element references cannot alias.
    unsafe {
        Some((
            &mut *pointer.add(first),
            &mut *pointer.add(second),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::{pair_mut, pair_mut_safe};

    #[test]
    fn both_orders_match_the_safe_reference() {
        for (first, second) in [(0, 2), (2, 0), (1, 3), (3, 1)] {
            let mut actual = [0, 1, 2, 3];
            let mut reference = actual;
            {
                let (left, right) = pair_mut(&mut actual, first, second).expect("valid pair");
                *left += 10;
                *right += 20;
            }
            {
                let (left, right) = pair_mut_safe(&mut reference, first, second)
                    .expect("valid reference pair");
                *left += 10;
                *right += 20;
            }
            assert_eq!(actual, reference);
        }
    }

    #[test]
    fn invalid_inputs_do_not_mutate() {
        let mut values = [1, 2];
        assert!(pair_mut(&mut values, 0, 0).is_none());
        assert!(pair_mut(&mut values, 0, 2).is_none());
        assert_eq!(values, [1, 2]);
    }
}


#![forbid(unsafe_code)]

pub fn try_build_vec<T, E>(
    count: usize,
    mut build: impl FnMut(usize) -> Result<T, E>,
) -> Result<Vec<T>, E> {
    let mut values = Vec::with_capacity(count);
    for index in 0..count {
        values.push(build(index)?);
    }
    Ok(values)
}

#[cfg(test)]
mod tests {
    use super::try_build_vec;

    #[test]
    fn safe_baseline_stops_on_error() {
        let mut seen = Vec::new();
        let result: Result<Vec<usize>, usize> = try_build_vec(5, |index| {
            seen.push(index);
            if index == 2 { Err(index) } else { Ok(index) }
        });
        assert_eq!(result, Err(2));
        assert_eq!(seen, [0, 1, 2]);
    }
}

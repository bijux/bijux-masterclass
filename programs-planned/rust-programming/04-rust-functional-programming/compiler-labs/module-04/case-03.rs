fn main() {
    let total: Result<i32, &str> = [1_i32, 2, 3]
        .into_iter()
        .try_fold(0_i32, |sum, value| sum.checked_add(value).ok_or("overflow"));
    assert_eq!(total, Ok(6));
}

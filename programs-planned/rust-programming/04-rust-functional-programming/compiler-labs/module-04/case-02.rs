fn main() {
    let empty: Option<i32> = std::iter::empty().reduce(|left, right| left + right);
    assert_eq!(empty, None);
}

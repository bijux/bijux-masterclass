fn main() {
    let total = [1, 2, 3].into_iter().fold(0, |sum, value| sum + value);
    assert_eq!(total, 6);
}

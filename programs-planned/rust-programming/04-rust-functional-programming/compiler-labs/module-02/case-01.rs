fn main() {
    let values = vec![1, 2, 3];
    let total: i32 = values.iter().copied().sum();
    assert_eq!(total, 6);
    assert_eq!(values.len(), 3);
}

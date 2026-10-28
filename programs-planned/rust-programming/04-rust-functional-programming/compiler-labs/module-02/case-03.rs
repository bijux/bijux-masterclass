fn main() {
    let mut values = vec![1, 2, 3];
    for value in values.iter_mut() { *value *= 2; }
    assert_eq!(values, vec![2, 4, 6]);
}

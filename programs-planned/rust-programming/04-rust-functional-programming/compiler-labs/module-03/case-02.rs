fn main() {
    let values: Vec<_> = [Some(1), None, Some(3)].into_iter().flatten().collect();
    assert_eq!(values, vec![1, 3]);
}

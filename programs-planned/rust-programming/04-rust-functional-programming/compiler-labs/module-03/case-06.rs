fn main() {
    let values: Vec<_> = [1, 3]
        .into_iter()
        .flat_map(|end| 0..end)
        .collect();
    assert_eq!(values, vec![0, 0, 1, 2]);
}

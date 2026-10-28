fn main() {
    let values: Vec<i32> = ["1", "x", "3"]
        .into_iter()
        .filter_map(|text| text.parse().ok())
        .collect();
    assert_eq!(values, vec![1, 3]);
}

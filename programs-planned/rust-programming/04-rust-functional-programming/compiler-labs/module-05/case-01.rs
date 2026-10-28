fn main() {
    let values: Result<Vec<i32>, _> = ["1", "2"].into_iter().map(str::parse).collect();
    assert_eq!(values.unwrap(), vec![1, 2]);
}

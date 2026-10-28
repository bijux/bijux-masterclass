fn main() {
    let pairs: Vec<_> = ["a", "b"].into_iter().zip([1, 2]).collect();
    assert_eq!(pairs, vec![("a", 1), ("b", 2)]);
}

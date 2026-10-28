fn main() {
    let mut iterator = 0..6;
    let first: Vec<_> = iterator.by_ref().take(2).collect();
    let rest: Vec<_> = iterator.collect();
    assert_eq!(first, vec![0, 1]);
    assert_eq!(rest, vec![2, 3, 4, 5]);
}

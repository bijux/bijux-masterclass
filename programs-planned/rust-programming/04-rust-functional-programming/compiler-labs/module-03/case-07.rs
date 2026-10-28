fn main() {
    let positions: Vec<_> = [10, 11, 12]
        .into_iter()
        .enumerate()
        .filter(|(_, value)| value % 2 == 0)
        .collect();
    assert_eq!(positions, vec![(0, 10), (2, 12)]);
}

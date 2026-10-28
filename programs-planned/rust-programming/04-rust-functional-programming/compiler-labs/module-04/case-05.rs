fn main() {
    let totals: Vec<_> = [2, 3, -1]
        .into_iter()
        .scan(0, |sum, value| { *sum += value; Some(*sum) })
        .collect();
    assert_eq!(totals, vec![2, 5, 4]);
}

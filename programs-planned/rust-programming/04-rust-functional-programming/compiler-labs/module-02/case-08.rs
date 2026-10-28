fn main() {
    let values = [1, 2, 3];
    let _program = values.iter().map(|value| value * 10);
    assert_eq!(values[0], 1);
}

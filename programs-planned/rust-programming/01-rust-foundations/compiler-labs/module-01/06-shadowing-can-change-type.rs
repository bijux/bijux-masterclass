// Predict before compiling.
fn main() {
    let value = " 42 ";
    let value = value.trim();
    let value = value.parse::<u32>();
    assert_eq!(value, Ok(42));
}

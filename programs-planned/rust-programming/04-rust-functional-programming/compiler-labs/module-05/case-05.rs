#[derive(Debug, PartialEq)] struct FieldError<E> { field: &'static str, source: E }
fn main() {
    let result = "x".parse::<u8>().map_err(|source| FieldError { field: "age", source });
    assert_eq!(result.unwrap_err().field, "age");
}

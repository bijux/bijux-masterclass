fn main() {
    let token = String::from("fallback");
    let result = None::<String>.unwrap_or_else(move || token);
    assert_eq!(result, "fallback");
}

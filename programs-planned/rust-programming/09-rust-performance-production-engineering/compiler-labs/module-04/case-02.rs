fn promote(field: &str) -> String { field.to_owned() } fn main() { let owned = promote("metric"); assert_eq!(owned, "metric"); }

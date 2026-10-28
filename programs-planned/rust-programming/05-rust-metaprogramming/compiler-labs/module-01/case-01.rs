fn normalize(input: &str) -> String { input.trim().to_ascii_lowercase() }
fn main() { assert_eq!(normalize("  ALPHA "), "alpha"); }

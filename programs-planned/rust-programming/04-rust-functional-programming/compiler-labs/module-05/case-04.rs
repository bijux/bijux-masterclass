fn parse_optional(text: &str) -> Option<i32> {
    Some(text.parse::<i32>()?)
}
fn main() { let _ = parse_optional("1"); }

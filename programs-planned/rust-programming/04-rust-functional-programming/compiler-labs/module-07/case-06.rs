fn renamed() -> &'static str {
    let value = String::from("new");
    value.as_str()
}
fn main() { let _ = renamed(); }

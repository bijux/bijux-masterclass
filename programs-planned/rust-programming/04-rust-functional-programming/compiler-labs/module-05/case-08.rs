fn parse_all() -> Result<Vec<i32>, String> {
    ["1", "x"].into_iter().map(str::parse::<i32>).collect()
}
fn main() { let _ = parse_all(); }

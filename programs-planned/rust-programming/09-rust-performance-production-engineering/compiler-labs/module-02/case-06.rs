fn select<'a>(left: &'a str, right: &str) -> &'a str { right } fn main() { println!("{}", select("a", "b")); }

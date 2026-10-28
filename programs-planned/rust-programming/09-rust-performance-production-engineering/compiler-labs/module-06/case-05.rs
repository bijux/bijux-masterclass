fn label<'a>() -> &'a str { let value = String::from("dynamic"); &value } fn main() { println!("{}", label()); }

fn retryable(code: &str) -> bool { match code { "TEMP" => true } } fn main() { println!("{}", retryable("X")); }

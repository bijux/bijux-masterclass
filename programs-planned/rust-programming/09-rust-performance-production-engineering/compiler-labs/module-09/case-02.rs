fn valid_digest(value:&str)->bool { value.len()==64 && value.bytes().all(|b|b.is_ascii_hexdigit()) } fn main(){ assert!(valid_digest(&"a".repeat(64))); }

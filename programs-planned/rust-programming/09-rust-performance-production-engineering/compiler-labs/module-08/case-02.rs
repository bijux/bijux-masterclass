fn allowed(byte: u8) -> bool { byte.is_ascii_alphanumeric() || matches!(byte,b'-'|b'_'|b'.') } fn main() { assert!(b"safe-name".iter().copied().all(allowed)); }

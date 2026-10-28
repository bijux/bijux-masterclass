fn classify(kind: std::io::ErrorKind) -> u8 { match kind { std::io::ErrorKind::NotFound => 1, std::io::ErrorKind::PermissionDenied => 2 } }
fn main() { let _ = classify(std::io::ErrorKind::NotFound); }

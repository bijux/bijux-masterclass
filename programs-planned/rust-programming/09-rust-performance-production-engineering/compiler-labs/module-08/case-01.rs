struct Secret(String);

impl Secret {
    fn byte_len(&self) -> usize {
        self.0.len()
    }
}

impl std::fmt::Debug for Secret {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str("[REDACTED]")
    }
}

fn main() {
    let secret = Secret("token".into());
    assert_eq!(secret.byte_len(), 5);
    assert_eq!(format!("{secret:?}"), "[REDACTED]");
}

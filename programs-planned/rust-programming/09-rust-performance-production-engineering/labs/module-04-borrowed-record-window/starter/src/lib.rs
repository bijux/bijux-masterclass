use bytes::Bytes;

#[derive(Debug, Clone)]
pub struct RecordWindow {
    bytes: Bytes,
}

impl RecordWindow {
    pub fn new(bytes: Bytes) -> Self {
        Self { bytes }
    }

    pub fn as_bytes(&self) -> &[u8] {
        &self.bytes
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exposes_the_window() {
        let window = RecordWindow::new(Bytes::from_static(b"a\t1\n"));
        assert_eq!(window.as_bytes(), b"a\t1\n");
    }
}

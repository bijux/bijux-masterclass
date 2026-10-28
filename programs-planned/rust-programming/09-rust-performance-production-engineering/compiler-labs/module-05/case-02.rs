#[derive(Clone, Copy)] struct Batch { items: usize, bytes: usize } fn flush(b: Batch) -> bool { b.items >= 64 || b.bytes >= 32768 } fn main() { assert!(flush(Batch { items: 2, bytes: 40000 })); }

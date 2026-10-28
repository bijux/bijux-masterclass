fn main() { let mut v = Vec::with_capacity(1024); v.extend_from_slice(b"x"); v.clear(); assert_eq!(v.len(), 0); assert!(v.capacity() >= 1024); }

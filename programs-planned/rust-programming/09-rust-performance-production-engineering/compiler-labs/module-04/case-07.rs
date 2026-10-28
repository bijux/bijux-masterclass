fn main() { let data = vec![1_u8; 1024]; let tiny = &data[0..4]; assert_eq!(tiny.len(), 4); assert_eq!(data.len(), 1024); }

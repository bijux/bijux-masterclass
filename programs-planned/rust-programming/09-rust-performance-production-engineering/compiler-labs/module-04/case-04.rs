fn copied_bytes(fields: &[&str]) -> Option<usize> { fields.iter().try_fold(0_usize, |n, f| n.checked_add(f.len())) } fn main() { assert_eq!(copied_bytes(&["a","bc"]), Some(3)); }

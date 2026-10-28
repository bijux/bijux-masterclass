fn view(data: &[u8], range: std::ops::Range<usize>) -> Option<&[u8]> { data.get(range) } fn main() { assert_eq!(view(b"abcd", 1..3), Some(&b"bc"[..])); }

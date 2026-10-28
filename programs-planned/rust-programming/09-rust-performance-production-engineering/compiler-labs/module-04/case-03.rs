fn chunks(data: &[u8]) -> impl Iterator<Item=&[u8]> { data.chunks(3) } fn main() { assert_eq!(chunks(b"abcdefg").count(), 3); }

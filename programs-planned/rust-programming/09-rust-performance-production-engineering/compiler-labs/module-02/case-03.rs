fn candidates<'a>(values: &'a [u64], threshold: u64) -> impl Iterator<Item=&'a u64> { values.iter().filter(move |&&v| v >= threshold) } fn main() { assert_eq!(candidates(&[1,3,2], 2).count(), 2); }

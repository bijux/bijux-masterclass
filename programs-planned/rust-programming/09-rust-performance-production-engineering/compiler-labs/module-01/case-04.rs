#[derive(Clone, Copy)] struct Case { size: usize } fn main() { let cases = [Case { size: 64 }, Case { size: 4096 }]; assert_eq!(cases.iter().map(|c| c.size).sum::<usize>(), 4160); }

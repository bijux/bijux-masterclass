#![allow(dead_code)]
#[derive(Debug, PartialEq)] enum Timed<T> { Completed(T), Deadline, Cancelled }
fn classify<T>(value: Option<T>, cancelled: bool) -> Timed<T> { if cancelled { Timed::Cancelled } else { value.map_or(Timed::Deadline, Timed::Completed) } }
fn main() { assert_eq!(classify(Some(3), false), Timed::Completed(3)); }

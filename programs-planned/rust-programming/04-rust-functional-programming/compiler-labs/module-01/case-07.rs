fn offset_by(offset: i32) -> impl Fn(i32) -> i32 { move |value| value + offset }
fn main() { assert_eq!(offset_by(4)(3), 7); }

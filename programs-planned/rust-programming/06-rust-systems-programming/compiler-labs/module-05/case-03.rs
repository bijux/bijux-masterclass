#![allow(dead_code, unused_imports, unused_variables)]
unsafe trait TrustedZero { fn zero() -> Self; } struct Byte(u8); // SAFETY: `Byte::zero` returns the only promised valid zero representation.
 unsafe impl TrustedZero for Byte { fn zero() -> Self { Self(0) } } fn main() { assert_eq!(Byte::zero().0,0); }

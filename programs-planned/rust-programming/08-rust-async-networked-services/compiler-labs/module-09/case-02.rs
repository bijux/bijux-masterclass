#![allow(dead_code)]
fn retry<F: FnMut(u8) -> Result<u8, ()>>(mut operation: F) -> Result<u8, ()> { for attempt in 0..3 { if let Ok(value)=operation(attempt) { return Ok(value); } } Err(()) }
fn main() { let mut failures = 0u8; let result = retry(|_| { failures += 1; (failures >= 2).then_some(7).ok_or(()) }); assert_eq!(result, Ok(7)); }

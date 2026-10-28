#![allow(dead_code)]
use std::{marker::PhantomPinned, pin::Pin};
struct AddressSensitive { value: u8, _pin: PhantomPinned }
fn observe(value: Pin<&AddressSensitive>) -> u8 { value.get_ref().value }
fn main() { let value = Box::pin(AddressSensitive { value: 9, _pin: PhantomPinned }); assert_eq!(observe(value.as_ref()), 9); }

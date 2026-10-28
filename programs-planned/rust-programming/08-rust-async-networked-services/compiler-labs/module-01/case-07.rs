#![allow(dead_code)]
use std::{marker::PhantomPinned, pin::Pin};
struct Fixed { _pin: PhantomPinned }
fn take(_: Fixed) {}
fn main() { let value = Box::pin(Fixed { _pin: PhantomPinned }); take(*value); }

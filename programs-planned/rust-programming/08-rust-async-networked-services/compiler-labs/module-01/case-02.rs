#![allow(dead_code)]
use std::{future::Future, pin::Pin, task::{Context, Poll}};
struct Immediate(Option<u8>);
impl Future for Immediate {
    type Output = u8;
    fn poll(mut self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<u8> {
        Poll::Ready(self.0.take().unwrap_or(0))
    }
}
fn main() { let future = Immediate(Some(7)); let _ = Box::pin(future); }

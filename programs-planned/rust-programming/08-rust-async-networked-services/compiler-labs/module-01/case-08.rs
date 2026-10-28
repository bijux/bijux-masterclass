#![allow(dead_code)]
use std::{future::Future, task::{Context, Poll}};
struct Wrong;
impl Future for Wrong {
    type Output = ();
    fn poll(&mut self, _: &mut Context<'_>) -> Poll<()> { Poll::Ready(()) }
}
fn main() {}

#![allow(dead_code)]
use std::{future::Future, task::{Context, Poll, Waker}, pin::Pin};
struct RememberWaker { saved: Option<Waker> }
impl Future for RememberWaker {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        self.saved = Some(cx.waker().clone());
        Poll::Pending
    }
}
fn main() { let _ = RememberWaker { saved: None }; }

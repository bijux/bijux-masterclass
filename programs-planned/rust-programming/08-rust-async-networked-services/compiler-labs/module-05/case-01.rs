#![allow(dead_code)]
#[derive(Clone, Copy)] enum Session { AwaitHello, Ready, Closing }
fn accepts_jobs(state: Session) -> bool { match state { Session::Ready => true, Session::AwaitHello | Session::Closing => false } }
fn main() { assert!(accepts_jobs(Session::Ready)); }

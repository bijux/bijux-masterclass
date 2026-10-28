#![allow(dead_code)]
enum Session { AwaitHello, Ready, Closing }
fn label(state: Session) -> &'static str { match state { Session::AwaitHello => "hello", Session::Ready => "ready" } }
fn main() {}

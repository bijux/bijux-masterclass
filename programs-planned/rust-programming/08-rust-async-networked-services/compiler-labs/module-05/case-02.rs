#![allow(dead_code)]
#[derive(Clone, Copy, PartialEq, Eq)] struct RequestId(u64);
#[derive(Clone, Copy, PartialEq, Eq)] struct ConnectionId(u64);
fn complete(_: RequestId) {}
fn main() { complete(RequestId(9)); let _ = ConnectionId(9); }

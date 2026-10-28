#![allow(dead_code)]
struct RequestId(u64); struct ConnectionId(u64);
fn complete(_: RequestId) {}
fn main() { complete(ConnectionId(4)); }

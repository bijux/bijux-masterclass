#![allow(dead_code)]
#[derive(Clone, Copy)] enum Shutdown { Running, Quiescing, Draining, Stopped }
fn may_accept(state: Shutdown) -> bool { matches!(state, Shutdown::Running) }
fn main() { assert!(!may_accept(Shutdown::Draining)); }

#![allow(dead_code)]
struct State { accepted: usize, completed: usize }
fn main() { let mut state = State { accepted: 0, completed: 0 }; let accepted = &mut state.accepted; let whole = &mut state; *accepted += 1; whole.completed += 1; }

#![allow(dead_code)]
struct CompletionGuard<'a>(&'a mut bool);
impl Drop for CompletionGuard<'_> { fn drop(&mut self) { *self.0 = true; } }
fn main() { let mut completed = false; { let _guard = CompletionGuard(&mut completed); } assert!(completed); }

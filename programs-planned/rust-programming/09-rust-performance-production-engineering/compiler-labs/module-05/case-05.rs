use std::cell::RefCell; use std::sync::Arc; use std::thread; fn main() { let state = Arc::new(RefCell::new(0)); thread::spawn(move || *state.borrow_mut() += 1); }

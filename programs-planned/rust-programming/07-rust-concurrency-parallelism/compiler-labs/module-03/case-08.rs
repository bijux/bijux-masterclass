use std::sync::Mutex; use std::thread;
fn main(){ let m=Mutex::new(1); let h=thread::spawn(move || m.lock().is_ok()); let _=m.lock(); let _=h.join(); }

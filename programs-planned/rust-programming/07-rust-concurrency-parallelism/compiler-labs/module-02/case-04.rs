use std::thread;
fn main(){ thread::scope(|s| { let a=s.spawn(||1); let b=s.spawn(||2); let _=(a.join(),b.join()); }); }

use std::sync::atomic::AtomicUsize;
fn main(){ let a=AtomicUsize::new(0); let _b=a; let _c=a; }

use std::sync::Barrier;
fn main(){ let b=Barrier::new(2); let _=b.clone(); }

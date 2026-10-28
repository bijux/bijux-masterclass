use std::sync::OnceLock;
fn main(){ let c=OnceLock::new(); assert_eq!(c.set(7),Ok(())); assert_eq!(c.get(),Some(&7)); }

use std::sync::OnceLock;
fn main(){ let c=OnceLock::new(); let _=c.set(1u32); let _: Option<&String>=c.get(); }

use std::mem::MaybeUninit;
fn main(){ let slot=MaybeUninit::<u32>::uninit(); let _:u32=*slot; }

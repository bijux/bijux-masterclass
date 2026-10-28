use std::cell::UnsafeCell;
fn main(){ let cell=UnsafeCell::new(1u8); let _=cell.get(); }

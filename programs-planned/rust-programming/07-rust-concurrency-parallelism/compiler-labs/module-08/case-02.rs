use std::mem::MaybeUninit;
fn main(){ let mut slot=MaybeUninit::<u32>::uninit(); slot.write(7); let value=unsafe{slot.assume_init()}; assert_eq!(value,7); }

use std::mem::MaybeUninit;fn main(){let mut x=MaybeUninit::uninit();x.write(7_u8);let y=unsafe{x.assume_init()};assert_eq!(y,7);}

// outcome: fail
// lesson: Raw representation copying crosses an unsafe boundary

#[repr(C)]struct H{a:u32}fn main(){let h=H{a:1};let _bytes:[u8;4]=std::mem::transmute(h);}

// outcome: pass
// lesson: repr(C) permits target-based field layout calculation
#[repr(C)]struct H{
    a:u8,b:u32,c:u16
}
fn main(){
    println!("{} {}",std::mem::size_of::<H>(),std::mem::align_of::<H>());
}

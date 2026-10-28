// outcome: pass
// lesson: as_mut creates shorter pinned reborrows
use std::pin::Pin;
fn touch(_:Pin<&mut String>){
}
fn main(){
    let mut p=Box::pin(String::from("x"));
    touch(p.as_mut());
    touch(p.as_mut());
}

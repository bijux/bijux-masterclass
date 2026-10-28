// outcome: pass
// lesson: An address can be observed without dereferencing raw pointers
use std::ptr::NonNull;
fn main(){
    let value=Box::pin(String::from("x"));
    let a=NonNull::from(value.as_ref().get_ref());
    let b=NonNull::from(value.as_ref().get_ref());
    assert_eq!(a,b);
}

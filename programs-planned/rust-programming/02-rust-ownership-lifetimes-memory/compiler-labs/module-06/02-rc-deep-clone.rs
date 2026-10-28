// outcome: pass
// lesson: Cloning the pointee creates a distinct allocation
use std::rc::Rc;
fn main(){
    let a=Rc::new(String::from("x"));
    let b=Rc::new((*a).clone());
    assert!(!Rc::ptr_eq(&a,&b));
    assert_eq!(a,b);
}

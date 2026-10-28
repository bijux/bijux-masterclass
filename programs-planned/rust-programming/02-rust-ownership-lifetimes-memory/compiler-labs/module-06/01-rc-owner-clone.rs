// outcome: pass
// lesson: Rc clone shares one allocation
use std::rc::Rc;
fn main(){
    let a=Rc::new(String::from("x"));
    let b=Rc::clone(&a);
    assert!(Rc::ptr_eq(&a,&b));
}

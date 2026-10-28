// outcome: pass
// lesson: Equal values can occupy distinct allocations
use std::rc::Rc;
fn main(){
    let a=Rc::new(1);
    let b=Rc::new(1);
    assert_eq!(a,b);
    assert!(!Rc::ptr_eq(&a,&b));
}

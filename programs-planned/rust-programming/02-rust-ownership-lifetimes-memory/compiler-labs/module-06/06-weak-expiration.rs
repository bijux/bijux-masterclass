// outcome: pass
// lesson: Weak upgrade reports liveness
use std::rc::Rc;
fn main(){
    let a=Rc::new(1);
    let w=Rc::downgrade(&a);
    drop(a);
    assert!(w.upgrade().is_none());
}

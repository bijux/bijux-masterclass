// outcome: pass
// lesson: Fallible dynamic borrowing exposes conflict
use std::cell::RefCell;
fn main(){
    let c=RefCell::new(1);
    let _r=c.borrow();
    assert!(c.try_borrow_mut().is_err());
}

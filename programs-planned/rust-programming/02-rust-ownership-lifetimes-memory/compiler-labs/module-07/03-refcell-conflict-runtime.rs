// outcome: pass
// lesson: Overlapping dynamic borrows compile but panic at runtime
use std::cell::RefCell;
fn main(){
    let c=RefCell::new(1);
    let _r=c.borrow();
    if false{
        let _w=c.borrow_mut();
    }
}

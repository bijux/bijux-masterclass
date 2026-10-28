// outcome: pass
// lesson: Interior mutation can construct a strong cycle
use std::cell::RefCell;
use std::rc::Rc;
struct N{
    edge:RefCell<Option<Rc<N>>>
}
fn main(){
    let n=Rc::new(N{
        edge:RefCell::new(None)
    });
    *n.edge.borrow_mut()=Some(Rc::clone(&n));
}

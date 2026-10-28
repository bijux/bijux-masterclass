// outcome: pass
// lesson: A strong cycle can compile and leak
use std::cell::RefCell;
use std::rc::Rc;
struct N{
    next:RefCell<Option<Rc<N>>>
}
fn main(){
    let a=Rc::new(N{
        next:RefCell::new(None)
    });
    let b=Rc::new(N{
        next:RefCell::new(Some(Rc::clone(&a)))
    });
    *a.next.borrow_mut()=Some(Rc::clone(&b));
}

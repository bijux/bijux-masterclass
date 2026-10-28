// outcome: pass
// lesson: Nested public methods can hide a runtime panic path
use std::cell::RefCell;
struct C{
    v:RefCell<i32>
}
impl C{
    fn inner(&self){
        *self.v.borrow_mut()+=1;
    }
    fn outer(&self){
        let _g=self.v.borrow_mut();
        if false{
            self.inner();
        }
    }
}
fn main(){
    C{
        v:RefCell::new(0)
    }
    .outer();
}

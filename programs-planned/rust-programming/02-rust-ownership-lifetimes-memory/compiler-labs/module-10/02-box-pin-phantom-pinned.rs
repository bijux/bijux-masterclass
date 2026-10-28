// outcome: pass
// lesson: Box::pin safely pins a !Unpin value
use std::marker::PhantomPinned;
struct T{
    _p:PhantomPinned
}
fn main(){
    let _p=Box::pin(T{
        _p:PhantomPinned
    });
}

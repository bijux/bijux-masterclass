// outcome: fail
// lesson: Unrestricted mutable access is unavailable for !Unpin
use std::marker::PhantomPinned;
struct T{
    _p:PhantomPinned
}
fn main(){
    let mut p=Box::pin(T{
        _p:PhantomPinned
    });
    let _r:&mut T=p.as_mut().get_mut();
}

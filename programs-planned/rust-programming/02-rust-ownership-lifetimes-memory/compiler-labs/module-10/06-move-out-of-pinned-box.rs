// outcome: fail
// lesson: A !Unpin pointee cannot be moved out through Pin<Box<T>>
use std::marker::PhantomPinned;
struct T{
    _p:PhantomPinned
}
fn main(){
    let p=Box::pin(T{
        _p:PhantomPinned
    });
    let _t:T=*p;
}

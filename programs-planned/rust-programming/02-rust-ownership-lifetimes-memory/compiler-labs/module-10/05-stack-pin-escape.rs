// outcome: fail
// lesson: A pinned stack borrow cannot escape its storage lifetime
use std::marker::PhantomPinned;
use std::pin::{
    pin,Pin
};
struct T{
    _p:PhantomPinned
}
fn bad<'a>()->Pin<&'a mut T>{
    let p=pin!(T{
        _p:PhantomPinned
    });
    p
}
fn main(){
}

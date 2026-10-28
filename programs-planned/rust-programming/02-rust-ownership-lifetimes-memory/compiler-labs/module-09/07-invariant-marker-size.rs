// outcome: pass
// lesson: An invariant marker is zero-sized but type-significant
use std::marker::PhantomData;
struct Brand<'a>(PhantomData<fn(&'a())->&'a()>);
fn main(){
    assert_eq!(std::mem::size_of::<Brand<'static>>(),0);
}

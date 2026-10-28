// outcome: fail
// lesson: Generative invariant brands cannot mix

use std::marker::PhantomData;
struct Arena<'id> { _m: PhantomData<fn(&'id ()) -> &'id ()> }
#[derive(Clone, Copy)]
struct Id<'id> { _m: PhantomData<fn(&'id ()) -> &'id ()> }
fn with<R>(f: impl for<'id> FnOnce(&Arena<'id>, Id<'id>) -> R) -> R {
    f(&Arena { _m: PhantomData }, Id { _m: PhantomData })
}
fn require_same<'id>(_: Id<'id>, _: Id<'id>) {}
fn main() {
    with(|_first, first_id| {
        with(|_second, second_id| {
            require_same(first_id, second_id);
        });
    });
}

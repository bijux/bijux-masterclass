// outcome: pass
// lesson: T: ?Sized accepts a str referent
fn bytes<T:?Sized>(v:&T)->usize{
    std::mem::size_of_val(v)
}
fn main(){
    assert_eq!(bytes::<str>("abc"),3);
}

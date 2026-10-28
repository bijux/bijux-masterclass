// outcome: pass
// lesson: Dropping a guard ends its mutable borrow
fn main(){
    let mut s=String::from("a");
    let r=&mut s;
    r.push('b');
    drop(r);
    s.push('c');
    assert_eq!(s,"abc");
}

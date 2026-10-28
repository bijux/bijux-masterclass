// outcome: pass
// lesson: make_mut clones on shared mutation
use std::rc::Rc;
fn main(){
    let mut a=Rc::new(String::from("x"));
    let b=Rc::clone(&a);
    Rc::make_mut(&mut a).push('!');
    assert_eq!(a.as_str(),"x!");
    assert_eq!(b.as_str(),"x");
}

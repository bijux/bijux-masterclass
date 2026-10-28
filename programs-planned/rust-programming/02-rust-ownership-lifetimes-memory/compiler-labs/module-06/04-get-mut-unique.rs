// outcome: pass
// lesson: get_mut succeeds while owner is unique
use std::rc::Rc;
fn main(){
    let mut a=Rc::new(String::from("x"));
    if let Some(v)=Rc::get_mut(&mut a){
        v.push('!');
    }
    assert_eq!(a.as_str(),"x!");
}

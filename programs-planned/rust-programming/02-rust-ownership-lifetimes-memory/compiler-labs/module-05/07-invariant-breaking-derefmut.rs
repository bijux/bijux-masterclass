// outcome: pass
// lesson: DerefMut can compile while violating a domain invariant
use std::ops::{
    Deref,DerefMut
};
struct NonEmpty(String);
impl Deref for NonEmpty{
    type Target=String;
    fn deref(&self)->&String{
        &self.0
    }
}
impl DerefMut for NonEmpty{
    fn deref_mut(&mut self)->&mut String{
        &mut self.0
    }
}
fn main(){
    let mut n=NonEmpty("x".into());
    n.clear();
    assert!(n.is_empty());
}

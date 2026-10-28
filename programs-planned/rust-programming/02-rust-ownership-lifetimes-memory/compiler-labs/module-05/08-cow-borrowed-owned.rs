// outcome: pass
// lesson: Cow can preserve a borrowed fast path
use std::borrow::Cow;
fn norm(s:&str)->Cow<'_,str>{
    if s.trim()==s{
        Cow::Borrowed(s)
    }
    else{
        Cow::Owned(s.trim().to_owned())
    }
}
fn main(){
    assert!(matches!(norm("x"),Cow::Borrowed(_)));
}

// outcome: pass
// lesson: A higher-ranked callback may return owned evidence
fn with<R>(s:&str,f:impl for<'a> FnOnce(&'a str)->R)->R{
    f(s)
}
fn main(){
    let n=with("abc",str::len);
    assert_eq!(n,3);
}

// outcome: pass
// lesson: Longer validity can be exposed under a shorter promise
fn short<'short,'long:'short>(x:&'long str)->&'short str{
    x
}
fn main(){
    let x=String::from("x");
    assert_eq!(short(&x),"x");
}

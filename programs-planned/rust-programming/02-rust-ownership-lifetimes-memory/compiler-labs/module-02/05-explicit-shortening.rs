// outcome: pass
// lesson: An outlives bound permits a weaker returned lifetime
fn shorten<'short,'long:'short>(v:&'long str)->&'short str{
    v
}
fn main(){
    let x=String::from("x");
    assert_eq!(shorten(&x),"x");
}

// outcome: pass
// lesson: A closure consuming capture is callable once
fn call<F:FnOnce()->String>(f:F)->String{
    f()
}
fn main(){
    let x=String::from("x");
    assert_eq!(call(move||x),"x");
}

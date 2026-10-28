// outcome: fail
// lesson: A universally supplied borrow cannot become fixed R
fn with<R>(s:&str,f:impl for<'a> FnOnce(&'a str)->R)->R{
    f(s)
}
fn main(){
    let escaped:&str=with("abc",|v|v);
    println!("{escaped}");
}

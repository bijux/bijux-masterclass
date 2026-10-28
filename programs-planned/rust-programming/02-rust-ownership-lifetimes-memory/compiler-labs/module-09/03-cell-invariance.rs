// outcome: fail
// lesson: Cell is invariant over its contained reference lifetime
use std::cell::Cell;
fn narrow<'a>(value:Cell<&'static str>,short:&'a str){
    let cell:Cell<&'a str>=value;
    cell.set(short);
}
fn main(){
}

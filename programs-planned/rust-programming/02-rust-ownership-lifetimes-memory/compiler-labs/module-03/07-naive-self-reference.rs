// outcome: fail
// lesson: An owner cannot safely store a reference into itself during construction
struct Bad<'a>{
    text:String,view:&'a str
}
fn make<'a>()->Bad<'a>{
    let text=String::from("x");
    let view=&text[..];
    Bad{
        text,view
    }
}
fn main(){
}

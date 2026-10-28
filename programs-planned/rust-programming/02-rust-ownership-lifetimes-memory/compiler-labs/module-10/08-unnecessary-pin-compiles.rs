// outcome: pass
// lesson: Pin can compile even when no address invariant justifies it
struct Document{
    title:String
}
fn main(){
    let mut d=Box::pin(Document{
        title:"x".into()
    });
    d.as_mut().title.push('!');
}

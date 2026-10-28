// outcome: fail
// lesson: A reference-bearing value cannot survive its owner
struct View<'a>{
    text:&'a str
}
fn main(){
    let view;
    {
        let text=String::from("x");
        view=View{
            text:&text
        };
    }
    println!("{}",view.text);
}

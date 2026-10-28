// outcome: pass
// lesson: Copy durable evidence before mutation
fn main(){
    let mut v=vec![String::from("a")];
    let length=v[0].len();
    v.push(String::from("b"));
    println!("{length}");
}

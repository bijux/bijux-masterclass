// outcome: fail
// lesson: A shared loan conflicts when it is used after mutation
fn main(){
    let mut v=vec![String::from("a")];
    let first=&v[0];
    v.push(String::from("b"));
    println!("{first}");
}

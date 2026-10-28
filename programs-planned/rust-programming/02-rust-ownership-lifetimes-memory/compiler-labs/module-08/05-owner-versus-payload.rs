// outcome: pass
// lesson: String owner size differs from logical payload length
fn main(){
    let s=String::from("abc");
    println!("{} {} {}",std::mem::size_of::<String>(),s.len(),s.capacity());
}

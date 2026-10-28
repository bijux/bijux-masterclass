// outcome: pass
// lesson: An owned String satisfies arbitrary outlives bounds
fn hold<'a,T:'a>(v:T,_:&'a())->T{
    v
}
fn main(){
    let witness=();
    let v=hold(String::from("x"),&witness);
    drop(v);
}

// outcome: pass
// lesson: ZSTs carry logical values without payload bytes
struct Marker;
fn main(){
    assert_eq!(std::mem::size_of::<Marker>(),0);
    let v=vec![Marker,Marker];
    assert_eq!(v.len(),2);
}

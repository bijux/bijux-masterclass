// outcome: pass
// lesson: Named fields can be borrowed independently
struct Pair {
    left: String, right: String
}
fn main() {
    let mut p=Pair{
        left:"a".into(),right:"b".into()
    };
    let l=&mut p.left;
    let r=&p.right;
    l.push('!');
    println!("{l} {r}");
}

// outcome: pass
// lesson: Owned ranges can outlive temporary line views
use std::ops::Range;
fn ranges(s:&str)->Vec<Range<usize>>{
    let mut out=Vec::new();
    let mut n=0;
    for line in s.lines(){
        out.push(n..n+line.len());
        n+=line.len()+1;
    }
    out
}
fn main(){
    let text=String::from("a\nb");
    let r=ranges(&text);
    assert_eq!(&text[r[1].clone()],"b");
}

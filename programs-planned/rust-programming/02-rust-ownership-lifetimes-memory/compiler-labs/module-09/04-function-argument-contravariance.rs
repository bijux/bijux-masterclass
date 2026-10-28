// outcome: pass
// lesson: A general accepter can satisfy a static-only call site

fn any(_: &str){}fn call(f:fn(&'static str)){f("x");}fn main(){call(any);}

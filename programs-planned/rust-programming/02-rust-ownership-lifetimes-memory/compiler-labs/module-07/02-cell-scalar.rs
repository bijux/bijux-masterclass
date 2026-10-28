// outcome: pass
// lesson: Cell safely replaces copyable scalar state
use std::cell::Cell;
struct C{
    n:Cell<u64>
}
impl C{
    fn inc(&self){
        self.n.set(self.n.get()+1);
    }
}
fn main(){
    let c=C{
        n:Cell::new(0)
    };
    c.inc();
    assert_eq!(c.n.get(),1);
}

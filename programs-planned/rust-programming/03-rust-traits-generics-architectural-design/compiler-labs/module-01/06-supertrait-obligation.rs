trait Id{fn id(&self)->u8;} trait Audit:Id{fn audit(&self)->u8{self.id()}}
struct X;impl Audit for X{}
fn main(){}

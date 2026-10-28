trait Lend{type Row<'a> where Self:'a;fn next(&mut self)->Self::Row<'_>;}struct S(String);
impl Lend for S{type Row<'a>=&'a str where Self:'a;fn next(&mut self)->&str{&self.0}}
fn main(){let mut s=S("x".into());let a=s.next();let b=s.next();println!("{a}{b}");}

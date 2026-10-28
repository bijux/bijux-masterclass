trait R{fn x(&self)->&str;}struct B<'a>(&'a str);impl R for B<'_>{fn x(&self)->&str{self.0}}fn store<T:R+'static>(_:T){}fn main(){let s=String::from("x");store(B(&s));}

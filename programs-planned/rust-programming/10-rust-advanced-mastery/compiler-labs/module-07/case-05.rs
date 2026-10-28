enum S{Add(u8),Mul(u8)}impl S{fn f(&self,x:u8)->u8{match self{Self::Add(n)=>x+n,Self::Mul(n)=>x*n}}}fn main(){assert_eq!(S::Add(3).f(2),5);assert_eq!(S::Mul(3).f(2),6);}

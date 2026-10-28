trait V{fn ok(&self)->bool;}struct S;impl V for S{fn ok(&self)->bool{true}}fn check(v:&dyn V)->bool{v.ok()}fn main(){assert!(check(&S));}

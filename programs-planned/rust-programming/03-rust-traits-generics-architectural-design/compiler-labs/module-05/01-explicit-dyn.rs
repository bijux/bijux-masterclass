trait Name{fn name(&self)->&str;}struct X;impl Name for X{fn name(&self)->&str{"x"}}fn show(x:&dyn Name)->&str{x.name()}fn main(){assert_eq!(show(&X),"x");}

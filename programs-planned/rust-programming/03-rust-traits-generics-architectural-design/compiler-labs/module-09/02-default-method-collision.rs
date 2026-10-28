trait A{fn name(&self)->&str{"a"}}trait B{fn name(&self)->&str{"b"}}struct X;impl A for X{}impl B for X{}fn main(){let _=X.name();}

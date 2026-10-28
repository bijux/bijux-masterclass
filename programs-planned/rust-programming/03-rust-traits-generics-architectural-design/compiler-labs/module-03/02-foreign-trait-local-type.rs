struct Local(u8);impl std::fmt::Display for Local{fn fmt(&self,f:&mut std::fmt::Formatter<'_>)->std::fmt::Result{write!(f,"{}",self.0)}}fn main(){assert_eq!(Local(2).to_string(),"2");}

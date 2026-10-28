use std::fmt::Display;trait Ext:Display{fn bracket(&self)->String{format!("[{self}]")}}impl<T:Display+?Sized>Ext for T{}fn main(){let s:&str="x";assert_eq!(s.bracket(),"[x]");}

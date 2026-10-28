mod x{pub trait Ext{fn x(&self)->u8;}impl Ext for u8{fn x(&self)->u8{*self}}}fn main(){let _=1u8.x();}

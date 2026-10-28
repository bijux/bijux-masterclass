trait A{fn id(&self)->u8;} trait B{fn id(&self)->u8;} struct X;
impl A for X{fn id(&self)->u8{1}} impl B for X{fn id(&self)->u8{2}}
fn main(){let x=X;let _=x.id();}

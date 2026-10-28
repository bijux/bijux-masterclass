trait Named{fn name(&self)->&str;fn boxed(self)->Box<Self> where Self:Sized{Box::new(self)}}
struct X;impl Named for X{fn name(&self)->&str{"x"}}
fn main(){let x:&dyn Named=&X;assert_eq!(x.name(),"x");let _=X.boxed();}

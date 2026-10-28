struct V1{p:String}struct V2{p:String,check:bool}impl From<V1> for V2{fn from(v:V1)->Self{Self{p:v.p,check:true}}}fn main(){let v=V2::from(V1{p:"x".into()});assert!(v.check&&!v.p.is_empty());}

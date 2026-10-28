#![forbid(unsafe_code)]
//! Reference design for the evolvable-sdk laboratory.

pub trait PluginV1 { fn run(&self, input: &str) -> String; }

pub trait PluginV1Ext: PluginV1 {
    fn run_trimmed(&self,input:&str)->String{self.run(input.trim())}
}
impl<T:PluginV1+?Sized> PluginV1Ext for T{}

#[derive(Clone,Debug,PartialEq,Eq)]
pub struct PluginError(pub String);
pub trait PluginV2 {
    fn id(&self)->&str;
    fn run_checked(&self,input:&str)->Result<String,PluginError>;
}

pub struct V1Adapter<T>{id:String,inner:T}
impl<T:PluginV1> V1Adapter<T>{pub fn new(id:impl Into<String>,inner:T)->Self{Self{id:id.into(),inner}}}
impl<T:PluginV1> PluginV2 for V1Adapter<T>{
 fn id(&self)->&str{&self.id}
 fn run_checked(&self,input:&str)->Result<String,PluginError>{Ok(self.inner.run(input))}
}

mod private{pub trait Sealed{}}
pub trait BuiltIn:private::Sealed+PluginV2{}
pub struct Upper;
impl PluginV1 for Upper{fn run(&self,input:&str)->String{input.to_uppercase()}}
impl PluginV2 for Upper{fn id(&self)->&str{"upper"}fn run_checked(&self,input:&str)->Result<String,PluginError>{if input.is_empty(){Err(PluginError("empty".into()))}else{Ok(input.to_uppercase())}}}
impl private::Sealed for Upper{}
impl BuiltIn for Upper{}

#[cfg(test)]mod tests{use super::*;
 #[test]fn extension_adds_nonrequired_convenience(){assert_eq!(Upper.run_trimmed(" a "),"A");}
 #[test]fn adapter_preserves_v1_behavior(){let a=V1Adapter::new("legacy",Upper);assert_eq!(a.run_checked("a"),Ok("A".into()));}
 #[test]fn v2_can_require_new_semantics(){assert_eq!(PluginV2::run_checked(&Upper,""),Err(PluginError("empty".into())));}
}

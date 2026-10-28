#![forbid(unsafe_code)]
//! Reference design for the inspection-platform transfer laboratory.

#[derive(Clone,Debug,PartialEq,Eq)]
pub struct Sample{pub id:u64,pub reading:i32}
#[derive(Clone,Copy,Debug,PartialEq,Eq,PartialOrd,Ord)]
pub enum Level{Info,Warning,Error}
#[derive(Clone,Debug,PartialEq,Eq)]
pub struct Notice{pub check:String,pub sample:u64,pub level:Level,pub message:String}

pub trait SampleSource{type Error;fn load(self)->Result<Vec<Sample>,Self::Error>;}
pub struct Memory(pub Vec<Sample>);
impl SampleSource for Memory{type Error=std::convert::Infallible;fn load(self)->Result<Vec<Sample>,Self::Error>{Ok(self.0)}}

pub trait Check{fn id(&self)->&str;fn inspect(&self,s:&Sample,out:&mut Vec<Notice>);}
pub struct Minimum{pub id:String,pub value:i32}
impl Check for Minimum{fn id(&self)->&str{&self.id}fn inspect(&self,s:&Sample,out:&mut Vec<Notice>){if s.reading<self.value{out.push(Notice{check:self.id.clone(),sample:s.id,level:Level::Error,message:format!("below {}",self.value)})}}}
pub struct CheckFn<F>{id:String,f:F}
impl<F> CheckFn<F>{pub fn new(id:impl Into<String>,f:F)->Self{Self{id:id.into(),f}}}
impl<F:Fn(&Sample,&mut Vec<Notice>)> Check for CheckFn<F>{fn id(&self)->&str{&self.id}fn inspect(&self,s:&Sample,out:&mut Vec<Notice>){(self.f)(s,out)}}

pub struct Missing;pub struct Ready<T>(T);
pub struct Plan<S>{source:S,checks:Vec<Box<dyn Check>>}
impl Plan<Missing>{pub fn new()->Self{Self{source:Missing,checks:Vec::new()}}pub fn source<S:SampleSource>(self,source:S)->Plan<Ready<S>>{Plan{source:Ready(source),checks:self.checks}}}
impl<S> Plan<S>{pub fn check<C:Check+'static>(mut self,check:C)->Self{self.checks.push(Box::new(check));self}}
impl<S:SampleSource> Plan<Ready<S>>{pub fn run(self)->Result<Vec<Notice>,S::Error>{let mut out=Vec::new();for sample in self.source.0.load()?{for check in &self.checks{check.inspect(&sample,&mut out);}}Ok(out)}}

#[cfg(test)]mod tests{use super::*;
 #[test]fn combines_static_source_dynamic_checks_and_closed_level(){let notices=Plan::new().source(Memory(vec![Sample{id:1,reading:-1}])).check(Minimum{id:"min".into(),value:0}).check(CheckFn::new("warn",|s:&Sample,o:&mut Vec<Notice>|if s.reading==0{o.push(Notice{check:"warn".into(),sample:s.id,level:Level::Warning,message:"zero".into()})})).run().expect("infallible");assert_eq!(notices.len(),1);assert_eq!(notices[0].level,Level::Error);}
}

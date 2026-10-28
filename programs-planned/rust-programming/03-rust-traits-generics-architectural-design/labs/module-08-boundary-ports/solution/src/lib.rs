#![forbid(unsafe_code)]
//! Reference design for the boundary-ports laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Item { pub id: u64, pub value: i32 }
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum SourceError { Injected, InvalidLine(usize) }

pub trait Source {
    type Item;
    type Error;
    fn load(self) -> Result<Vec<Self::Item>, Self::Error>;
}

pub struct MemorySource { items: Vec<Item>, fail: bool }
impl MemorySource {
    pub fn new(items: Vec<Item>) -> Self { Self { items, fail: false } }
    pub fn failing(items: Vec<Item>) -> Self { Self { items, fail: true } }
}
impl Source for MemorySource {
    type Item = Item; type Error = SourceError;
    fn load(self) -> Result<Vec<Item>, SourceError> { if self.fail { Err(SourceError::Injected) } else { Ok(self.items) } }
}

pub struct TextSource<'a>(pub &'a str);
impl Source for TextSource<'_> {
    type Item = Item; type Error = SourceError;
    fn load(self) -> Result<Vec<Item>, SourceError> {
        self.0.lines().enumerate().map(|(index,line)| {
            let (id,value)=line.split_once(',').ok_or(SourceError::InvalidLine(index+1))?;
            Ok(Item { id:id.parse().map_err(|_|SourceError::InvalidLine(index+1))?, value:value.parse().map_err(|_|SourceError::InvalidLine(index+1))? })
        }).collect()
    }
}

pub struct PolicyFn<F>(pub F);
impl<F> PolicyFn<F> where F: Fn(&Item)->bool {
    pub fn accepts(&self,item:&Item)->bool{(self.0)(item)}
}

pub struct InspectionService<S,P>{source:S,policy:PolicyFn<P>}
impl<S,P> InspectionService<S,P>{pub fn new(source:S,policy:P)->Self{Self{source,policy:PolicyFn(policy)}}}
impl<S,P> InspectionService<S,P>
where S:Source<Item=Item,Error=SourceError>, P:Fn(&Item)->bool {
    pub fn inspect(self)->Result<Vec<Item>,SourceError>{Ok(self.source.load()?.into_iter().filter(|i|self.policy.accepts(i)).collect())}
}

#[cfg(test)]
mod tests{
 use super::*;
 fn source_contract<S:Source<Item=Item,Error=SourceError>>(source:S, expected:usize){assert_eq!(source.load().expect("load").len(),expected);}
 #[test] fn both_sources_follow_contract(){source_contract(MemorySource::new(vec![Item{id:1,value:2}]),1);source_contract(TextSource("1,2\n2,3"),2);}
 #[test] fn service_keeps_domain_values(){let out=InspectionService::new(TextSource("1,2\n2,-1"),|i:&Item|i.value>=0).inspect().expect("inspect");assert_eq!(out.len(),1);}
 #[test] fn fake_injects_failure(){assert_eq!(MemorySource::failing(Vec::new()).load(),Err(SourceError::Injected));}
}

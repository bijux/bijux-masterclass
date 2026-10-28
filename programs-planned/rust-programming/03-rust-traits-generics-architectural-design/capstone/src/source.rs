use std::{collections::BTreeSet, fs, path::{Path, PathBuf}};
use crate::{InputError, Submission, SubmissionId};

pub trait Source {
    type Item;
    type Error;
    fn load(self) -> Result<Vec<Self::Item>, Self::Error>;
}

pub struct MemorySource<T> { items: Vec<T> }
impl<T> MemorySource<T> { pub fn new(items: Vec<T>) -> Self { Self { items } } }
impl<T> Source for MemorySource<T> {
    type Item=T; type Error=std::convert::Infallible;
    fn load(self)->Result<Vec<T>,Self::Error>{Ok(self.items)}
}

pub struct TsvSource<'a> { text: &'a str }
impl<'a> TsvSource<'a> { pub const fn new(text:&'a str)->Self{Self{text}} }
impl Source for TsvSource<'_> {
    type Item=Submission; type Error=InputError;
    fn load(self)->Result<Vec<Submission>,InputError>{parse_submissions(self.text)}
}

pub struct FileSource { path: PathBuf }
impl FileSource { pub fn new(path: impl Into<PathBuf>)->Self{Self{path:path.into()}} pub fn path(&self)->&Path{&self.path} }
impl Source for FileSource {
    type Item=Submission; type Error=InputError;
    fn load(self)->Result<Vec<Submission>,InputError>{let text=fs::read_to_string(&self.path).map_err(|source|InputError::Io{path:self.path.clone(),source})?;parse_submissions(&text)}
}

pub fn parse_submissions(text:&str)->Result<Vec<Submission>,InputError>{
 let mut items=Vec::new();let mut seen=BTreeSet::new();
 for (index,raw) in text.lines().enumerate(){let line=index+1;if raw.trim().is_empty()||raw.trim_start().starts_with('#'){continue;}let parts:Vec<&str>=raw.splitn(5,'\t').collect();if parts.len()!=5{return Err(InputError::InvalidLine{line,message:"expected five tab-separated columns".into()});}let id=SubmissionId::new(parts[0]).map_err(|m|InputError::InvalidLine{line,message:m.into()})?;if !seen.insert(id.as_str().to_owned()){return Err(InputError::DuplicateId{line,id:id.to_string()});}let score=parts[2].parse::<u8>().map_err(|_|InputError::InvalidLine{line,message:"score must be an integer in 0..=255".into()})?;let tags=parts[3].split(',').map(str::to_owned).collect();let item=Submission::new(id,parts[1],score,tags,parts[4]).map_err(|m|InputError::InvalidLine{line,message:m.into()})?;items.push(item);}Ok(items)
}

#[cfg(test)] mod tests{
 use super::*;
 #[test]fn parses_and_normalizes(){let v=parse_submissions("S-1\tada\t90\tRust, cli \tTitle").expect("parse");assert!(v[0].has_tag("rust"));}
 #[test]fn rejects_duplicate(){assert!(matches!(parse_submissions("S-1\ta\t1\t\tt\nS-1\tb\t2\t\tu"),Err(InputError::DuplicateId{line:2,..})));}
}

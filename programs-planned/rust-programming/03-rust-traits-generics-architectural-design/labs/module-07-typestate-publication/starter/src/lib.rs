#![forbid(unsafe_code)]
//! Starter for the typestate-publication laboratory.

pub struct Draft;
pub struct Article<S> { title: String, body: String, state: S }
impl Article<Draft> {
    pub fn new(title: impl Into<String>, body: impl Into<String>) -> Self {
        Self { title: title.into(), body: body.into(), state: Draft }
    }
    pub fn title(&self) -> &str { &self.title }
}

#[cfg(test)] mod tests { use super::*; #[test] fn creates_draft(){ assert_eq!(Article::new("t","b").title(),"t"); } }

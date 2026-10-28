#![forbid(unsafe_code)]
//! Reference design for the typestate-publication laboratory.

mod state {
    pub trait Sealed {}
    #[derive(Debug)]
    pub struct Draft(pub(crate) ());
    #[derive(Debug)]
    pub struct Reviewed { pub(crate) reviewer: String }
    impl Sealed for Draft {}
    impl Sealed for Reviewed {}
}
pub trait ArticleState: state::Sealed {}
impl ArticleState for state::Draft {}
impl ArticleState for state::Reviewed {}
pub use state::{Draft, Reviewed};

#[derive(Debug)]
pub struct Article<S: ArticleState> { id: u64, title: String, body: String, state: S }
#[derive(Debug)]
pub struct ReviewFailure { pub draft: Article<Draft>, pub reason: &'static str }
pub struct PublishPermit { _private: () }
pub struct PublishedArticle { pub id: u64, pub title: String, pub body: String, pub reviewer: String }

impl PublishPermit { pub fn issue_for_tests() -> Self { Self { _private: () } } }

impl Article<Draft> {
    pub fn new(id: u64, title: impl Into<String>, body: impl Into<String>) -> Self {
        Self { id, title: title.into(), body: body.into(), state: Draft(()) }
    }
    pub fn edit_body(&mut self, body: impl Into<String>) { self.body = body.into(); }
    pub fn review(self, reviewer: impl Into<String>) -> Result<Article<Reviewed>, ReviewFailure> {
        if self.title.trim().is_empty() || self.body.trim().is_empty() {
            return Err(ReviewFailure { draft: self, reason: "title and body required" });
        }
        Ok(Article { id: self.id, title: self.title, body: self.body, state: Reviewed { reviewer: reviewer.into() } })
    }
}
impl Article<Reviewed> {
    pub fn publish(self, _permit: PublishPermit) -> PublishedArticle {
        PublishedArticle { id: self.id, title: self.title, body: self.body, reviewer: self.state.reviewer }
    }
}

pub enum StoredArticle { Draft(Article<Draft>), Reviewed(Article<Reviewed>) }

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn failure_returns_draft() {
        let result = Article::new(1, "", "body").review("Ada");
        let failure = match result { Err(f) => f, Ok(_) => panic!("expected failure") };
        assert_eq!(failure.draft.id, 1);
    }
    #[test] fn reviewed_article_can_publish_with_single_use_permit() {
        let reviewed = Article::new(1, "Title", "Body").review("Ada").expect("review");
        let published = reviewed.publish(PublishPermit::issue_for_tests());
        assert_eq!(published.reviewer, "Ada");
    }
}

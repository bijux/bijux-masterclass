use crate::{EvaluationContext, Policy, Reporter, Review, RunError, Source, Submission};

#[derive(Debug, Default)]
pub struct Missing;
#[derive(Debug)]
pub struct Present<T>(pub T);

pub struct EngineBuilder<S, R, P> { source:S, reporter:R, policy:P }
impl EngineBuilder<Missing,Missing,Missing>{pub fn new()->Self{Self{source:Missing,reporter:Missing,policy:Missing}}}
impl Default for EngineBuilder<Missing,Missing,Missing>{fn default()->Self{Self::new()}}
impl<S,R,P> EngineBuilder<S,R,P>{
 pub fn with_source<NS>(self,source:NS)->EngineBuilder<Present<NS>,R,P>{EngineBuilder{source:Present(source),reporter:self.reporter,policy:self.policy}}
 pub fn with_reporter<NR>(self,reporter:NR)->EngineBuilder<S,Present<NR>,P>{EngineBuilder{source:self.source,reporter:Present(reporter),policy:self.policy}}
 pub fn with_policy(self,policy:Policy)->EngineBuilder<S,R,Present<Policy>>{EngineBuilder{source:self.source,reporter:self.reporter,policy:Present(policy)}}
}
impl<S,R> EngineBuilder<Present<S>,Present<R>,Present<Policy>>{pub fn build(self)->Engine<S,R>{Engine{source:self.source.0,reporter:self.reporter.0,policy:self.policy.0}}}

pub struct Engine<S,R>{source:S,reporter:R,policy:Policy}
pub struct RunOutcome<O>{pub review:Review,pub output:O}
impl<O> RunOutcome<O>{pub fn accepted(&self)->bool{self.review.accepted()}}

impl<S,R> Engine<S,R>
where S:Source<Item=Submission>,R:Reporter{
 pub fn run(self)->Result<RunOutcome<R::Output>,RunError<S::Error,R::Error>>{
  let submissions=self.source.load().map_err(RunError::Source)?;
  let mut findings=Vec::new();
  for submission in &submissions{let context=EvaluationContext::new(submission);for rule in self.policy.rules(){rule.evaluate(&context,&mut findings);}}
  let review=Review::new(submissions.len(),findings);
  let output=self.reporter.report(&review).map_err(RunError::Report)?;
  Ok(RunOutcome{review,output})
 }
 pub fn rule_count(&self)->usize{self.policy.len()}
}

#[cfg(test)]mod tests{
 use super::*;use crate::{default_registry,MemorySource,SubmissionId,TextReporter};
 #[test]fn complete_builder_runs(){let s=Submission::new(SubmissionId::new("S-1").expect("id"),"ada",80,vec!["rust".into()],"Title").expect("submission");let p=default_registry().parse("min-score\t70").expect("policy");let result=EngineBuilder::new().with_source(MemorySource::new(vec![s])).with_reporter(TextReporter).with_policy(p).build().run().expect("run");assert!(result.accepted());}
}

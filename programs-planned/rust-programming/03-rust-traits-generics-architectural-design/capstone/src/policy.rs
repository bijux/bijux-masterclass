use std::collections::BTreeSet;
use crate::{EvaluationContext, Finding, PolicyError, Rule, RuleId, Severity};
use crate::rule::{BuiltInRule, BuiltInSealed};

pub struct Policy { rules: Vec<Box<dyn Rule>> }
impl Policy {
    pub fn new(rules: Vec<Box<dyn Rule>>) -> Result<Self, PolicyError> {
        let mut seen = BTreeSet::new();
        for rule in &rules {
            if !seen.insert(rule.id().as_str().to_owned()) { return Err(PolicyError::DuplicateRuleId(rule.id().to_string())); }
        }
        Ok(Self { rules })
    }
    pub fn rules(&self) -> impl Iterator<Item = &dyn Rule> { self.rules.iter().map(Box::as_ref) }
    pub fn len(&self) -> usize { self.rules.len() }
    pub fn is_empty(&self) -> bool { self.rules.is_empty() }
}

pub trait RuleFactory {
    fn name(&self) -> &'static str;
    fn explanation(&self) -> &'static str;
    fn build(&self, args: &[&str], line: usize) -> Result<Box<dyn Rule>, PolicyError>;
}

pub struct RuleRegistry { factories: Vec<Box<dyn RuleFactory>> }
impl RuleRegistry {
    pub fn new() -> Self { Self { factories: Vec::new() } }
    pub fn register<F: RuleFactory + 'static>(&mut self, factory: F) { self.factories.push(Box::new(factory)); }
    pub fn names(&self) -> impl Iterator<Item = &'static str> + '_ { self.factories.iter().map(|f| f.name()) }
    pub fn explain(&self, name: &str) -> Option<&'static str> { self.factories.iter().find(|f| f.name() == name).map(|f| f.explanation()) }
    pub fn parse(&self, text: &str) -> Result<Policy, PolicyError> {
        let mut rules = Vec::new();
        for (index, raw) in text.lines().enumerate() {
            let line = index + 1; let raw = raw.trim();
            if raw.is_empty() || raw.starts_with('#') { continue; }
            let parts: Vec<&str> = raw.split('\t').collect();
            let name = parts[0];
            let factory = self.factories.iter().find(|f| f.name() == name)
                .ok_or_else(|| PolicyError::UnknownRule { line, name: name.to_owned() })?;
            rules.push(factory.build(&parts[1..], line)?);
        }
        Policy::new(rules)
    }
}
impl Default for RuleRegistry { fn default() -> Self { default_registry() } }

fn arg_count(args: &[&str], expected: usize, line: usize, usage: &str) -> Result<(), PolicyError> {
    if args.len() == expected { Ok(()) } else { Err(PolicyError::InvalidLine { line, message: format!("expected {usage}") }) }
}
fn parse_u8(value: &str, line: usize, name: &str) -> Result<u8, PolicyError> {
    value.parse().map_err(|_| PolicyError::InvalidLine { line, message: format!("{name} must be an integer in 0..=255") })
}

struct MinimumScore { id: RuleId, minimum: u8 }
impl BuiltInSealed for MinimumScore {}
impl BuiltInRule for MinimumScore {}
impl Rule for MinimumScore {
    fn id(&self) -> &RuleId { &self.id }
    fn evaluate(&self, c: &EvaluationContext<'_>, out: &mut Vec<Finding>) {
        let s=c.submission(); if s.score()<self.minimum { out.push(Finding{submission:s.id().clone(),rule:self.id.clone(),severity:Severity::Error,message:format!("score {} is below required {}",s.score(),self.minimum)}); }
    }
}
struct MinimumScoreFactory;
impl RuleFactory for MinimumScoreFactory {
    fn name(&self)->&'static str{"min-score"}
    fn explanation(&self)->&'static str{"Reject submissions whose score is below the configured inclusive minimum."}
    fn build(&self,args:&[&str],line:usize)->Result<Box<dyn Rule>,PolicyError>{arg_count(args,1,line,"min-score<TAB>minimum")?;Ok(Box::new(MinimumScore{id:RuleId::new(format!("min-score-{}",args[0])).map_err(|m|PolicyError::InvalidLine{line,message:m.into()})?,minimum:parse_u8(args[0],line,"minimum")?}))}
}

struct RequiredTag { id: RuleId, tag: String }
impl BuiltInSealed for RequiredTag {} impl BuiltInRule for RequiredTag {}
impl Rule for RequiredTag {
 fn id(&self)->&RuleId{&self.id}
 fn evaluate(&self,c:&EvaluationContext<'_>,out:&mut Vec<Finding>){let s=c.submission();if !s.has_tag(&self.tag){out.push(Finding{submission:s.id().clone(),rule:self.id.clone(),severity:Severity::Error,message:format!("required tag {:?} is missing",self.tag)})}}
}
struct RequiredTagFactory;
impl RuleFactory for RequiredTagFactory {
 fn name(&self)->&'static str{"require-tag"}
 fn explanation(&self)->&'static str{"Reject submissions that do not contain the configured normalized tag."}
 fn build(&self,args:&[&str],line:usize)->Result<Box<dyn Rule>,PolicyError>{arg_count(args,1,line,"require-tag<TAB>tag")?;let tag=args[0].trim().to_ascii_lowercase();if tag.is_empty(){return Err(PolicyError::InvalidLine{line,message:"tag must not be empty".into()});}Ok(Box::new(RequiredTag{id:RuleId::new(format!("require-tag-{tag}")).map_err(|m|PolicyError::InvalidLine{line,message:m.into()})?,tag}))}
}

struct TitleLength { id: RuleId, minimum: usize, maximum: usize }
impl BuiltInSealed for TitleLength {} impl BuiltInRule for TitleLength {}
impl Rule for TitleLength {
 fn id(&self)->&RuleId{&self.id}
 fn evaluate(&self,c:&EvaluationContext<'_>,out:&mut Vec<Finding>){let s=c.submission();let n=s.title().chars().count();if n<self.minimum||n>self.maximum{out.push(Finding{submission:s.id().clone(),rule:self.id.clone(),severity:Severity::Warning,message:format!("title length {n} is outside {}..={}",self.minimum,self.maximum)})}}
}
struct TitleLengthFactory;
impl RuleFactory for TitleLengthFactory {
 fn name(&self)->&'static str{"title-length"}
 fn explanation(&self)->&'static str{"Warn when Unicode scalar-value title length falls outside the configured inclusive range."}
 fn build(&self,args:&[&str],line:usize)->Result<Box<dyn Rule>,PolicyError>{arg_count(args,2,line,"title-length<TAB>minimum<TAB>maximum")?;let min=args[0].parse::<usize>().map_err(|_|PolicyError::InvalidLine{line,message:"minimum must be a nonnegative integer".into()})?;let max=args[1].parse::<usize>().map_err(|_|PolicyError::InvalidLine{line,message:"maximum must be a nonnegative integer".into()})?;if min>max{return Err(PolicyError::InvalidLine{line,message:"minimum must not exceed maximum".into()});}Ok(Box::new(TitleLength{id:RuleId::new(format!("title-length-{min}-{max}")).map_err(|m|PolicyError::InvalidLine{line,message:m.into()})?,minimum:min,maximum:max}))}
}

struct DenyOwner { id: RuleId, owner: String }
impl BuiltInSealed for DenyOwner {} impl BuiltInRule for DenyOwner {}
impl Rule for DenyOwner {
 fn id(&self)->&RuleId{&self.id}
 fn evaluate(&self,c:&EvaluationContext<'_>,out:&mut Vec<Finding>){let s=c.submission();if s.owner()==self.owner{out.push(Finding{submission:s.id().clone(),rule:self.id.clone(),severity:Severity::Error,message:format!("owner {:?} is denied",self.owner)})}}
}
struct DenyOwnerFactory;
impl RuleFactory for DenyOwnerFactory {
 fn name(&self)->&'static str{"deny-owner"}
 fn explanation(&self)->&'static str{"Reject submissions owned by the configured exact owner name."}
 fn build(&self,args:&[&str],line:usize)->Result<Box<dyn Rule>,PolicyError>{arg_count(args,1,line,"deny-owner<TAB>owner")?;let owner=args[0].trim().to_owned();if owner.is_empty(){return Err(PolicyError::InvalidLine{line,message:"owner must not be empty".into()});}let normalized=owner.to_ascii_lowercase().replace(|c:char|!c.is_ascii_alphanumeric(),"-");Ok(Box::new(DenyOwner{id:RuleId::new(format!("deny-owner-{normalized}")).map_err(|m|PolicyError::InvalidLine{line,message:m.into()})?,owner}))}
}

pub fn default_registry() -> RuleRegistry {
    let mut registry=RuleRegistry::new();
    registry.register(MinimumScoreFactory);registry.register(RequiredTagFactory);registry.register(TitleLengthFactory);registry.register(DenyOwnerFactory);registry
}

#[cfg(test)] mod tests {
 use super::*;
 #[test] fn registry_is_deterministic(){assert_eq!(default_registry().names().collect::<Vec<_>>(),vec!["min-score","require-tag","title-length","deny-owner"]);}
 #[test] fn parser_rejects_duplicate_rule_ids(){let e=default_registry().parse("min-score\t70\nmin-score\t70").err().expect("error"); assert_eq!(e, PolicyError::DuplicateRuleId("min-score-70".into()));}
}

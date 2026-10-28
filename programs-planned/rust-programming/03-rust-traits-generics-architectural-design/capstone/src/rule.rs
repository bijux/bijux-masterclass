use crate::{Finding, RuleId, Submission};

pub struct EvaluationContext<'a> { submission: &'a Submission }
impl<'a> EvaluationContext<'a> {
    pub const fn new(submission: &'a Submission) -> Self { Self { submission } }
    pub const fn submission(&self) -> &'a Submission { self.submission }
}

pub trait Rule {
    fn id(&self) -> &RuleId;
    fn evaluate(&self, context: &EvaluationContext<'_>, findings: &mut Vec<Finding>);
}

pub trait RuleExt: Rule {
    fn findings(&self, submission: &Submission) -> Vec<Finding> {
        let mut findings = Vec::new();
        self.evaluate(&EvaluationContext::new(submission), &mut findings);
        findings
    }
}
impl<T: Rule + ?Sized> RuleExt for T {}

pub struct RuleFn<F> { id: RuleId, function: F }
impl<F> RuleFn<F> {
    pub fn new(id: RuleId, function: F) -> Self { Self { id, function } }
}
impl<F> Rule for RuleFn<F>
where F: for<'a> Fn(&EvaluationContext<'a>, &mut Vec<Finding>) {
    fn id(&self) -> &RuleId { &self.id }
    fn evaluate(&self, context: &EvaluationContext<'_>, findings: &mut Vec<Finding>) { (self.function)(context, findings); }
}

mod private { pub trait Sealed {} }
#[allow(private_bounds)]
pub trait BuiltInRule: Rule + private::Sealed {}

pub(crate) use private::Sealed as BuiltInSealed;

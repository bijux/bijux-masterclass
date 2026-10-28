use std::fmt;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SubmissionId(String);
impl SubmissionId {
    pub fn new(value: impl Into<String>) -> Result<Self, &'static str> {
        let value = value.into();
        let valid = !value.is_empty()
            && value.len() <= 64
            && value.bytes().all(|b| b.is_ascii_alphanumeric() || matches!(b, b'-' | b'_'));
        valid.then_some(Self(value)).ok_or("submission ID must use 1-64 ASCII letters, digits, '-' or '_'")
    }
    pub fn as_str(&self) -> &str { &self.0 }
}
impl fmt::Display for SubmissionId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { f.write_str(&self.0) }
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct RuleId(String);
impl RuleId {
    pub fn new(value: impl Into<String>) -> Result<Self, &'static str> {
        let value = value.into();
        let valid = !value.is_empty()
            && value.len() <= 64
            && value.bytes().all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-');
        valid.then_some(Self(value)).ok_or("rule ID must use 1-64 lowercase ASCII letters, digits, or '-'")
    }
    pub fn as_str(&self) -> &str { &self.0 }
}
impl fmt::Display for RuleId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { f.write_str(&self.0) }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum Severity { Info, Warning, Error }
impl fmt::Display for Severity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self { Self::Info => "info", Self::Warning => "warning", Self::Error => "error" })
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Submission {
    id: SubmissionId,
    owner: String,
    score: u8,
    tags: Vec<String>,
    title: String,
}
impl Submission {
    pub fn new(id: SubmissionId, owner: impl Into<String>, score: u8, tags: Vec<String>, title: impl Into<String>) -> Result<Self, &'static str> {
        let owner = owner.into();
        let title = title.into();
        if owner.trim().is_empty() { return Err("owner must not be empty"); }
        if title.chars().any(|c| matches!(c, '\t' | '\n' | '\r')) { return Err("title must not contain tabs or line breaks"); }
        let mut tags: Vec<String> = tags.into_iter().map(|t| t.trim().to_ascii_lowercase()).filter(|t| !t.is_empty()).collect();
        tags.sort(); tags.dedup();
        Ok(Self { id, owner, score, tags, title })
    }
    pub fn id(&self) -> &SubmissionId { &self.id }
    pub fn owner(&self) -> &str { &self.owner }
    pub const fn score(&self) -> u8 { self.score }
    pub fn tags(&self) -> &[String] { &self.tags }
    pub fn title(&self) -> &str { &self.title }
    pub fn has_tag(&self, tag: &str) -> bool { self.tags.binary_search_by(|t| t.as_str().cmp(tag)).is_ok() }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Finding {
    pub submission: SubmissionId,
    pub rule: RuleId,
    pub severity: Severity,
    pub message: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Review {
    submissions: usize,
    findings: Vec<Finding>,
}
impl Review {
    pub fn new(submissions: usize, findings: Vec<Finding>) -> Self { Self { submissions, findings } }
    pub const fn submission_count(&self) -> usize { self.submissions }
    pub fn findings(&self) -> &[Finding] { &self.findings }
    pub fn accepted(&self) -> bool { !self.findings.iter().any(|f| f.severity == Severity::Error) }
    pub fn error_count(&self) -> usize { self.findings.iter().filter(|f| f.severity == Severity::Error).count() }
    pub fn warning_count(&self) -> usize { self.findings.iter().filter(|f| f.severity == Severity::Warning).count() }
}

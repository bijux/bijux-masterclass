use std::{error::Error, fmt, io, path::PathBuf};

#[derive(Debug)]
pub enum InputError {
    Io { path: PathBuf, source: io::Error },
    InvalidLine { line: usize, message: String },
    DuplicateId { line: usize, id: String },
}
impl fmt::Display for InputError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io { path, source } => write!(f, "cannot read {}: {source}", path.display()),
            Self::InvalidLine { line, message } => write!(f, "invalid submission line {line}: {message}"),
            Self::DuplicateId { line, id } => write!(f, "duplicate submission ID {id:?} at line {line}"),
        }
    }
}
impl Error for InputError { fn source(&self) -> Option<&(dyn Error + 'static)> { match self { Self::Io{source,..} => Some(source), _ => None } } }

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum PolicyError {
    InvalidLine { line: usize, message: String },
    UnknownRule { line: usize, name: String },
    DuplicateRuleId(String),
}
impl fmt::Display for PolicyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidLine { line, message } => write!(f, "invalid policy line {line}: {message}"),
            Self::UnknownRule { line, name } => write!(f, "unknown rule {name:?} at policy line {line}"),
            Self::DuplicateRuleId(id) => write!(f, "duplicate rule ID {id:?}"),
        }
    }
}
impl Error for PolicyError {}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ReportError(pub String);
impl fmt::Display for ReportError { fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { f.write_str(&self.0) } }
impl Error for ReportError {}

#[derive(Debug)]
pub enum RunError<S, R> { Source(S), Report(R) }
impl<S: fmt::Display, R: fmt::Display> fmt::Display for RunError<S, R> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self { Self::Source(e) => write!(f, "source failure: {e}"), Self::Report(e) => write!(f, "report failure: {e}") }
    }
}
impl<S: Error + 'static, R: Error + 'static> Error for RunError<S, R> {
    fn source(&self) -> Option<&(dyn Error + 'static)> { match self { Self::Source(e) => Some(e), Self::Report(e) => Some(e) } }
}

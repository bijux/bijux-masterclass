//! Domain baseline for the trait-and-lifetime laboratory.
//!
//! Standard trait implementations, generic I/O, typed boundary errors, and
//! reference-returning selection functions remain the learner's work.

/// Report severity in ascending order.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Severity {
    /// Informational report.
    Info,
    /// Warning requiring attention.
    Warning,
    /// Critical report requiring immediate action.
    Critical,
}

/// One validated owned report.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Report {
    name: String,
    severity: Severity,
    message: String,
}

impl Report {
    /// Constructs a report when required fields are nonblank and record-safe.
    pub fn new(
        name: String,
        severity: Severity,
        message: String,
    ) -> Result<Self, &'static str> {
        if name.trim().is_empty() {
            return Err("name cannot be empty");
        }
        if message.trim().is_empty() {
            return Err("message cannot be empty");
        }
        if [name.as_str(), message.as_str()]
            .into_iter()
            .any(has_record_delimiter)
        {
            return Err("fields cannot contain tab or line breaks");
        }
        Ok(Self {
            name,
            severity,
            message,
        })
    }

    /// Borrows the report name.
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Returns severity.
    pub const fn severity(&self) -> Severity {
        self.severity
    }

    /// Borrows the message.
    pub fn message(&self) -> &str {
        &self.message
    }
}

fn has_record_delimiter(value: &str) -> bool {
    value
        .chars()
        .any(|character| matches!(character, '\t' | '\n' | '\r'))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_constructor_preserves_domain_invariant() {
        let report = Report::new(
            String::from("parser"),
            Severity::Warning,
            String::from("line skipped"),
        )
        .expect("valid report");
        assert_eq!(report.name(), "parser");
        assert_eq!(report.severity(), Severity::Warning);
        assert_eq!(report.message(), "line skipped");
        assert!(Report::new(String::new(), Severity::Info, String::from("x")).is_err());
    }
}

//! Reference report codec using standard traits and precise lifetime relationships.

use std::error::Error;
use std::fmt;
use std::io::{self, BufRead, Write};
use std::str::FromStr;

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

impl fmt::Display for Severity {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Info => "info",
            Self::Warning => "warning",
            Self::Critical => "critical",
        })
    }
}

/// Failure to parse a severity label.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseSeverityError {
    input: String,
}

impl fmt::Display for ParseSeverityError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "unknown severity `{}`", self.input)
    }
}

impl Error for ParseSeverityError {}

impl FromStr for Severity {
    type Err = ParseSeverityError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input {
            "info" => Ok(Self::Info),
            "warning" => Ok(Self::Warning),
            "critical" => Ok(Self::Critical),
            other => Err(ParseSeverityError { input: other.to_owned() }),
        }
    }
}

/// One owned report.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Report {
    name: String,
    severity: Severity,
    message: String,
}

impl Report {
    /// Creates a report, rejecting blank names or messages.
    pub fn new(name: String, severity: Severity, message: String) -> Result<Self, &'static str> {
        if name.trim().is_empty() {
            return Err("name cannot be empty");
        }
        if message.trim().is_empty() {
            return Err("message cannot be empty");
        }
        if has_record_delimiter(&name) || has_record_delimiter(&message) {
            return Err("fields cannot contain tab or line breaks");
        }
        Ok(Self { name, severity, message })
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

/// Failure at the report text or I/O boundary.
#[derive(Debug)]
pub enum ReportError {
    /// Reader or writer failed.
    Io(io::Error),
    /// One record was malformed.
    InvalidRecord {
        /// One-based line number.
        line: usize,
        /// Stable explanation.
        message: String,
    },
}

impl fmt::Display for ReportError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(formatter, "report I/O failed: {error}"),
            Self::InvalidRecord { line, message } => {
                write!(formatter, "invalid report at line {line}: {message}")
            }
        }
    }
}

impl Error for ReportError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::InvalidRecord { .. } => None,
        }
    }
}

impl From<io::Error> for ReportError {
    fn from(error: io::Error) -> Self {
        Self::Io(error)
    }
}

/// Parses reports from a buffered text source.
pub fn load_reports<R: BufRead>(reader: R) -> Result<Vec<Report>, ReportError> {
    let mut reports = Vec::new();
    for (index, line) in reader.lines().enumerate() {
        let line_number = index + 1;
        let line = line?;
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 3 {
            return Err(ReportError::InvalidRecord {
                line: line_number,
                message: String::from("expected SEVERITY<TAB>NAME<TAB>MESSAGE"),
            });
        }
        let severity = fields[0].parse::<Severity>().map_err(|error| ReportError::InvalidRecord {
            line: line_number,
            message: error.to_string(),
        })?;
        let report = Report::new(fields[1].to_owned(), severity, fields[2].to_owned())
            .map_err(|message| ReportError::InvalidRecord {
            line: line_number,
            message: message.to_owned(),
        })?;
        reports.push(report);
    }
    Ok(reports)
}

/// Writes reports in deterministic name/severity/message order.
pub fn write_reports<W: Write>(writer: &mut W, reports: &[Report]) -> Result<(), ReportError> {
    let mut ordered: Vec<_> = reports.iter().collect();
    ordered.sort_unstable_by(|left, right| {
        left.name.cmp(&right.name)
            .then_with(|| left.severity.cmp(&right.severity))
            .then_with(|| left.message.cmp(&right.message))
    });
    for report in ordered {
        writeln!(writer, "{}\t{}\t{}", report.severity, report.name, report.message)?;
    }
    Ok(())
}

/// Borrows the more severe input; ties select `left`.
pub fn most_severe<'a>(left: &'a Report, right: &'a Report) -> &'a Report {
    if left.severity >= right.severity {
        left
    } else {
        right
    }
}

/// Borrows reports whose names begin with `prefix`.
pub fn find_by_prefix<'a>(reports: &'a [Report], prefix: &str) -> Vec<&'a Report> {
    reports.iter().filter(|report| report.name.starts_with(prefix)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::{Cursor, Read};

    fn report(name: &str, severity: Severity, message: &str) -> Report {
        Report::new(name.to_owned(), severity, message.to_owned()).expect("valid fixture")
    }

    #[test]
    fn display_and_from_str_are_inverse_for_supported_values() {
        for severity in [Severity::Info, Severity::Warning, Severity::Critical] {
            assert_eq!(severity.to_string().parse::<Severity>(), Ok(severity));
        }
        assert!("fatal".parse::<Severity>().is_err());
    }

    #[test]
    fn loader_adds_line_context() {
        let input = Cursor::new("info\tparser\tok\nfatal\tstorage\tbad\n");
        let error = load_reports(input).expect_err("second severity is invalid");
        assert!(matches!(
            error,
            ReportError::InvalidRecord { line: 2, message } if message.contains("fatal")
        ));
    }

    #[test]
    fn writer_is_deterministic() {
        let reports = vec![
            report("storage", Severity::Critical, "checksum"),
            report("parser", Severity::Warning, "recovered"),
            report("parser", Severity::Info, "started"),
        ];
        let mut output = Vec::new();
        write_reports(&mut output, &reports).expect("memory write");
        assert_eq!(
            String::from_utf8(output).expect("UTF-8"),
            concat!(
                "info\tparser\tstarted\n",
                "warning\tparser\trecovered\n",
                "critical\tstorage\tchecksum\n",
            )
        );
    }

    #[test]
    fn lifetime_relations_are_minimal() {
        let reports = vec![
            report("parser", Severity::Warning, "recovered"),
            report("storage", Severity::Critical, "checksum"),
        ];
        assert!(std::ptr::eq(most_severe(&reports[0], &reports[1]), &reports[1]));
        let matches = {
            let prefix = String::from("par");
            find_by_prefix(&reports, &prefix)
        };
        assert_eq!(matches, vec![&reports[0]]);
    }

    struct ErrorReader;

    impl Read for ErrorReader {
        fn read(&mut self, _buffer: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::other("synthetic"))
        }
    }

    impl BufRead for ErrorReader {
        fn fill_buf(&mut self) -> io::Result<&[u8]> {
            Err(io::Error::other("synthetic"))
        }

        fn consume(&mut self, _amount: usize) {}
    }

    #[test]
    fn io_error_conversion_preserves_source() {
        let error = load_reports(ErrorReader).expect_err("reader fails");
        assert!(matches!(error, ReportError::Io(_)));
        assert!(error.source().is_some());
    }
}

use crate::{ReportError, Review};

pub trait Reporter {
    type Output;
    type Error;
    fn report(&self, review: &Review) -> Result<Self::Output, Self::Error>;
}

#[derive(Clone, Copy, Debug, Default)]
pub struct TextReporter;
impl Reporter for TextReporter {
    type Output=String;type Error=ReportError;
    fn report(&self,review:&Review)->Result<String,ReportError>{
        let mut out=format!("submissions: {}\nfindings: {}\nerrors: {}\nwarnings: {}\naccepted: {}\n",review.submission_count(),review.findings().len(),review.error_count(),review.warning_count(),review.accepted());
        for f in review.findings(){out.push_str(&format!("{} [{}] {}: {}\n",f.submission,f.severity,f.rule,f.message));}
        Ok(out)
    }
}

#[derive(Clone, Copy, Debug, Default)]
pub struct TsvReporter;
impl Reporter for TsvReporter {
    type Output=String;type Error=ReportError;
    fn report(&self,review:&Review)->Result<String,ReportError>{
        let mut lines=vec!["submission\tseverity\trule\tmessage".to_owned()];
        for f in review.findings(){if f.message.chars().any(|c| matches!(c, '\t' | '\n' | '\r')){return Err(ReportError("finding message is not TSV-safe".into()));}lines.push(format!("{}\t{}\t{}\t{}",f.submission,f.severity,f.rule,f.message));}
        Ok(lines.join("\n")+"\n")
    }
}

#[cfg(test)]mod tests{use super::*;use crate::Review;#[test]fn empty_report_is_deterministic(){let r=Review::new(0,Vec::new());assert_eq!(TextReporter.report(&r).expect("report"),"submissions: 0\nfindings: 0\nerrors: 0\nwarnings: 0\naccepted: true\n");}}

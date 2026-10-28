#![forbid(unsafe_code)]
//! Reference design for the composed-renderer laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Report { pub title: String, pub lines: Vec<String> }
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RenderError(pub &'static str);

pub trait Formatter { fn render(&self, report: &Report) -> Result<String, RenderError>; }

pub struct Plain;
impl Formatter for Plain {
    fn render(&self, report: &Report) -> Result<String, RenderError> {
        if report.title.contains('\n') { return Err(RenderError("newline in title")); }
        Ok(format!("{}\n{}", report.title, report.lines.join("\n")))
    }
}

pub struct Tsv;
impl Formatter for Tsv {
    fn render(&self, report: &Report) -> Result<String, RenderError> {
        if report.title.chars().any(|c| matches!(c, '\t' | '\n')) { return Err(RenderError("invalid title")); }
        Ok(report.lines.iter().map(|line| format!("{}\t{}", report.title, line)).collect::<Vec<_>>().join("\n"))
    }
}

pub struct Signed<F> { pub inner: F, pub signer: String }
impl<F: Formatter> Formatter for Signed<F> {
    fn render(&self, report: &Report) -> Result<String, RenderError> {
        Ok(format!("{}\n-- {}", self.inner.render(report)?, self.signer))
    }
}

pub struct Numbered<F>(pub F);
impl<F: Formatter> Formatter for Numbered<F> {
    fn render(&self, report: &Report) -> Result<String, RenderError> {
        self.0.render(report).map(|text| text.lines().enumerate().map(|(i,l)| format!("{}: {l}", i+1)).collect::<Vec<_>>().join("\n"))
    }
}

pub enum FormatKind { Plain, Tsv }
impl Formatter for FormatKind {
    fn render(&self, report: &Report) -> Result<String, RenderError> {
        match self { Self::Plain => Plain.render(report), Self::Tsv => Tsv.render(report) }
    }
}

pub fn runtime_formatter(tsv: bool) -> Box<dyn Formatter> {
    if tsv { Box::new(Tsv) } else { Box::new(Plain) }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn sample() -> Report { Report { title: "R".into(), lines: vec!["a".into(), "b".into()] } }
    #[test] fn wrappers_compose_statically() {
        let f = Signed { inner: Numbered(Plain), signer: "Ada".into() };
        let out = f.render(&sample()).expect("render");
        assert!(out.contains("1: R")); assert!(out.ends_with("-- Ada"));
    }
    #[test] fn runtime_selection_erases_concrete_type() {
        assert!(runtime_formatter(true).render(&sample()).expect("render").contains('\t'));
    }
}

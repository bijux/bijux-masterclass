#![forbid(unsafe_code)]
//! Reference design for the associated-families laboratory.

pub trait RowAccess {
    fn len(&self) -> usize;
    fn field(&self, index: usize) -> Option<&str>;
    fn is_empty(&self) -> bool { self.len() == 0 }
}

pub trait LendingRows {
    type Row<'a>: RowAccess + 'a where Self: 'a;
    fn next_row(&mut self) -> Option<Self::Row<'_>>;
}

#[derive(Debug)]
pub struct RowView<'a> { line: &'a str }
impl RowAccess for RowView<'_> {
    fn len(&self) -> usize { self.line.split('\t').count() }
    fn field(&self, index: usize) -> Option<&str> { self.line.split('\t').nth(index) }
}

pub struct TsvRows { rows: Vec<String>, next: usize }
impl TsvRows {
    pub fn new(input: &str) -> Self {
        Self { rows: input.lines().map(str::to_owned).collect(), next: 0 }
    }
}
impl LendingRows for TsvRows {
    type Row<'a> = RowView<'a> where Self: 'a;
    fn next_row(&mut self) -> Option<Self::Row<'_>> {
        let index = self.next;
        let line = self.rows.get(index)?;
        self.next += 1;
        Some(RowView { line })
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct OwnedRow(pub Vec<String>);

pub struct OwnedRows<S> { source: S }
impl<S> OwnedRows<S> {
    pub fn new(source: S) -> Self { Self { source } }
}
impl<S: LendingRows> OwnedRows<S> {
    pub fn next_owned(&mut self) -> Option<OwnedRow> {
        let row = self.source.next_row()?;
        let fields = (0..row.len())
            .filter_map(|index| row.field(index).map(str::to_owned))
            .collect();
        Some(OwnedRow(fields))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn borrowed_view_reads_fields() {
        let mut source = TsvRows::new("a\tb\nc\td");
        let row = source.next_row().expect("row");
        assert_eq!(row.field(1), Some("b"));
    }
    #[test] fn owned_adapter_allows_collection() {
        let mut rows = OwnedRows::new(TsvRows::new("a\tb\nc\td"));
        let first = rows.next_owned().expect("first");
        let second = rows.next_owned().expect("second");
        assert_eq!(first.0, vec!["a", "b"]);
        assert_eq!(second.0, vec!["c", "d"]);
    }
}

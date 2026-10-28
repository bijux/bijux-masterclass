#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct RowView<'a> {
    raw: &'a str,
}

impl<'a> RowView<'a> {
    pub fn raw(self) -> &'a str {
        self.raw
    }

    pub fn fields(self) -> impl Iterator<Item = &'a str> {
        self.raw.split('\t')
    }

    pub fn to_owned(self) -> Vec<String> {
        self.fields().map(str::to_owned).collect()
    }
}

pub trait LendingCursor {
    type View<'a>
    where
        Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::View<'a>>;
}

pub struct TableCursor<'input> {
    remaining: &'input str,
}

impl<'input> TableCursor<'input> {
    pub fn new(input: &'input str) -> Self {
        Self { remaining: input }
    }

    pub fn is_exhausted(&self) -> bool {
        self.remaining.is_empty()
    }
}

impl LendingCursor for TableCursor<'_> {
    type View<'a>
        = RowView<'a>
    where
        Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::View<'a>> {
        if self.remaining.is_empty() {
            return None;
        }

        let current = self.remaining;
        let (row, rest) = current.split_once('\n').unwrap_or((current, ""));
        self.remaining = rest;
        Some(RowView { raw: row })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn lends_rows_in_order() {
        let mut cursor = TableCursor::new("a\tb\nc\td");
        let first = cursor.next().expect("first row").to_owned();
        assert_eq!(first, vec![String::from("a"), String::from("b")]);
        assert_eq!(cursor.next().expect("second row").raw(), "c\td");
        assert!(cursor.next().is_none());
    }

    #[test]
    fn preserves_an_empty_row_before_a_newline() {
        let mut cursor = TableCursor::new("\nlast");
        assert_eq!(cursor.next().expect("empty row").raw(), "");
        assert_eq!(cursor.next().expect("last row").raw(), "last");
    }

    #[test]
    fn empty_input_has_no_rows() {
        assert!(TableCursor::new("").next().is_none());
    }
}

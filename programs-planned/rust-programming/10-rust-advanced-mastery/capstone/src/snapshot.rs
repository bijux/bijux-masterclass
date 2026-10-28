use crate::{format, RecordView, StoreError};

pub trait LendingRecords {
    type View<'a>
    where
        Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Result<Self::View<'a>, StoreError>>;
}

#[derive(Clone, Debug)]
pub struct Snapshot<const MAX_RECORD: usize> {
    bytes: Vec<u8>,
    count: usize,
}

impl<const MAX_RECORD: usize> Snapshot<MAX_RECORD> {
    pub(crate) fn from_bytes(bytes: Vec<u8>) -> Result<Self, StoreError> {
        let count = format::verify_archive::<MAX_RECORD>(&bytes)?;
        Ok(Self { bytes, count })
    }

    pub fn len(&self) -> usize {
        self.count
    }

    pub fn is_empty(&self) -> bool {
        self.count == 0
    }

    pub fn records(&self) -> RecordCursor<'_, MAX_RECORD> {
        RecordCursor {
            bytes: &self.bytes,
            remaining: self.count,
            offset: format::first_record_offset(),
            failed: false,
        }
    }

    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }
}

pub struct RecordCursor<'snapshot, const MAX_RECORD: usize> {
    bytes: &'snapshot [u8],
    remaining: usize,
    offset: usize,
    failed: bool,
}

impl<const MAX_RECORD: usize> LendingRecords for RecordCursor<'_, MAX_RECORD> {
    type View<'a>
        = RecordView<'a>
    where
        Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Result<Self::View<'a>, StoreError>> {
        if self.failed || self.remaining == 0 {
            return None;
        }

        match format::record_at::<MAX_RECORD>(self.bytes, self.offset) {
            Ok((view, next)) => {
                self.offset = next;
                self.remaining -= 1;
                Some(Ok(view))
            }
            Err(error) => {
                self.failed = true;
                Some(Err(error))
            }
        }
    }
}


#![deny(unsafe_op_in_unsafe_fn)]

use std::alloc::{Layout, alloc_zeroed, dealloc};
use std::fmt;
use std::ptr::NonNull;

pub struct AlignedBytes {
    pointer: NonNull<u8>,
    length: usize,
    alignment: usize,
    layout: Option<Layout>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AllocationError {
    InvalidLayout {
        length: usize,
        alignment: usize,
    },
    AllocationFailed {
        length: usize,
        alignment: usize,
    },
}

impl fmt::Display for AllocationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for AllocationError {}

impl AlignedBytes {
    pub fn new_zeroed(length: usize, alignment: usize) -> Result<Self, AllocationError> {
        let layout = Layout::from_size_align(length.max(1), alignment).map_err(|_| {
            AllocationError::InvalidLayout {
                length,
                alignment,
            }
        })?;

        if length == 0 {
            return Ok(Self {
                pointer: NonNull::dangling(),
                length: 0,
                alignment: layout.align(),
                layout: None,
            });
        }

        // SAFETY: `layout` was validated and has non-zero size. A successful
        // allocation is immediately transferred into this unique owner.
        let raw = unsafe { alloc_zeroed(layout) };
        let pointer = NonNull::new(raw).ok_or(AllocationError::AllocationFailed {
            length,
            alignment,
        })?;
        Ok(Self {
            pointer,
            length,
            alignment: layout.align(),
            layout: Some(layout),
        })
    }

    #[must_use]
    pub const fn len(&self) -> usize {
        self.length
    }

    #[must_use]
    pub const fn is_empty(&self) -> bool {
        self.length == 0
    }

    #[must_use]
    pub const fn alignment(&self) -> usize {
        self.alignment
    }

    #[must_use]
    pub fn as_slice(&self) -> &[u8] {
        if self.length == 0 {
            return &[];
        }
        // SAFETY: a non-empty value owns a live allocation valid for `length`
        // initialized bytes. The result is tied to this shared owner borrow.
        unsafe { std::slice::from_raw_parts(self.pointer.as_ptr(), self.length) }
    }

    #[must_use]
    pub fn as_mut_slice(&mut self) -> &mut [u8] {
        if self.length == 0 {
            return &mut [];
        }
        // SAFETY: exclusive access to the owner establishes exclusive access to
        // its live allocation for the returned slice lifetime.
        unsafe { std::slice::from_raw_parts_mut(self.pointer.as_ptr(), self.length) }
    }

    pub fn fill(&mut self, value: u8) {
        self.as_mut_slice().fill(value);
    }
}

impl fmt::Debug for AlignedBytes {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("AlignedBytes")
            .field("length", &self.length)
            .field("alignment", &self.alignment())
            .finish_non_exhaustive()
    }
}

impl Drop for AlignedBytes {
    fn drop(&mut self) {
        if let Some(layout) = self.layout {
            // SAFETY: the pointer was allocated with this exact layout, remains
            // uniquely owned, and `Drop` runs at most once.
            unsafe { dealloc(self.pointer.as_ptr(), layout) };
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{AlignedBytes, AllocationError};

    #[test]
    fn nonzero_allocation_is_zeroed_aligned_and_mutable() {
        let mut bytes = AlignedBytes::new_zeroed(37, 64).expect("valid allocation");
        assert_eq!(bytes.len(), 37);
        assert_eq!((bytes.as_slice().as_ptr() as usize) % 64, 0);
        assert!(bytes.as_slice().iter().all(|byte| *byte == 0));
        bytes.fill(9);
        assert!(bytes.as_slice().iter().all(|byte| *byte == 9));
    }

    #[test]
    fn zero_length_performs_no_visible_allocation() {
        let bytes = AlignedBytes::new_zeroed(0, 128).expect("valid empty value");
        assert!(bytes.is_empty());
        assert_eq!(bytes.alignment(), 128);
        assert_eq!(bytes.as_slice(), &[]);
    }

    #[test]
    fn invalid_alignment_is_rejected_before_allocation() {
        assert!(matches!(
            AlignedBytes::new_zeroed(8, 3),
            Err(AllocationError::InvalidLayout { .. })
        ));
    }
}


//! A minimal owning abstraction over a manually allocated byte region.
//!
//! The unsafe operations are intentionally concentrated here so callers use
//! ordinary slices. The type is educational, not a replacement for `Vec<u8>`.

use std::alloc::{Layout, alloc_zeroed, dealloc};
use std::fmt;
use std::ptr::NonNull;

/// An allocation failure or invalid layout request.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AllocationError {
    InvalidLayout,
    AllocationFailed,
}

impl fmt::Display for AllocationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidLayout => formatter.write_str("invalid size/alignment layout"),
            Self::AllocationFailed => formatter.write_str("allocator returned a null pointer"),
        }
    }
}

impl std::error::Error for AllocationError {}

/// An owned zero-initialized byte region with a caller-selected alignment.
pub struct AlignedBytes {
    pointer: NonNull<u8>,
    length: usize,
    alignment: usize,
    layout: Option<Layout>,
}

impl AlignedBytes {
    /// Allocate `length` zeroed bytes at `alignment`.
    pub fn new_zeroed(length: usize, alignment: usize) -> Result<Self, AllocationError> {
        let validation_layout = Layout::from_size_align(length.max(1), alignment)
            .map_err(|_| AllocationError::InvalidLayout)?;

        if length == 0 {
            return Ok(Self {
                pointer: NonNull::dangling(),
                length: 0,
                alignment: validation_layout.align(),
                layout: None,
            });
        }

        // SAFETY: `validation_layout` is non-zero in size and was accepted by
        // `Layout::from_size_align`. Ownership of a successful allocation is
        // transferred immediately into the returned `AlignedBytes` value.
        let raw = unsafe { alloc_zeroed(validation_layout) };
        let pointer = NonNull::new(raw).ok_or(AllocationError::AllocationFailed)?;

        Ok(Self {
            pointer,
            length,
            alignment: validation_layout.align(),
            layout: Some(validation_layout),
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

        // SAFETY: a non-empty value owns an allocation valid for `length`
        // bytes. Shared access to `self` prevents mutable access through this
        // safe API for the duration of the returned slice.
        unsafe { std::slice::from_raw_parts(self.pointer.as_ptr(), self.length) }
    }

    #[must_use]
    pub fn as_mut_slice(&mut self) -> &mut [u8] {
        if self.length == 0 {
            return &mut [];
        }

        // SAFETY: a non-empty value owns an allocation valid for `length`
        // bytes. Exclusive access to `self` establishes exclusive access to
        // the returned region for the lifetime of the slice.
        unsafe { std::slice::from_raw_parts_mut(self.pointer.as_ptr(), self.length) }
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
            // SAFETY: `pointer` was allocated with exactly `layout`, remains
            // owned by this value, and `drop` runs at most once.
            unsafe { dealloc(self.pointer.as_ptr(), layout) };
        }
    }
}

#[cfg(test)]
mod tests {
    use super::AlignedBytes;

    #[test]
    fn allocation_is_zeroed_and_aligned() {
        let mut bytes = AlignedBytes::new_zeroed(32, 64).expect("valid allocation");
        assert_eq!(bytes.as_slice(), &[0; 32]);
        assert_eq!((bytes.as_slice().as_ptr() as usize) % 64, 0);
        bytes.as_mut_slice()[3] = 9;
        assert_eq!(bytes.as_slice()[3], 9);
    }

    #[test]
    fn zero_length_has_no_allocation() {
        let bytes = AlignedBytes::new_zeroed(0, 128).expect("valid zero-length layout");
        assert!(bytes.is_empty());
        assert_eq!(bytes.alignment(), 128);
    }
}

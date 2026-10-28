use std::mem::MaybeUninit;

pub(crate) struct InlineBatch<T, const N: usize> {
    slots: [MaybeUninit<T>; N],
    len: usize,
}

impl<T, const N: usize> InlineBatch<T, N> {
    pub(crate) fn new() -> Self {
        Self {
            slots: std::array::from_fn(|_| MaybeUninit::uninit()),
            len: 0,
        }
    }

    pub(crate) fn len(&self) -> usize {
        self.len
    }

    pub(crate) fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub(crate) fn push(&mut self, value: T) -> Result<(), T> {
        if self.len == N {
            return Err(value);
        }
        self.slots[self.len].write(value);
        self.len += 1;
        Ok(())
    }

    pub(crate) fn as_slice(&self) -> &[T] {
        // SAFETY: exactly `0..len` is initialized contiguous storage for `T`.
        // The shared borrow prevents mutation for the returned slice lifetime.
        unsafe { std::slice::from_raw_parts(self.slots.as_ptr().cast::<T>(), self.len) }
    }
}

impl<T, const N: usize> Default for InlineBatch<T, N> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T, const N: usize> Drop for InlineBatch<T, N> {
    fn drop(&mut self) {
        for slot in &mut self.slots[..self.len] {
            // SAFETY: every slot in the initialized prefix contains one live
            // value still owned by the batch, and each slot is visited once.
            unsafe { slot.assume_init_drop() };
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{cell::Cell, rc::Rc};

    struct DropCount(Rc<Cell<usize>>);

    impl Drop for DropCount {
        fn drop(&mut self) {
            self.0.set(self.0.get() + 1);
        }
    }

    #[test]
    fn values_are_dropped_exactly_once() {
        let count = Rc::new(Cell::new(0));
        {
            let mut batch = InlineBatch::<DropCount, 3>::new();
            assert!(batch.push(DropCount(count.clone())).is_ok());
            assert!(batch.push(DropCount(count.clone())).is_ok());
            assert_eq!(batch.len(), 2);
        }
        assert_eq!(count.get(), 2);
    }

    #[test]
    fn transitions_match_a_vec_oracle() {
        let mut batch = InlineBatch::<u8, 3>::new();
        let mut oracle = Vec::new();

        for value in [1, 2, 3] {
            assert_eq!(batch.push(value), Ok(()));
            oracle.push(value);
            assert_eq!(batch.as_slice(), oracle.as_slice());
        }

        assert_eq!(batch.push(4), Err(4));
        assert_eq!(batch.as_slice(), oracle.as_slice());
    }

    #[test]
    fn zero_capacity_is_a_defined_full_state() {
        let mut batch = InlineBatch::<u8, 0>::new();
        assert_eq!(batch.push(7), Err(7));
        assert!(batch.as_slice().is_empty());
    }
}

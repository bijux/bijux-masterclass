use std::mem::MaybeUninit;

pub struct InlineBatch<T, const N: usize> {
    slots: [MaybeUninit<T>; N],
    len: usize,
}

impl<T, const N: usize> InlineBatch<T, N> {
    pub fn new() -> Self {
        Self {
            slots: std::array::from_fn(|_| MaybeUninit::uninit()),
            len: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn is_full(&self) -> bool {
        self.len == N
    }

    pub fn push(&mut self, value: T) -> Result<(), T> {
        if self.is_full() {
            return Err(value);
        }

        self.slots[self.len].write(value);
        self.len += 1;
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.is_empty() {
            return None;
        }

        self.len -= 1;
        // SAFETY: the initialized-prefix invariant says that slot `len`
        // contains one live `T`. Decrementing first removes that slot from the
        // prefix before ownership is transferred to the caller.
        Some(unsafe { self.slots[self.len].assume_init_read() })
    }

    pub fn as_slice(&self) -> &[T] {
        // SAFETY: `0..len` is a contiguous, aligned prefix of initialized `T`
        // values. The shared borrow prevents mutation for the returned lifetime.
        unsafe { std::slice::from_raw_parts(self.slots.as_ptr().cast::<T>(), self.len) }
    }

    pub fn as_mut_slice(&mut self) -> &mut [T] {
        // SAFETY: `&mut self` grants exclusive access to the initialized prefix,
        // and no element outside `0..len` is included in the returned slice.
        unsafe {
            std::slice::from_raw_parts_mut(self.slots.as_mut_ptr().cast::<T>(), self.len)
        }
    }

    pub fn clear(&mut self) {
        while let Some(value) = self.pop() {
            drop(value);
        }
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
            // SAFETY: exactly the initialized prefix contains live values still
            // owned by the batch. Each slot is visited once during destruction.
            unsafe { slot.assume_init_drop() };
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::Cell;
    use std::rc::Rc;

    struct DropCounter(Rc<Cell<usize>>);

    impl Drop for DropCounter {
        fn drop(&mut self) {
            self.0.set(self.0.get() + 1);
        }
    }

    #[test]
    fn drops_each_value_exactly_once() {
        let drops = Rc::new(Cell::new(0));
        {
            let mut batch = InlineBatch::<DropCounter, 3>::new();
            assert!(batch.push(DropCounter(drops.clone())).is_ok());
            assert!(batch.push(DropCounter(drops.clone())).is_ok());
            drop(batch.pop());
            assert_eq!(drops.get(), 1);
        }
        assert_eq!(drops.get(), 2);
    }

    #[test]
    fn rejected_push_returns_ownership() {
        let mut batch = InlineBatch::<String, 1>::new();
        batch.push("first".into()).expect("space");
        assert_eq!(batch.push("second".into()), Err("second".into()));
        assert_eq!(batch.as_slice(), ["first"]);
    }

    #[test]
    fn mutable_slice_updates_only_live_values() {
        let mut batch = InlineBatch::<u8, 3>::new();
        batch.push(1).expect("space");
        batch.push(2).expect("space");
        batch.as_mut_slice()[1] = 9;
        assert_eq!(batch.as_slice(), [1, 9]);
    }

    #[test]
    fn zero_capacity_is_defined() {
        let mut batch = InlineBatch::<u8, 0>::new();
        assert_eq!(batch.push(1), Err(1));
        assert!(batch.as_slice().is_empty());
    }
}

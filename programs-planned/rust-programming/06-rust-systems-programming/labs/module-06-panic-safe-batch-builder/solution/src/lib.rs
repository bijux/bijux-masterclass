
#![deny(unsafe_op_in_unsafe_fn)]

use std::mem::MaybeUninit;

pub fn try_build_array<T, E, const N: usize>(
    mut build: impl FnMut(usize) -> Result<T, E>,
) -> Result<[T; N], E> {
    let mut slots: [MaybeUninit<T>; N] = std::array::from_fn(|_| MaybeUninit::uninit());

    struct Guard<'a, T, const N: usize> {
        slots: &'a mut [MaybeUninit<T>; N],
        initialized: usize,
    }

    impl<T, const N: usize> Drop for Guard<'_, T, N> {
        fn drop(&mut self) {
            for slot in &mut self.slots[..self.initialized] {
                // SAFETY: `initialized` advances only after `write`, so exactly
                // this prefix contains live `T` values, each still owned here.
                unsafe { slot.assume_init_drop() };
            }
        }
    }

    let mut guard = Guard {
        slots: &mut slots,
        initialized: 0,
    };

    for index in 0..N {
        let value = build(index)?;
        guard.slots[index].write(value);
        guard.initialized += 1;
    }

    let array_pointer = guard.slots.as_ptr().cast::<T>() as *const [T; N];
    guard.initialized = 0;
    // SAFETY: all `N` elements were initialized exactly once. `MaybeUninit<T>`
    // has the same layout and alignment as `T`; `array_pointer` addresses the
    // complete initialized array. Clearing the guard count transfers cleanup
    // responsibility to the returned array, so the source storage will not drop
    // the moved values.
    // SAFETY: the preceding proof establishes validity for this exact read.
    let result = unsafe { array_pointer.read() };
    drop(guard);
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::try_build_array;
    use std::cell::Cell;
    use std::panic::{AssertUnwindSafe, catch_unwind};
    use std::rc::Rc;

    #[derive(Debug)]
    struct Token(Rc<Cell<usize>>);

    impl Drop for Token {
        fn drop(&mut self) {
            self.0.set(self.0.get() + 1);
        }
    }

    #[test]
    fn success_returns_the_array() {
        assert_eq!(
            try_build_array::<_, (), 3>(|index| Ok(index)).expect("build succeeds"),
            [0, 1, 2]
        );
    }

    #[test]
    fn error_drops_exactly_the_initialized_prefix() {
        let drops = Rc::new(Cell::new(0));
        let result: Result<[Token; 4], usize> = try_build_array(|index| {
            if index == 2 {
                Err(index)
            } else {
                Ok(Token(Rc::clone(&drops)))
            }
        });
        assert!(matches!(result, Err(2)));
        assert_eq!(drops.get(), 2);
    }

    #[test]
    fn panic_drops_exactly_the_initialized_prefix() {
        let drops = Rc::new(Cell::new(0));
        let observed = Rc::clone(&drops);
        let result = catch_unwind(AssertUnwindSafe(|| {
            let _: Result<[Token; 4], ()> = try_build_array(|index| {
                if index == 3 {
                    panic!("construction panic");
                }
                Ok(Token(Rc::clone(&observed)))
            });
        }));
        assert!(result.is_err());
        assert_eq!(drops.get(), 3);
    }

    #[test]
    fn zero_length_works_without_invoking_the_builder() {
        let value: [String; 0] =
            try_build_array::<_, (), 0>(|_| unreachable!()).expect("zero array");
        assert!(value.is_empty());
    }
}

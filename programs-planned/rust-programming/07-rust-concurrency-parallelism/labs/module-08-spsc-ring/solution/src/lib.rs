#![deny(unsafe_op_in_unsafe_fn)]

use std::cell::{Cell, UnsafeCell};
use std::marker::PhantomData;
use std::mem::MaybeUninit;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RingError { ZeroCapacity, CapacityOverflow }
#[derive(Debug, PartialEq, Eq)]
pub struct Full<T>(pub T);

struct Inner<T> {
    slots: Box<[UnsafeCell<MaybeUninit<T>>]>,
    head: AtomicUsize,
    tail: AtomicUsize,
}

// SAFETY: `ring` creates exactly one non-cloneable producer and one non-cloneable
// consumer. Endpoint methods require `&mut self`, and endpoint marker fields make
// them !Sync. Head/tail publication gives one role exclusive access to each slot.
// Values move from the producer thread to the consumer thread, requiring T: Send.
unsafe impl<T: Send> Sync for Inner<T> {}

impl<T> Inner<T> {
    fn next(&self, index: usize) -> usize {
        if index + 1 == self.slots.len() { 0 } else { index + 1 }
    }
}

impl<T> Drop for Inner<T> {
    fn drop(&mut self) {
        let mut head = *self.head.get_mut();
        let tail = *self.tail.get_mut();
        while head != tail {
            let slot = &mut self.slots[head];
            // SAFETY: all endpoints are gone before Inner::drop runs. The modular
            // interval [head, tail) contains exactly the unread initialized slots.
            unsafe { slot.get_mut().assume_init_drop() };
            head = if head + 1 == self.slots.len() { 0 } else { head + 1 };
        }
    }
}

pub struct Producer<T> {
    inner: Arc<Inner<T>>,
    _not_sync: PhantomData<Cell<()>>,
}

pub struct Consumer<T> {
    inner: Arc<Inner<T>>,
    _not_sync: PhantomData<Cell<()>>,
}

pub fn ring<T>(capacity: usize) -> Result<(Producer<T>, Consumer<T>), RingError> {
    let slots = physical_slots(capacity)?;
    let mut storage = Vec::with_capacity(slots);
    storage.resize_with(slots, || UnsafeCell::new(MaybeUninit::uninit()));
    let inner = Arc::new(Inner { slots: storage.into_boxed_slice(), head: AtomicUsize::new(0), tail: AtomicUsize::new(0) });
    Ok((
        Producer { inner: Arc::clone(&inner), _not_sync: PhantomData },
        Consumer { inner, _not_sync: PhantomData },
    ))
}

#[must_use]
pub fn physical_slots(capacity: usize) -> Result<usize, RingError> {
    if capacity == 0 { return Err(RingError::ZeroCapacity); }
    capacity.checked_add(1).ok_or(RingError::CapacityOverflow)
}

impl<T> Producer<T> {
    pub fn try_push(&mut self, value: T) -> Result<(), Full<T>> {
        let tail = self.inner.tail.load(Ordering::Relaxed);
        let next = self.inner.next(tail);
        if next == self.inner.head.load(Ordering::Acquire) { return Err(Full(value)); }
        // SAFETY: this is the unique producer. `next != head` proves the tail slot
        // has been released by the consumer and is currently uninitialized.
        unsafe { (*self.inner.slots[tail].get()).write(value) };
        self.inner.tail.store(next, Ordering::Release);
        Ok(())
    }

    #[must_use]
    pub fn capacity(&self) -> usize { self.inner.slots.len() - 1 }
}

impl<T> Consumer<T> {
    pub fn try_pop(&mut self) -> Option<T> {
        let head = self.inner.head.load(Ordering::Relaxed);
        if head == self.inner.tail.load(Ordering::Acquire) { return None; }
        // SAFETY: this is the unique consumer. Acquire observation of a different
        // tail proves the producer initialized the current head slot before publish.
        let value = unsafe { (*self.inner.slots[head].get()).assume_init_read() };
        self.inner.head.store(self.inner.next(head), Ordering::Release);
        Some(value)
    }
}

#[cfg(test)]
mod tests {
    use super::{Full, RingError, ring};
    use std::sync::Arc;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::thread;

    #[test]
    fn empty_full_fifo_and_wraparound() {
        let (mut producer, mut consumer) = ring(2).expect("valid capacity");
        assert_eq!(consumer.try_pop(), None);
        assert_eq!(producer.try_push(1), Ok(()));
        assert_eq!(producer.try_push(2), Ok(()));
        assert_eq!(producer.try_push(3), Err(Full(3)));
        assert_eq!(consumer.try_pop(), Some(1));
        assert_eq!(producer.try_push(3), Ok(()));
        assert_eq!(consumer.try_pop(), Some(2));
        assert_eq!(consumer.try_pop(), Some(3));
        assert_eq!(consumer.try_pop(), None);
    }

    #[test]
    fn endpoints_move_to_threads() {
        let (mut producer, mut consumer) = ring(8).expect("valid capacity");
        let p = thread::spawn(move || {
            for value in 0..1000 {
                let mut pending = value;
                loop {
                    match producer.try_push(pending) {
                        Ok(()) => break,
                        Err(Full(value)) => { pending = value; thread::yield_now(); }
                    }
                }
            }
        });
        let c = thread::spawn(move || {
            let mut output = Vec::new();
            while output.len() < 1000 {
                match consumer.try_pop() { Some(v) => output.push(v), None => thread::yield_now() }
            }
            output
        });
        p.join().expect("producer joins");
        assert_eq!(c.join().expect("consumer joins"), (0..1000).collect::<Vec<_>>());
    }

    #[test]
    fn unread_values_drop_exactly_once() {
        struct Counted(Arc<AtomicUsize>);
        impl Drop for Counted { fn drop(&mut self) { self.0.fetch_add(1, Ordering::Relaxed); } }
        let drops = Arc::new(AtomicUsize::new(0));
        let (mut producer, mut consumer) = ring(3).expect("valid capacity");
        producer.try_push(Counted(Arc::clone(&drops))).map_err(|_| ()).expect("space");
        producer.try_push(Counted(Arc::clone(&drops))).map_err(|_| ()).expect("space");
        drop(consumer.try_pop());
        drop(producer);
        drop(consumer);
        assert_eq!(drops.load(Ordering::Relaxed), 2);
    }

    #[test]
    fn rejects_zero_capacity() {
        assert!(matches!(ring::<u8>(0), Err(RingError::ZeroCapacity)));
    }
}

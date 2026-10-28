use std::collections::VecDeque;
use std::num::NonZeroUsize;
use std::sync::{Condvar, Mutex, MutexGuard};

#[derive(Debug)]
struct State<T> {
    items: VecDeque<T>,
    closed: bool,
}

#[derive(Debug)]
pub(crate) struct Closed<T>(pub T);

#[derive(Debug)]
pub(crate) struct BoundedQueue<T> {
    capacity: NonZeroUsize,
    state: Mutex<State<T>>,
    not_empty: Condvar,
    not_full: Condvar,
}

impl<T> BoundedQueue<T> {
    pub(crate) fn new(capacity: NonZeroUsize) -> Self {
        Self {
            capacity,
            state: Mutex::new(State { items: VecDeque::new(), closed: false }),
            not_empty: Condvar::new(),
            not_full: Condvar::new(),
        }
    }

    fn lock(&self) -> MutexGuard<'_, State<T>> {
        self.state.lock().unwrap_or_else(|poisoned| poisoned.into_inner())
    }

    pub(crate) fn push(&self, item: T) -> Result<(), Closed<T>> {
        let mut state = self.lock();
        while state.items.len() == self.capacity.get() && !state.closed {
            state = self.not_full.wait(state).unwrap_or_else(|poisoned| poisoned.into_inner());
        }
        if state.closed {
            return Err(Closed(item));
        }
        state.items.push_back(item);
        self.not_empty.notify_one();
        Ok(())
    }

    pub(crate) fn pop(&self) -> Option<T> {
        let mut state = self.lock();
        while state.items.is_empty() && !state.closed {
            state = self.not_empty.wait(state).unwrap_or_else(|poisoned| poisoned.into_inner());
        }
        let item = state.items.pop_front();
        if item.is_some() {
            self.not_full.notify_one();
        }
        item
    }

    pub(crate) fn close(&self) {
        let mut state = self.lock();
        state.closed = true;
        drop(state);
        self.not_empty.notify_all();
        self.not_full.notify_all();
    }
}

#[cfg(test)]
mod tests {
    use super::BoundedQueue;
    use std::num::NonZeroUsize;
    use std::sync::{Arc, mpsc};
    use std::thread;

    #[test]
    fn full_push_unblocks_after_pop() {
        let queue = Arc::new(BoundedQueue::new(NonZeroUsize::new(1).expect("nonzero")));
        queue.push(1).expect("space");
        let (entered_tx, entered_rx) = mpsc::channel();
        let (done_tx, done_rx) = mpsc::channel();
        let child = {
            let queue = Arc::clone(&queue);
            thread::spawn(move || {
                entered_tx.send(()).expect("receiver");
                let result = queue.push(2);
                done_tx.send(result.is_ok()).expect("receiver");
            })
        };
        entered_rx.recv().expect("child reached push");
        assert_eq!(queue.pop(), Some(1));
        assert_eq!(done_rx.recv().expect("child completes"), true);
        queue.close();
        child.join().expect("joins");
        assert_eq!(queue.pop(), Some(2));
        assert_eq!(queue.pop(), None);
    }

    #[test]
    fn close_returns_blocked_item_and_wakes_empty_consumer() {
        let queue = Arc::new(BoundedQueue::new(NonZeroUsize::new(1).expect("nonzero")));
        let consumer = {
            let queue = Arc::clone(&queue);
            thread::spawn(move || queue.pop())
        };
        queue.close();
        assert_eq!(consumer.join().expect("joins"), None);
        assert_eq!(queue.push(7).expect_err("closed").0, 7);
    }
}

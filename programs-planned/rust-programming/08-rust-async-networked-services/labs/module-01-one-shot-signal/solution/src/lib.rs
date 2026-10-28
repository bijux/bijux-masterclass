use std::{
    future::Future,
    pin::Pin,
    sync::{Arc, Mutex},
    task::{Context, Poll, Waker},
};

struct State<T> {
    value: Option<T>,
    waker: Option<Waker>,
    receiver_alive: bool,
    sender_alive: bool,
    completed: bool,
}

pub struct Sender<T> {
    state: Arc<Mutex<State<T>>>,
}

pub struct Receiver<T> {
    state: Arc<Mutex<State<T>>>,
}

pub fn channel<T>() -> (Sender<T>, Receiver<T>) {
    let state = Arc::new(Mutex::new(State {
        value: None,
        waker: None,
        receiver_alive: true,
        sender_alive: true,
        completed: false,
    }));
    (Sender { state: Arc::clone(&state) }, Receiver { state })
}

impl<T> Sender<T> {
    pub fn send(self, value: T) -> Result<(), T> {
        let waker = {
            let mut state = self
                .state
                .lock()
                .unwrap_or_else(|poisoned| poisoned.into_inner());
            state.sender_alive = false;
            if !state.receiver_alive || state.completed {
                return Err(value);
            }
            state.value = Some(value);
            state.waker.take()
        };
        if let Some(waker) = waker {
            waker.wake();
        }
        Ok(())
    }
}

impl<T> Drop for Sender<T> {
    fn drop(&mut self) {
        let waker = {
            let mut state = self
                .state
                .lock()
                .unwrap_or_else(|poisoned| poisoned.into_inner());
            state.sender_alive = false;
            state.waker.take()
        };
        if let Some(waker) = waker {
            waker.wake();
        }
    }
}

impl<T> Future for Receiver<T> {
    type Output = Option<T>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let mut state = self
            .state
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
        if state.completed {
            drop(state);
            panic!("one-shot receiver polled after completion");
        }
        if let Some(value) = state.value.take() {
            state.completed = true;
            return Poll::Ready(Some(value));
        }
        if !state.sender_alive {
            state.completed = true;
            return Poll::Ready(None);
        }
        if state.waker.as_ref().is_none_or(|stored| !stored.will_wake(cx.waker())) {
            state.waker = Some(cx.waker().clone());
        }
        Poll::Pending
    }
}

impl<T> Drop for Receiver<T> {
    fn drop(&mut self) {
        let mut state = self
            .state
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
        state.receiver_alive = false;
        state.waker = None;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::task::{Wake, Waker};

    struct Counter(AtomicUsize);
    impl Wake for Counter {
        fn wake(self: Arc<Self>) {
            let _previous = self.0.fetch_add(1, Ordering::SeqCst);
        }
    }

    fn counter_waker() -> (Arc<Counter>, Waker) {
        let counter = Arc::new(Counter(AtomicUsize::new(0)));
        (Arc::clone(&counter), Waker::from(counter))
    }

    #[tokio::test]
    async fn completion_before_await_is_observed() {
        let (sender, receiver) = channel();
        sender.send(7).unwrap();
        assert_eq!(receiver.await, Some(7));
    }

    #[tokio::test]
    async fn sender_drop_completes_with_none() {
        let (sender, receiver) = channel::<u64>();
        drop(sender);
        assert_eq!(receiver.await, None);
    }

    #[test]
    fn latest_distinct_waker_is_used() {
        let (sender, mut receiver) = channel();
        let (first_count, first) = counter_waker();
        let (second_count, second) = counter_waker();
        let mut first_cx = Context::from_waker(&first);
        let mut second_cx = Context::from_waker(&second);
        assert!(Pin::new(&mut receiver).poll(&mut first_cx).is_pending());
        assert!(Pin::new(&mut receiver).poll(&mut second_cx).is_pending());
        sender.send(9).unwrap();
        assert_eq!(first_count.0.load(Ordering::SeqCst), 0);
        assert_eq!(second_count.0.load(Ordering::SeqCst), 1);
        assert_eq!(Pin::new(&mut receiver).poll(&mut second_cx), Poll::Ready(Some(9)));
    }

    struct LockCheckingWake<T> {
        state: Arc<Mutex<State<T>>>,
        woke_without_lock: AtomicUsize,
    }

    impl<T: Send + 'static> Wake for LockCheckingWake<T> {
        fn wake(self: Arc<Self>) {
            if self.state.try_lock().is_ok() {
                let _previous = self.woke_without_lock.fetch_add(1, Ordering::SeqCst);
            }
        }
    }

    #[test]
    fn producer_wakes_only_after_releasing_the_state_lock() {
        let (sender, mut receiver) = channel::<u64>();
        let checker = Arc::new(LockCheckingWake {
            state: Arc::clone(&receiver.state),
            woke_without_lock: AtomicUsize::new(0),
        });
        let waker = Waker::from(Arc::clone(&checker));
        let mut context = Context::from_waker(&waker);

        assert!(Pin::new(&mut receiver).poll(&mut context).is_pending());
        sender.send(17).unwrap();

        assert_eq!(checker.woke_without_lock.load(Ordering::SeqCst), 1);
        assert_eq!(Pin::new(&mut receiver).poll(&mut context), Poll::Ready(Some(17)));
    }

    #[test]
    fn cancelled_receiver_returns_value_to_sender() {
        let (sender, receiver) = channel();
        drop(receiver);
        assert_eq!(sender.send("kept"), Err("kept"));
    }
}

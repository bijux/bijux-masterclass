//! RAII leases that return checked-out items exactly once.
#[derive(Debug, Default)]
pub struct Pool<T> {
    items: Vec<T>
}
impl<T> Pool<T> {
    pub fn new(items: Vec<T>) -> Self {
        Self {
            items
        }
    }
    pub fn available(&self) -> usize {
        self.items.len()
    }
    pub fn checkout(&mut self) -> Option<Lease<'_, T>> {
        let item = self.items.pop()?;
        Some(Lease {
            item: Some(item), return_to: &mut self.items
        })
    }
}
#[derive(Debug)]
pub struct Lease<'a, T> {
    item: Option<T>,
    return_to: &'a mut Vec<T>,
}
impl<T> Lease<'_, T> {
    pub fn get(&self) -> &T {
        match self.item.as_ref() {
            Some(item) => item, None => unreachable!("public transitions consume the lease")
        }
    }
    pub fn get_mut(&mut self) -> &mut T {
        match self.item.as_mut() {
            Some(item) => item, None => unreachable!("public transitions consume the lease")
        }
    }
    pub fn discard(mut self) {
        drop(self.item.take());
    }
    pub fn replace(mut self, replacement: T) -> T {
        let original = match self.item.take() {
            Some(item) => item, None => unreachable!("public transitions consume the lease")
        };
        self.return_to.push(replacement);
        original
    }
}
impl<T> Drop for Lease<'_, T> {
    fn drop(&mut self) {
        if let Some(item) = self.item.take() {
            self.return_to.push(item);
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::panic::{
        catch_unwind, AssertUnwindSafe
    };
    #[test]
    fn ordinary_drop_returns_item() {
        let mut pool = Pool::new(vec![String::from("one")]);
        {
            let mut lease = match pool.checkout() {
                Some(v) => v, None => panic!("missing")
            };
            lease.get_mut().push('!');
        }
        assert_eq!(pool.available(), 1);
        let lease = match pool.checkout() {
            Some(v) => v, None => panic!("missing")
        };
        assert_eq!(lease.get(), "one!");
    }
    #[test]
    fn discard_removes_item() {
        let mut pool = Pool::new(vec![1]);
        match pool.checkout() {
            Some(lease) => lease.discard(), None => panic!("missing")
        }
        assert_eq!(pool.available(), 0);
    }
    #[test]
    fn replace_returns_old_and_keeps_new() {
        let mut pool = Pool::new(vec![1]);
        let old = match pool.checkout() {
            Some(lease) => lease.replace(9), None => panic!("missing")
        };
        assert_eq!(old, 1);
        let lease = match pool.checkout() {
            Some(v) => v, None => panic!("missing")
        };
        assert_eq!(*lease.get(), 9);
    }
    #[test]
    fn unwinding_returns_item() {
        let mut pool = Pool::new(vec![7]);
        let result = catch_unwind(AssertUnwindSafe(|| {
            let _lease = match pool.checkout() {
                Some(v) => v, None => panic!("missing")
            };
            panic!("intentional");
        }));
        assert!(result.is_err());
        assert_eq!(pool.available(), 1);
    }
}

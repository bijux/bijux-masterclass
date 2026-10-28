//! Owning pool baseline before RAII leases are introduced.

/// Explicitly managed resource pool.
#[derive(Debug, Default)]
pub struct Pool<T> {
    items: Vec<T>,
}

impl<T> Pool<T> {
    /// Creates a pool owning all supplied items.
    pub fn new(items: Vec<T>) -> Self {
        Self { items }
    }

    /// Returns the number of resources currently owned by the pool.
    pub fn available(&self) -> usize {
        self.items.len()
    }

    /// Transfers one resource to the caller.
    pub fn take(&mut self) -> Option<T> {
        self.items.pop()
    }

    /// Returns a resource explicitly.
    pub fn put_back(&mut self, item: T) {
        self.items.push(item);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_requires_manual_return() {
        let mut pool = Pool::new(vec![String::from("connection")]);
        let resource = pool.take().expect("one resource");
        assert_eq!(pool.available(), 0);
        pool.put_back(resource);
        assert_eq!(pool.available(), 1);
    }
}

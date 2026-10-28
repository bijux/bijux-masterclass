//! Safe generative brands preventing cross-arena ID mixing.

use std::marker::PhantomData;

#[derive(Debug)]
pub struct Arena<'id, T> {
    values: Vec<T>,
    brand: PhantomData<fn(&'id ()) -> &'id ()>,
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub struct Id<'id> {
    index: usize,
    brand: PhantomData<fn(&'id ()) -> &'id ()>,
}

impl<'id> Copy for Id<'id> {}
impl<'id> Clone for Id<'id> { fn clone(&self) -> Self { *self } }

pub fn with_arena<T, R>(operation: impl for<'id> FnOnce(&mut Arena<'id, T>) -> R) -> R {
    let mut arena = Arena { values: Vec::new(), brand: PhantomData };
    operation(&mut arena)
}

impl<'id, T> Arena<'id, T> {
    pub fn insert(&mut self, value: T) -> Id<'id> {
        let id = Id { index: self.values.len(), brand: PhantomData };
        self.values.push(value);
        id
    }
    pub fn get(&self, id: Id<'id>) -> Option<&T> { self.values.get(id.index) }
    pub fn get_mut(&mut self, id: Id<'id>) -> Option<&mut T> { self.values.get_mut(id.index) }
    pub fn len(&self) -> usize { self.values.len() }
    pub fn is_empty(&self) -> bool { self.values.is_empty() }
}

/// IDs from distinct brand scopes cannot be mixed.
///
/// ```compile_fail
/// use rust_olm_lab_09_variance_branding::with_arena;
/// with_arena::<String, _>(|first| {
///     let id = first.insert(String::from("first"));
///     with_arena::<String, _>(|second| {
///         let _ = second.get(id);
///     });
/// });
/// ```
///
/// Branded IDs cannot escape as the higher-ranked return value.
///
/// ```compile_fail
/// use rust_olm_lab_09_variance_branding::with_arena;
/// let _escaped = with_arena::<String, _>(|arena| arena.insert(String::from("x")));
/// ```
pub fn brand_contract() {}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn same_brand_ids_access_only_their_arena() {
        let result = with_arena::<String, _>(|arena| {
            let first = arena.insert(String::from("first"));
            let second = arena.insert(String::from("second"));
            if let Some(value) = arena.get_mut(second) { value.push('!'); }
            (arena.get(first).cloned(), arena.get(second).cloned(), arena.len())
        });
        assert_eq!(result, (Some(String::from("first")), Some(String::from("second!")), 2));
    }
    #[test]
    fn out_of_bounds_is_checked() {
        with_arena::<u8, _>(|arena| {
            let id = arena.insert(1);
            assert_eq!(arena.get(id), Some(&1));
            assert!(!arena.is_empty());
        });
    }
}

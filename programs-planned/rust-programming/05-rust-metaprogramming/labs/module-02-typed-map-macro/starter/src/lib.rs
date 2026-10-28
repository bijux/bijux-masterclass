#![forbid(unsafe_code)]

use std::collections::BTreeMap;

pub fn empty<K: Ord, V>() -> BTreeMap<K, V> {
    BTreeMap::new()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_is_typed() {
        let map: BTreeMap<String, u64> = empty();
        assert!(map.is_empty());
    }
}

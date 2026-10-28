#![forbid(unsafe_code)]

#[macro_export]
macro_rules! typed_map {
    (
        $key_ty:ty => $value_ty:ty;
        $( $key:expr => $value:expr ),* $(,)?
    ) => {{
        let mut __typed_map: ::std::collections::BTreeMap<$key_ty, $value_ty> =
            ::std::collections::BTreeMap::new();

        $(
            let __typed_key: $key_ty = $key;
            let __typed_value: $value_ty = $value;
            __typed_map.insert(__typed_key, __typed_value);
        )*

        __typed_map
    }};
}

#[cfg(test)]
mod tests {
    #[test]
    fn empty_map_keeps_declared_types() {
        let map = crate::typed_map!(String => u64;);
        assert!(map.is_empty());
    }

    #[test]
    fn expressions_run_once_in_source_order() {
        use std::cell::RefCell;

        let log = RefCell::new(Vec::new());
        let map = crate::typed_map!(
            String => u64;
            {
                log.borrow_mut().push("k1");
                "a".to_owned()
            } => {
                log.borrow_mut().push("v1");
                1
            },
            {
                log.borrow_mut().push("k2");
                "b".to_owned()
            } => {
                log.borrow_mut().push("v2");
                2
            },
        );

        assert_eq!(log.into_inner(), vec!["k1", "v1", "k2", "v2"]);
        assert_eq!(map["b"], 2);
    }

    #[test]
    fn later_duplicate_replaces_the_previous_value() {
        let map = crate::typed_map!(&'static str => u32; "a" => 1, "a" => 2);
        assert_eq!(map["a"], 2);
    }
}

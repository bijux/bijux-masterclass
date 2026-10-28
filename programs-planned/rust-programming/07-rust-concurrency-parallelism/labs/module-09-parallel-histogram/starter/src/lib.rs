#![forbid(unsafe_code)]

use std::collections::BTreeMap;

#[must_use]
pub fn sequential(labels: &[String]) -> BTreeMap<String, usize> {
    labels.iter().fold(BTreeMap::new(), |mut map, label| {
        *map.entry(label.clone()).or_default() += 1;
        map
    })
}

#[cfg(test)]
mod tests {
    use super::sequential;
    #[test]
    fn baseline_histogram_is_ordered() {
        let labels = vec!["z".to_owned(), "a".to_owned(), "z".to_owned()];
        let map = sequential(&labels);
        assert_eq!(map.keys().cloned().collect::<Vec<_>>(), vec!["a", "z"]);
        assert_eq!(map["z"], 2);
    }
}

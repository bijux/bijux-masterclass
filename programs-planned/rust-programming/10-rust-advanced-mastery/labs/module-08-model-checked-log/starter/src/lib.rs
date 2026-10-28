use std::collections::BTreeMap;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Op {
    Put(String, String),
    Remove(String),
    Clear,
}

pub fn apply_model(model: &mut BTreeMap<String, String>, operation: &Op) {
    match operation {
        Op::Put(key, value) => {
            model.insert(key.clone(), value.clone());
        }
        Op::Remove(key) => {
            model.remove(key);
        }
        Op::Clear => model.clear(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_model_applies_one_operation() {
        let mut model = BTreeMap::new();
        apply_model(&mut model, &Op::Put("k".into(), "v".into()));
        assert_eq!(model.get("k").map(String::as_str), Some("v"));
    }
}

use std::collections::BTreeMap;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Op {
    Put(String, String),
    Remove(String),
    Clear,
}

#[derive(Default)]
pub struct Engine {
    items: Vec<(String, String)>,
}

impl Engine {
    pub fn apply(&mut self, operation: &Op) {
        match operation {
            Op::Put(key, value) => {
                if let Some((_, previous)) =
                    self.items.iter_mut().find(|(existing, _)| existing == key)
                {
                    *previous = value.clone();
                } else {
                    self.items.push((key.clone(), value.clone()));
                    self.items.sort_by(|left, right| left.0.cmp(&right.0));
                }
            }
            Op::Remove(key) => self.items.retain(|(existing, _)| existing != key),
            Op::Clear => self.items.clear(),
        }
    }

    pub fn snapshot(&self) -> BTreeMap<String, String> {
        self.items.iter().cloned().collect()
    }
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

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Divergence {
    pub prefix: Vec<Op>,
    pub engine: BTreeMap<String, String>,
    pub model: BTreeMap<String, String>,
}

pub fn explore(alphabet: &[Op], maximum_depth: usize) -> Result<usize, Divergence> {
    fn walk(
        prefix: &mut Vec<Op>,
        alphabet: &[Op],
        maximum_depth: usize,
        visited: &mut usize,
    ) -> Result<(), Divergence> {
        let mut model = BTreeMap::new();
        let mut engine = Engine::default();

        for operation in prefix.iter() {
            apply_model(&mut model, operation);
            engine.apply(operation);
            *visited += 1;
            let engine_state = engine.snapshot();
            if engine_state != model {
                return Err(Divergence {
                    prefix: prefix.clone(),
                    engine: engine_state,
                    model,
                });
            }
        }

        if prefix.len() == maximum_depth {
            return Ok(());
        }

        for operation in alphabet {
            prefix.push(operation.clone());
            walk(prefix, alphabet, maximum_depth, visited)?;
            prefix.pop();
        }
        Ok(())
    }

    let mut visited = 0;
    walk(
        &mut Vec::new(),
        alphabet,
        maximum_depth,
        &mut visited,
    )?;
    Ok(visited)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bounded_sequences_match_the_independent_model() {
        let operations = [
            Op::Put("a".into(), "1".into()),
            Op::Put("a".into(), "2".into()),
            Op::Put("b".into(), "3".into()),
            Op::Remove("a".into()),
            Op::Clear,
        ];
        assert!(explore(&operations, 4).expect("no divergence") > 0);
    }

    #[test]
    fn engine_snapshot_is_canonical() {
        let mut engine = Engine::default();
        engine.apply(&Op::Put("z".into(), "1".into()));
        engine.apply(&Op::Put("a".into(), "2".into()));
        assert_eq!(
            engine.snapshot().keys().cloned().collect::<Vec<_>>(),
            vec![String::from("a"), String::from("z")]
        );
    }
}

use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Artifact {
    pub id: String,
    pub payload: String,
    pub tag: Option<String>,
}

pub trait Policy {
    fn name(&self) -> &'static str;
    fn check(&self, artifact: &Artifact) -> Result<(), String>;
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Error {
    Format(&'static str),
    DuplicatePolicy(&'static str),
    Policy {
        policy: &'static str,
        message: String,
    },
    DuplicateArtifact(String),
    Capacity { maximum: usize },
}

pub struct Registry<const N: usize> {
    items: BTreeMap<String, Artifact>,
    policies: Vec<Box<dyn Policy>>,
}

impl<const N: usize> Default for Registry<N> {
    fn default() -> Self {
        Self {
            items: BTreeMap::new(),
            policies: Vec::new(),
        }
    }
}

impl<const N: usize> Registry<N> {
    pub fn register<P>(&mut self, policy: P) -> Result<(), Error>
    where
        P: Policy + 'static,
    {
        let name = policy.name();
        if self.policies.iter().any(|current| current.name() == name) {
            return Err(Error::DuplicatePolicy(name));
        }
        self.policies.push(Box::new(policy));
        Ok(())
    }

    pub fn insert(&mut self, artifact: Artifact) -> Result<(), Error> {
        self.validate_candidate(&artifact)?;
        if self.items.contains_key(&artifact.id) {
            return Err(Error::DuplicateArtifact(artifact.id));
        }
        if self.items.len() == N {
            return Err(Error::Capacity { maximum: N });
        }
        self.items.insert(artifact.id.clone(), artifact);
        Ok(())
    }

    pub fn insert_all(&mut self, artifacts: Vec<Artifact>) -> Result<(), Error> {
        let mut batch_ids = BTreeSet::new();
        for artifact in &artifacts {
            self.validate_candidate(artifact)?;
            if self.items.contains_key(&artifact.id) || !batch_ids.insert(artifact.id.clone()) {
                return Err(Error::DuplicateArtifact(artifact.id.clone()));
            }
        }
        if self.items.len().saturating_add(artifacts.len()) > N {
            return Err(Error::Capacity { maximum: N });
        }

        for artifact in artifacts {
            self.items.insert(artifact.id.clone(), artifact);
        }
        Ok(())
    }

    pub fn ids(&self) -> impl Iterator<Item = &str> {
        self.items.keys().map(String::as_str)
    }

    pub fn get(&self, id: &str) -> Option<&Artifact> {
        self.items.get(id)
    }

    fn validate_candidate(&self, artifact: &Artifact) -> Result<(), Error> {
        for policy in &self.policies {
            policy.check(artifact).map_err(|message| Error::Policy {
                policy: policy.name(),
                message,
            })?;
        }
        Ok(())
    }
}

pub struct NonEmptyPayload;

impl Policy for NonEmptyPayload {
    fn name(&self) -> &'static str {
        "non-empty-payload"
    }

    fn check(&self, artifact: &Artifact) -> Result<(), String> {
        if artifact.payload.is_empty() {
            Err("payload is empty".into())
        } else {
            Ok(())
        }
    }
}

pub fn decode(input: &str) -> Result<Artifact, Error> {
    let fields = input.split('|').collect::<Vec<_>>();
    match fields.as_slice() {
        ["V1", id, payload] if !id.is_empty() => Ok(Artifact {
            id: (*id).to_owned(),
            payload: (*payload).to_owned(),
            tag: None,
        }),
        ["V2", id, payload, tag] if !id.is_empty() => Ok(Artifact {
            id: (*id).to_owned(),
            payload: (*payload).to_owned(),
            tag: (!tag.is_empty()).then(|| (*tag).to_owned()),
        }),
        _ => Err(Error::Format("expected V1|id|payload or V2|id|payload|tag")),
    }
}

pub fn encode_v2(artifact: &Artifact) -> Result<String, Error> {
    if artifact.id.contains('|')
        || artifact.payload.contains('|')
        || artifact.tag.as_deref().is_some_and(|tag| tag.contains('|'))
    {
        return Err(Error::Format("fields may not contain |"));
    }
    Ok(format!(
        "V2|{}|{}|{}",
        artifact.id,
        artifact.payload,
        artifact.tag.as_deref().unwrap_or("")
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn both_versions_produce_one_stable_model() {
        assert_eq!(
            decode("V1|a|payload").expect("V1"),
            Artifact {
                id: "a".into(),
                payload: "payload".into(),
                tag: None,
            }
        );
        assert_eq!(
            decode("V2|a|payload|blue").expect("V2").tag.as_deref(),
            Some("blue")
        );
    }

    #[test]
    fn policy_failure_preserves_registry_state() {
        let mut registry = Registry::<2>::default();
        registry.register(NonEmptyPayload).expect("unique policy");
        let result = registry.insert(Artifact {
            id: "a".into(),
            payload: String::new(),
            tag: None,
        });
        assert!(matches!(result, Err(Error::Policy { .. })));
        assert_eq!(registry.ids().count(), 0);
    }

    #[test]
    fn batch_insert_is_all_or_nothing() {
        let mut registry = Registry::<2>::default();
        registry.register(NonEmptyPayload).expect("unique policy");
        let result = registry.insert_all(vec![
            Artifact {
                id: "a".into(),
                payload: "one".into(),
                tag: None,
            },
            Artifact {
                id: "a".into(),
                payload: "two".into(),
                tag: None,
            },
        ]);
        assert_eq!(result, Err(Error::DuplicateArtifact("a".into())));
        assert_eq!(registry.ids().count(), 0);
    }

    #[test]
    fn canonical_v2_encoding_is_deterministic() {
        let artifact = Artifact {
            id: "a".into(),
            payload: "payload".into(),
            tag: Some("blue".into()),
        };
        assert_eq!(encode_v2(&artifact), Ok("V2|a|payload|blue".into()));
    }
}

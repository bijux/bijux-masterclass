use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Product {
    pub target: String,
    pub profile: String,
    pub features: BTreeSet<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Matrix {
    pub targets: BTreeSet<String>,
    pub profiles: BTreeSet<String>,
    pub allowed_feature_sets: BTreeSet<BTreeSet<String>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Artifact {
    pub name: String,
    pub version: String,
    pub source_revision: String,
    pub lockfile_sha256: String,
    pub toolchain: String,
    pub product: Product,
    pub size_bytes: u64,
    pub sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReleaseError {
    UnsupportedTarget,
    UnsupportedProfile,
    UnsupportedFeatures,
    InvalidDigest(&'static str),
    InvalidField(&'static str),
}

fn valid_digest(value: &str) -> bool {
    value.len() == 64 && value.bytes().all(|byte| byte.is_ascii_hexdigit())
}

impl Matrix {
    pub fn validate(&self, product: &Product) -> Result<(), ReleaseError> {
        if !self.targets.contains(&product.target) {
            return Err(ReleaseError::UnsupportedTarget);
        }
        if !self.profiles.contains(&product.profile) {
            return Err(ReleaseError::UnsupportedProfile);
        }
        if !self.allowed_feature_sets.contains(&product.features) {
            return Err(ReleaseError::UnsupportedFeatures);
        }
        Ok(())
    }
}

pub fn render_manifest(matrix: &Matrix, artifact: &Artifact) -> Result<String, ReleaseError> {
    matrix.validate(&artifact.product)?;
    if artifact.name.is_empty() || artifact.name.contains('/') || artifact.name.contains('\\') {
        return Err(ReleaseError::InvalidField("artifact name"));
    }
    if !valid_digest(&artifact.lockfile_sha256) {
        return Err(ReleaseError::InvalidDigest("lockfile"));
    }
    if !valid_digest(&artifact.sha256) {
        return Err(ReleaseError::InvalidDigest("artifact"));
    }

    let features = artifact.product.features.iter().cloned().collect::<Vec<_>>().join(",");
    let fields = BTreeMap::from([
        ("artifact", artifact.name.clone()),
        ("artifact_sha256", artifact.sha256.clone()),
        ("features", features),
        ("lockfile_sha256", artifact.lockfile_sha256.clone()),
        ("profile", artifact.product.profile.clone()),
        ("size_bytes", artifact.size_bytes.to_string()),
        ("source_revision", artifact.source_revision.clone()),
        ("target", artifact.product.target.clone()),
        ("toolchain", artifact.toolchain.clone()),
        ("version", artifact.version.clone()),
    ]);

    Ok(fields
        .into_iter()
        .map(|(key, value)| format!("{key}={value}\n"))
        .collect())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn matrix() -> Matrix {
        Matrix {
            targets: BTreeSet::from(["x86_64-unknown-linux-gnu".into()]),
            profiles: BTreeSet::from(["dist".into()]),
            allowed_feature_sets: BTreeSet::from([BTreeSet::new()]),
        }
    }

    fn artifact() -> Artifact {
        Artifact {
            name: "metricrail".into(),
            version: "1.0.0".into(),
            source_revision: "abc123".into(),
            lockfile_sha256: "a".repeat(64),
            toolchain: "1.97.1".into(),
            product: Product {
                target: "x86_64-unknown-linux-gnu".into(),
                profile: "dist".into(),
                features: BTreeSet::new(),
            },
            size_bytes: 42,
            sha256: "b".repeat(64),
        }
    }

    #[test]
    fn manifest_is_deterministic_and_has_no_timestamp() {
        let first = render_manifest(&matrix(), &artifact()).expect("supported artifact");
        let second = render_manifest(&matrix(), &artifact()).expect("supported artifact");
        assert_eq!(first, second);
        assert!(!first.contains("timestamp"));
        assert!(first.starts_with("artifact=metricrail\n"));
    }

    #[test]
    fn unsupported_target_is_rejected() {
        let mut artifact = artifact();
        artifact.product.target = "unknown".into();
        assert_eq!(render_manifest(&matrix(), &artifact), Err(ReleaseError::UnsupportedTarget));
    }
}

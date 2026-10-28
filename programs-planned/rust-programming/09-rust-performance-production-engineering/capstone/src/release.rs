use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BuildInfo {
    pub package_version: &'static str,
    pub source_revision: &'static str,
    pub target: &'static str,
    pub profile: &'static str,
    pub toolchain: &'static str,
}

impl BuildInfo {
    pub fn current() -> Self {
        Self {
            package_version: env!("CARGO_PKG_VERSION"),
            source_revision: env!("METRICRAIL_SOURCE_REVISION"),
            target: env!("METRICRAIL_TARGET"),
            profile: env!("METRICRAIL_PROFILE"),
            toolchain: "1.97.1",
        }
    }

    pub fn render(&self) -> String {
        let fields = BTreeMap::from([
            ("package_version", self.package_version),
            ("profile", self.profile),
            ("source_revision", self.source_revision),
            ("target", self.target),
            ("toolchain", self.toolchain),
        ]);
        fields
            .into_iter()
            .map(|(key, value)| format!("{key}={value}\n"))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn metadata_is_sorted_and_has_no_wall_clock() {
        let info = BuildInfo {
            package_version: "1.0.0",
            source_revision: "abc",
            target: "x86_64",
            profile: "dist",
            toolchain: "1.97.1",
        };
        let rendered = info.render();
        assert!(rendered.starts_with("package_version=1.0.0\n"));
        assert!(!rendered.contains("timestamp"));
    }
}

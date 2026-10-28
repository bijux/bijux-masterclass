use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum Severity {
    Low,
    Medium,
    High,
    Critical,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Boundary {
    pub name: String,
    pub assets: BTreeSet<String>,
    pub untrusted_input: bool,
    pub privileged_operation: bool,
    pub controls: BTreeSet<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Dependency {
    pub name: String,
    pub exact_version: String,
    pub default_features: bool,
    pub has_build_script: bool,
    pub reviewed: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Finding {
    pub severity: Severity,
    pub subject: String,
    pub message: String,
}

fn looks_like_exact_version(value: &str) -> bool {
    let Some(version) = value.strip_prefix('=') else {
        return false;
    };
    let mut components = version.split('.');
    matches!(
        (components.next(), components.next(), components.next(), components.next()),
        (Some(major), Some(minor), Some(patch), None)
            if [major, minor, patch]
                .into_iter()
                .all(|part| !part.is_empty() && part.bytes().all(|byte| byte.is_ascii_digit()))
    )
}

pub fn review(boundaries: &[Boundary], dependencies: &[Dependency]) -> Vec<Finding> {
    let mut findings = Vec::new();
    let mut boundary_counts = BTreeMap::<&str, usize>::new();
    for boundary in boundaries {
        *boundary_counts.entry(boundary.name.as_str()).or_default() += 1;
    }
    for (name, count) in boundary_counts {
        if name.is_empty() || count > 1 {
            findings.push(Finding {
                severity: Severity::High,
                subject: if name.is_empty() {
                    "boundaries".into()
                } else {
                    name.into()
                },
                message: if name.is_empty() {
                    "boundary name must not be empty".into()
                } else {
                    "boundary name is duplicated".into()
                },
            });
        }
    }

    for boundary in boundaries {
        if boundary.untrusted_input && !boundary.controls.contains("size-limit") {
            findings.push(Finding {
                severity: Severity::Critical,
                subject: boundary.name.clone(),
                message: "untrusted input lacks a size limit".into(),
            });
        }
        if boundary.privileged_operation && !boundary.controls.contains("authorization") {
            findings.push(Finding {
                severity: Severity::Critical,
                subject: boundary.name.clone(),
                message: "privileged operation lacks authorization".into(),
            });
        }
        if boundary.assets.is_empty() {
            findings.push(Finding {
                severity: Severity::Medium,
                subject: boundary.name.clone(),
                message: "boundary names no protected assets".into(),
            });
        }
    }

    let mut dependency_counts = BTreeMap::<&str, usize>::new();
    for dependency in dependencies {
        *dependency_counts
            .entry(dependency.name.as_str())
            .or_default() += 1;
    }
    for (name, count) in dependency_counts {
        if name.is_empty() || count > 1 {
            findings.push(Finding {
                severity: Severity::High,
                subject: if name.is_empty() {
                    "dependencies".into()
                } else {
                    name.into()
                },
                message: if name.is_empty() {
                    "dependency name must not be empty".into()
                } else {
                    "dependency appears more than once".into()
                },
            });
        }
    }

    for dependency in dependencies {
        if !looks_like_exact_version(&dependency.exact_version) {
            findings.push(Finding {
                severity: Severity::High,
                subject: dependency.name.clone(),
                message: "dependency version is not an exact =major.minor.patch pin".into(),
            });
        }
        if dependency.has_build_script && !dependency.reviewed {
            findings.push(Finding {
                severity: Severity::High,
                subject: dependency.name.clone(),
                message: "build script has not been reviewed".into(),
            });
        }
        if dependency.default_features && !dependency.reviewed {
            findings.push(Finding {
                severity: Severity::Medium,
                subject: dependency.name.clone(),
                message: "default feature surface has not been reviewed".into(),
            });
        }
    }

    findings.sort_by(|left, right| {
        left.severity
            .cmp(&right.severity)
            .reverse()
            .then_with(|| left.subject.cmp(&right.subject))
            .then_with(|| left.message.cmp(&right.message))
    });
    findings
}

pub fn summarize(findings: &[Finding]) -> BTreeMap<Severity, usize> {
    let mut counts = BTreeMap::new();
    for finding in findings {
        *counts.entry(finding.severity.clone()).or_default() += 1;
    }
    counts
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unbounded_privileged_boundary_is_critical() {
        let boundary = Boundary {
            name: "admin".into(),
            assets: BTreeSet::from(["configuration".into()]),
            untrusted_input: true,
            privileged_operation: true,
            controls: BTreeSet::new(),
        };
        let findings = review(&[boundary], &[]);
        assert_eq!(
            summarize(&findings).get(&Severity::Critical),
            Some(&2)
        );
    }

    #[test]
    fn reviewed_boundary_and_dependency_are_clean() {
        let boundary = Boundary {
            name: "ingest".into(),
            assets: BTreeSet::from(["availability".into()]),
            untrusted_input: true,
            privileged_operation: false,
            controls: BTreeSet::from(["size-limit".into()]),
        };
        let dependency = Dependency {
            name: "bytes".into(),
            exact_version: "=1.12.1".into(),
            default_features: false,
            has_build_script: false,
            reviewed: true,
        };
        assert!(review(&[boundary], &[dependency]).is_empty());
    }

    #[test]
    fn range_version_is_not_an_exact_reviewed_input() {
        let dependency = Dependency {
            name: "example".into(),
            exact_version: "1".into(),
            default_features: false,
            has_build_script: false,
            reviewed: true,
        };
        let findings = review(&[], &[dependency]);
        assert!(findings
            .iter()
            .any(|finding| finding.message.contains("exact")));
    }
}

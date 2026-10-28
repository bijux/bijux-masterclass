use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Area {
    Correctness,
    Capacity,
    Observability,
    Reliability,
    Security,
    Release,
    Rollback,
    IncidentResponse,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Evidence {
    pub area: Area,
    pub description: String,
    pub reviewed_revision: String,
    pub current_revision: String,
    pub passed: bool,
}

impl Evidence {
    pub fn is_current(&self) -> bool {
        self.reviewed_revision == self.current_revision
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    Deploy,
    CanaryOnly,
    DoNotDeploy,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Capacity {
    pub active: usize,
    pub queued: usize,
    pub bytes_per_active: usize,
    pub bytes_per_queued: usize,
    pub fixed_bytes: usize,
}

impl Capacity {
    pub fn estimated_peak_bytes(&self) -> Option<usize> {
        self.active
            .checked_mul(self.bytes_per_active)?
            .checked_add(self.queued.checked_mul(self.bytes_per_queued)?)?
            .checked_add(self.fixed_bytes)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReviewError {
    CapacityArithmeticOverflow,
    ZeroCapacityBudget,
    DuplicateEvidence(Area),
    EmptyDescription(Area),
}

#[derive(Debug, PartialEq, Eq)]
pub struct Review {
    pub decision: Decision,
    pub missing: Vec<Area>,
    pub stale: Vec<Area>,
    pub failed: Vec<Area>,
    pub capacity_bytes: usize,
    pub capacity_exceeded: bool,
}

pub fn review(
    evidence: &[Evidence],
    capacity: Capacity,
    max_bytes: usize,
) -> Result<Review, ReviewError> {
    if max_bytes == 0 {
        return Err(ReviewError::ZeroCapacityBudget);
    }
    let capacity_bytes = capacity
        .estimated_peak_bytes()
        .ok_or(ReviewError::CapacityArithmeticOverflow)?;
    let mut by_area = BTreeMap::new();
    for item in evidence {
        if item.description.trim().is_empty() {
            return Err(ReviewError::EmptyDescription(item.area));
        }
        if by_area.insert(item.area, item).is_some() {
            return Err(ReviewError::DuplicateEvidence(item.area));
        }
    }

    let required = [
        Area::Correctness,
        Area::Capacity,
        Area::Observability,
        Area::Reliability,
        Area::Security,
        Area::Release,
        Area::Rollback,
        Area::IncidentResponse,
    ];

    let mut missing = Vec::new();
    let mut stale = Vec::new();
    let mut failed = Vec::new();
    for area in required {
        match by_area.get(&area) {
            None => missing.push(area),
            Some(item) if !item.passed => failed.push(area),
            Some(item) if !item.is_current() => stale.push(area),
            Some(_) => {}
        }
    }

    let capacity_exceeded = capacity_bytes > max_bytes;
    let decision = if !failed.is_empty() || !missing.is_empty() || capacity_exceeded {
        Decision::DoNotDeploy
    } else if !stale.is_empty() {
        Decision::CanaryOnly
    } else {
        Decision::Deploy
    };

    Ok(Review {
        decision,
        missing,
        stale,
        failed,
        capacity_bytes,
        capacity_exceeded,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn complete(revision: &str) -> Vec<Evidence> {
        [
            Area::Correctness,
            Area::Capacity,
            Area::Observability,
            Area::Reliability,
            Area::Security,
            Area::Release,
            Area::Rollback,
            Area::IncidentResponse,
        ]
        .into_iter()
        .map(|area| Evidence {
            area,
            description: format!("{area:?} reviewed"),
            reviewed_revision: revision.into(),
            current_revision: revision.into(),
            passed: true,
        })
        .collect()
    }

    fn small_capacity() -> Capacity {
        Capacity {
            active: 1,
            queued: 1,
            bytes_per_active: 1,
            bytes_per_queued: 1,
            fixed_bytes: 1,
        }
    }

    #[test]
    fn complete_current_evidence_and_capacity_allow_deploy() {
        let review = review(
            &complete("abc"),
            Capacity {
                active: 4,
                queued: 8,
                bytes_per_active: 1024,
                bytes_per_queued: 128,
                fixed_bytes: 2048,
            },
            16 * 1024,
        )
        .expect("valid arithmetic");
        assert_eq!(review.decision, Decision::Deploy);
        assert!(!review.capacity_exceeded);
    }

    #[test]
    fn stale_evidence_limits_rollout_to_canary() {
        let mut evidence = complete("abc");
        evidence[0].current_revision = "def".into();
        let review = review(&evidence, small_capacity(), 100).expect("valid arithmetic");
        assert_eq!(review.decision, Decision::CanaryOnly);
    }

    #[test]
    fn failed_evidence_blocks_even_when_it_is_stale() {
        let mut evidence = complete("abc");
        evidence[0].current_revision = "def".into();
        evidence[0].passed = false;
        let review = review(&evidence, small_capacity(), 100).expect("valid arithmetic");
        assert_eq!(review.decision, Decision::DoNotDeploy);
        assert_eq!(review.failed, vec![Area::Correctness]);
    }

    #[test]
    fn missing_security_blocks_deployment() {
        let mut evidence = complete("abc");
        evidence.retain(|item| item.area != Area::Security);
        let review = review(&evidence, small_capacity(), 100).expect("valid arithmetic");
        assert_eq!(review.decision, Decision::DoNotDeploy);
        assert_eq!(review.missing, vec![Area::Security]);
    }

    #[test]
    fn duplicate_evidence_is_rejected() {
        let mut evidence = complete("abc");
        evidence.push(evidence[0].clone());
        assert_eq!(
            review(&evidence, small_capacity(), 100),
            Err(ReviewError::DuplicateEvidence(Area::Correctness))
        );
    }
}

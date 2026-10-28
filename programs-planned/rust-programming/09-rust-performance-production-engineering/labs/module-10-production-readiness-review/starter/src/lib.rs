#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    Deploy,
    DoNotDeploy,
}

pub fn decide(tests_pass: bool, rollback_documented: bool) -> Decision {
    if tests_pass && rollback_documented {
        Decision::Deploy
    } else {
        Decision::DoNotDeploy
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn missing_rollback_blocks_deployment() {
        assert_eq!(decide(true, false), Decision::DoNotDeploy);
    }
}


#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AllocationError {
    InvalidAlignment(usize),
}

pub fn validate_alignment(alignment: usize) -> Result<(), AllocationError> {
    if alignment.is_power_of_two() {
        Ok(())
    } else {
        Err(AllocationError::InvalidAlignment(alignment))
    }
}

#[cfg(test)]
mod tests {
    use super::validate_alignment;

    #[test]
    fn alignment_contract_is_explicit() {
        assert!(validate_alignment(64).is_ok());
        assert!(validate_alignment(3).is_err());
        assert!(validate_alignment(0).is_err());
    }
}

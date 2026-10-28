#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Boundary {
    pub name: String,
    pub accepts_untrusted_input: bool,
}

pub fn untrusted_count(boundaries: &[Boundary]) -> usize {
    boundaries.iter().filter(|boundary| boundary.accepts_untrusted_input).count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn counts_untrusted_boundaries() {
        let boundaries = vec![
            Boundary { name: "tcp".into(), accepts_untrusted_input: true },
            Boundary { name: "internal".into(), accepts_untrusted_input: false },
        ];
        assert_eq!(untrusted_count(&boundaries), 1);
    }
}

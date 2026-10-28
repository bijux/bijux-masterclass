#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConfigV1 {
    pub path: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConfigV2 {
    pub path: String,
    pub verify_on_open: bool,
}

impl From<ConfigV1> for ConfigV2 {
    fn from(old: ConfigV1) -> Self {
        Self {
            path: old.path,
            verify_on_open: true,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_conversion_preserves_path() {
        let v2 = ConfigV2::from(ConfigV1 {
            path: "a.ax".into(),
        });
        assert_eq!(v2.path, "a.ax");
        assert!(v2.verify_on_open);
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConfigV1 {
    pub path: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConfigV2 {
    pub path: String,
    pub verify_on_open: bool,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Error {
    WrongHeader,
    MissingField(&'static str),
    DuplicateField(&'static str),
    InvalidField(&'static str),
    UnknownField(String),
}

pub fn decode_v1(input: &str) -> Result<ConfigV1, Error> {
    let mut lines = input.lines();
    if lines.next() != Some("V1") {
        return Err(Error::WrongHeader);
    }

    let mut path = None;
    for line in lines {
        let (name, value) = line
            .split_once('=')
            .ok_or(Error::InvalidField("line"))?;
        match name {
            "path" if path.is_none() => path = Some(value),
            "path" => return Err(Error::DuplicateField("path")),
            other => return Err(Error::UnknownField(other.to_owned())),
        }
    }

    let path = path.ok_or(Error::MissingField("path"))?;
    validate_path(path)?;
    Ok(ConfigV1 {
        path: path.to_owned(),
    })
}

pub fn encode_v2(config: &ConfigV2) -> Result<String, Error> {
    validate_path(&config.path)?;
    Ok(format!(
        "V2\npath={}\nverify={}\n",
        config.path, config.verify_on_open
    ))
}

pub fn decode_v2(input: &str) -> Result<ConfigV2, Error> {
    let mut lines = input.lines();
    if lines.next() != Some("V2") {
        return Err(Error::WrongHeader);
    }

    let mut path = None;
    let mut verify = None;
    for line in lines {
        let (name, value) = line
            .split_once('=')
            .ok_or(Error::InvalidField("line"))?;
        match name {
            "path" if path.is_none() => path = Some(value),
            "path" => return Err(Error::DuplicateField("path")),
            "verify" if verify.is_none() => verify = Some(value),
            "verify" => return Err(Error::DuplicateField("verify")),
            other => return Err(Error::UnknownField(other.to_owned())),
        }
    }

    let path = path.ok_or(Error::MissingField("path"))?;
    validate_path(path)?;
    let verify_on_open = match verify.ok_or(Error::MissingField("verify"))? {
        "true" => true,
        "false" => false,
        _ => return Err(Error::InvalidField("verify")),
    };

    Ok(ConfigV2 {
        path: path.to_owned(),
        verify_on_open,
    })
}

pub fn migrate(input: &str) -> Result<String, Error> {
    let old = decode_v1(input)?;
    let candidate = encode_v2(&ConfigV2 {
        path: old.path,
        verify_on_open: true,
    })?;
    decode_v2(&candidate)?;
    Ok(candidate)
}

fn validate_path(path: &str) -> Result<(), Error> {
    if path.is_empty() || path.contains('\n') || path.contains('\r') {
        Err(Error::InvalidField("path"))
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn migration_is_verified_and_canonical() {
        let output = migrate("V1\npath=data.ax\n").expect("valid migration");
        assert_eq!(output, "V2\npath=data.ax\nverify=true\n");
        assert_eq!(decode_v2(&output).expect("valid V2").path, "data.ax");
    }

    #[test]
    fn duplicate_fields_are_rejected() {
        assert_eq!(
            decode_v2("V2\npath=a\npath=b\nverify=true\n"),
            Err(Error::DuplicateField("path"))
        );
    }

    #[test]
    fn malformed_source_remains_an_error() {
        let source = "not-a-version\npath=data.ax\n";
        assert_eq!(migrate(source), Err(Error::WrongHeader));
        assert_eq!(source, "not-a-version\npath=data.ax\n");
    }
}

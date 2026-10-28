use std::collections::BTreeMap;
use std::fs::{self, File};
use std::io::{self, Write};
use std::path::Path;

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Row {
    pub(crate) name: String,
    pub(crate) code: u16,
    pub(crate) help: String,
}

pub(crate) fn parse(input: &str) -> Result<Vec<Row>, String> {
    let mut rows = Vec::new();
    let mut names: BTreeMap<String, usize> = BTreeMap::new();
    let mut codes: BTreeMap<u16, usize> = BTreeMap::new();

    for (index, line) in input.lines().enumerate() {
        let line_number = index + 1;
        if line.trim().is_empty() {
            continue;
        }
        let fields = line.split('\t').collect::<Vec<_>>();
        if fields.len() != 3 {
            return Err(format!(
                "line {line_number} must contain exactly three tab-separated fields"
            ));
        }

        let name = fields[0];
        let valid_name = !name.is_empty()
            && !name.as_bytes()[0].is_ascii_digit()
            && name
                .bytes()
                .all(|byte| byte.is_ascii_lowercase() || byte == b'_' || byte.is_ascii_digit());
        if !valid_name {
            return Err(format!("line {line_number} has invalid command name `{name}`"));
        }

        let code: u16 = fields[1]
            .parse()
            .map_err(|_| format!("line {line_number} has invalid code"))?;
        if code == 0 {
            return Err(format!("line {line_number} uses reserved zero code"));
        }
        if fields[2].is_empty() {
            return Err(format!("line {line_number} has empty help"));
        }

        if let Some(first) = names.get(name).copied() {
            return Err(format!(
                "line {line_number} duplicates command name `{name}` first declared on line {first}"
            ));
        }
        names.insert(name.to_owned(), line_number);

        if let Some(first) = codes.get(&code).copied() {
            return Err(format!(
                "line {line_number} duplicates code `{code}` first declared on line {first}"
            ));
        }
        codes.insert(code, line_number);

        rows.push(Row {
            name: name.to_owned(),
            code,
            help: fields[2].to_owned(),
        });
    }

    if rows.is_empty() {
        return Err("command schema must contain at least one row".to_owned());
    }
    Ok(rows)
}

fn rust_string(value: &str) -> String {
    format!("{value:?}")
}

pub(crate) fn render(rows: &[Row]) -> String {
    let mut output = String::from("pub const COMMANDS: &[GeneratedCommand] = &[\n");
    for row in rows {
        output.push_str(&format!(
            "    GeneratedCommand {{ name: {}, code: {}, help: {} }},\n",
            rust_string(&row.name),
            row.code,
            rust_string(&row.help),
        ));
    }
    output.push_str("];\n");
    output
}


pub(crate) fn write_generated(destination: &Path, contents: &str) -> io::Result<()> {
    let temporary = destination.with_extension("rs.tmp");
    let mut file = File::create(&temporary)?;
    file.write_all(contents.as_bytes())?;
    file.flush()?;
    file.sync_all()?;

    #[cfg(windows)]
    if destination.exists() {
        fs::remove_file(destination)?;
    }

    fs::rename(temporary, destination)
}

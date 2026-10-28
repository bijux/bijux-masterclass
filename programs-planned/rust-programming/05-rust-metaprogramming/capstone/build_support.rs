use std::collections::BTreeMap;
use std::fs::{self, File};
use std::io::{self, Write};
use std::path::Path;

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ExitCodeRow {
    pub(crate) name: String,
    pub(crate) code: i32,
    pub(crate) description: String,
}

pub(crate) fn parse(input: &str) -> Result<Vec<ExitCodeRow>, String> {
    let mut rows = Vec::new();
    let mut names: BTreeMap<String, usize> = BTreeMap::new();
    let mut codes: BTreeMap<i32, usize> = BTreeMap::new();

    for (index, line) in input.lines().enumerate() {
        let line_number = index + 1;
        if line.trim().is_empty() {
            continue;
        }

        let fields = line.split('\t').collect::<Vec<_>>();
        if fields.len() != 3 {
            return Err(format!(
                "line {line_number} must contain NAME, CODE, and DESCRIPTION separated by tabs"
            ));
        }

        let name = fields[0];
        let valid_name = !name.is_empty()
            && !name.as_bytes()[0].is_ascii_digit()
            && name
                .bytes()
                .all(|byte| byte.is_ascii_uppercase() || byte == b'_' || byte.is_ascii_digit());
        if !valid_name {
            return Err(format!(
                "line {line_number} has invalid exit-code name `{name}`"
            ));
        }

        let code: i32 = fields[1]
            .parse()
            .map_err(|_| format!("line {line_number} has invalid numeric code"))?;
        if !(0..=255).contains(&code) {
            return Err(format!(
                "line {line_number} has code `{code}` outside 0..=255"
            ));
        }

        let description = fields[2];
        if description.is_empty() {
            return Err(format!("line {line_number} has an empty description"));
        }

        if let Some(first_line) = names.get(name).copied() {
            return Err(format!(
                "line {line_number} duplicates name `{name}` first declared on line {first_line}"
            ));
        }
        names.insert(name.to_owned(), line_number);

        if let Some(first_line) = codes.get(&code).copied() {
            return Err(format!(
                "line {line_number} duplicates code `{code}` first declared on line {first_line}"
            ));
        }
        codes.insert(code, line_number);

        rows.push(ExitCodeRow {
            name: name.to_owned(),
            code,
            description: description.to_owned(),
        });
    }

    if rows.is_empty() {
        return Err("exit-code table must contain at least one row".to_owned());
    }

    Ok(rows)
}

fn rust_string(value: &str) -> String {
    format!("{value:?}")
}

pub(crate) fn render(rows: &[ExitCodeRow]) -> String {
    let mut output = String::from("pub const EXIT_CODES: &[ExitCodeRecord] = &[\n");
    for row in rows {
        output.push_str(&format!(
            "    ExitCodeRecord {{ name: {}, code: {}, description: {} }},\n",
            rust_string(&row.name),
            row.code,
            rust_string(&row.description),
        ));
    }
    output.push_str("];\n\n");

    for row in rows {
        output.push_str(&format!(
            "pub const EXIT_{}: i32 = {};\n",
            row.name, row.code
        ));
    }
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

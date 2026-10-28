use crate::{
    ParsePriorityError, ParseStatusError, ParseTaskIdError, Priority, Status, Task, TaskBoard,
    TaskError, TaskId,
};
use std::error::Error;
use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};
use std::process;
use std::time::{SystemTime, UNIX_EPOCH};

const HEADER: &str = "TASKBOARD-V1";
const NEXT_ID_TAG: &str = "NEXT_ID";
const TASK_TAG: &str = "TASK";
const EXHAUSTED: &str = "exhausted";

/// Failure to decode one non-header storage record.
#[derive(Debug)]
pub enum RecordError {
    /// Record tag was not recognized.
    UnknownTag(String),
    /// Record contained the wrong number of tab-separated fields.
    FieldCount {
        /// Record tag whose grammar was checked.
        tag: String,
        /// Required number of fields.
        expected: usize,
        /// Observed number of fields.
        found: usize,
    },
    /// `NEXT_ID` value was neither a nonzero integer nor `exhausted`.
    InvalidNextId(String),
    /// Task ID was invalid.
    InvalidTaskId(ParseTaskIdError),
    /// Task status was invalid.
    InvalidStatus(ParseStatusError),
    /// Task priority was invalid.
    InvalidPriority(ParsePriorityError),
    /// A restored task violated a domain invariant.
    InvalidTask(TaskError),
}

impl fmt::Display for RecordError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnknownTag(tag) => write!(formatter, "unknown record tag `{tag}`"),
            Self::FieldCount {
                tag,
                expected,
                found,
            } => write!(
                formatter,
                "record `{tag}` has {found} fields; expected {expected}"
            ),
            Self::InvalidNextId(value) => write!(
                formatter,
                "invalid NEXT_ID value `{value}`; expected a nonzero integer or exhausted"
            ),
            Self::InvalidTaskId(error) => error.fmt(formatter),
            Self::InvalidStatus(error) => error.fmt(formatter),
            Self::InvalidPriority(error) => error.fmt(formatter),
            Self::InvalidTask(error) => error.fmt(formatter),
        }
    }
}

impl Error for RecordError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::InvalidTaskId(error) => Some(error),
            Self::InvalidStatus(error) => Some(error),
            Self::InvalidPriority(error) => Some(error),
            Self::InvalidTask(error) => Some(error),
            _ => None,
        }
    }
}

/// Failure to read, validate, or commit the persistence protocol.
#[derive(Debug)]
pub enum StorageError {
    /// An I/O operation failed with contextual operation text.
    Io {
        /// Operation attempted when the error occurred.
        context: String,
        /// Original standard-library I/O error.
        source: io::Error,
    },
    /// Input contained no header line.
    EmptyInput,
    /// Header did not match the supported protocol version.
    InvalidHeader {
        /// Observed first line.
        found: String,
    },
    /// No `NEXT_ID` metadata record was present.
    MissingNextId,
    /// More than one `NEXT_ID` record was present.
    DuplicateNextId {
        /// One-based line number of the duplicate.
        line: usize,
    },
    /// One record failed to decode.
    InvalidRecord {
        /// One-based line number.
        line: usize,
        /// Record-specific failure.
        source: RecordError,
    },
    /// Decoded records contradicted aggregate domain invariants.
    InvalidSnapshot(TaskError),
}

impl StorageError {
    fn io(context: impl Into<String>, source: io::Error) -> Self {
        Self::Io {
            context: context.into(),
            source,
        }
    }
}

impl fmt::Display for StorageError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io { context, source } => write!(formatter, "{context}: {source}"),
            Self::EmptyInput => formatter.write_str("storage is empty; expected TASKBOARD-V1"),
            Self::InvalidHeader { found } => write!(
                formatter,
                "unsupported storage header `{found}`; expected {HEADER}"
            ),
            Self::MissingNextId => formatter.write_str("storage is missing NEXT_ID metadata"),
            Self::DuplicateNextId { line } => {
                write!(formatter, "line {line}: duplicate NEXT_ID record")
            }
            Self::InvalidRecord { line, source } => write!(formatter, "line {line}: {source}"),
            Self::InvalidSnapshot(error) => write!(formatter, "invalid storage snapshot: {error}"),
        }
    }
}

impl Error for StorageError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io { source, .. } => Some(source),
            Self::InvalidRecord { source, .. } => Some(source),
            Self::InvalidSnapshot(error) => Some(error),
            _ => None,
        }
    }
}

/// Decodes one complete board from a buffered or in-memory reader.
pub fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError> {
    let mut lines = reader.lines().enumerate();
    let (_, header_result) = lines.next().ok_or(StorageError::EmptyInput)?;
    let header = header_result.map_err(|error| StorageError::io("read storage header", error))?;
    if header != HEADER {
        return Err(StorageError::InvalidHeader { found: header });
    }

    let mut tasks = Vec::new();
    let mut next_id = None;
    let mut saw_next_id = false;

    for (zero_based, line_result) in lines {
        let line_number = zero_based + 1;
        let line = line_result.map_err(|error| {
            StorageError::io(format!("read storage line {line_number}"), error)
        })?;
        let fields: Vec<&str> = line.split('\t').collect();
        let tag = fields.first().copied().unwrap_or_default();

        match tag {
            NEXT_ID_TAG => {
                if saw_next_id {
                    return Err(StorageError::DuplicateNextId { line: line_number });
                }
                next_id = decode_next_id(&fields).map_err(|source| {
                    StorageError::InvalidRecord {
                        line: line_number,
                        source,
                    }
                })?;
                saw_next_id = true;
            }
            TASK_TAG => {
                let task = decode_task(&fields).map_err(|source| StorageError::InvalidRecord {
                    line: line_number,
                    source,
                })?;
                tasks.push(task);
            }
            _ => {
                return Err(StorageError::InvalidRecord {
                    line: line_number,
                    source: RecordError::UnknownTag(tag.to_owned()),
                });
            }
        }
    }

    if !saw_next_id {
        return Err(StorageError::MissingNextId);
    }

    TaskBoard::restore(tasks, next_id).map_err(StorageError::InvalidSnapshot)
}

/// Encodes one board to a writer in deterministic ascending-ID order.
pub fn save_to<W: Write>(writer: &mut W, board: &TaskBoard) -> Result<(), StorageError> {
    writeln!(writer, "{HEADER}")
        .map_err(|error| StorageError::io("write storage header", error))?;

    match board.next_id_token() {
        Some(next_id) => writeln!(writer, "{NEXT_ID_TAG}\t{next_id}"),
        None => writeln!(writer, "{NEXT_ID_TAG}\t{EXHAUSTED}"),
    }
    .map_err(|error| StorageError::io("write NEXT_ID metadata", error))?;

    let mut tasks: Vec<&Task> = board.tasks().iter().collect();
    tasks.sort_unstable_by_key(|task| task.id());
    for task in tasks {
        writeln!(
            writer,
            "{TASK_TAG}\t{}\t{}\t{}\t{}",
            task.id(),
            task.status(),
            task.priority(),
            task.title()
        )
        .map_err(|error| StorageError::io("write task record", error))?;
    }
    Ok(())
}

/// Loads a board from `path`; a missing path represents a new empty board.
pub fn load_path(path: &Path) -> Result<TaskBoard, StorageError> {
    let file = match File::open(path) {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(TaskBoard::new()),
        Err(error) => {
            return Err(StorageError::io(
                format!("open storage path `{}`", path.display()),
                error,
            ));
        }
    };
    load_from(BufReader::new(file))
}

/// Writes a board to a same-directory temporary file and commits it with rename.
pub fn save_path(path: &Path, board: &TaskBoard) -> Result<(), StorageError> {
    let (temporary_path, file) = create_temporary_file(path)?;
    let mut writer = BufWriter::new(file);

    let write_result = (|| {
        save_to(&mut writer, board)?;
        writer
            .flush()
            .map_err(|error| StorageError::io("flush temporary storage", error))?;
        writer
            .get_ref()
            .sync_all()
            .map_err(|error| StorageError::io("synchronize temporary storage", error))?;
        Ok::<(), StorageError>(())
    })();

    if let Err(error) = write_result {
        drop(writer);
        let _ignored = fs::remove_file(&temporary_path);
        return Err(error);
    }
    drop(writer);

    if let Err(error) = fs::rename(&temporary_path, path) {
        let _ignored = fs::remove_file(&temporary_path);
        return Err(StorageError::io(
            format!(
                "commit temporary storage `{}` to `{}`",
                temporary_path.display(),
                path.display()
            ),
            error,
        ));
    }
    Ok(())
}

fn decode_next_id(fields: &[&str]) -> Result<Option<u64>, RecordError> {
    if fields.len() != 2 {
        return Err(RecordError::FieldCount {
            tag: NEXT_ID_TAG.to_owned(),
            expected: 2,
            found: fields.len(),
        });
    }
    if fields[1] == EXHAUSTED {
        return Ok(None);
    }
    fields[1]
        .parse::<u64>()
        .ok()
        .filter(|value| *value != 0)
        .map(Some)
        .ok_or_else(|| RecordError::InvalidNextId(fields[1].to_owned()))
}

fn decode_task(fields: &[&str]) -> Result<Task, RecordError> {
    if fields.len() != 5 {
        return Err(RecordError::FieldCount {
            tag: TASK_TAG.to_owned(),
            expected: 5,
            found: fields.len(),
        });
    }
    let id = fields[1]
        .parse::<TaskId>()
        .map_err(RecordError::InvalidTaskId)?;
    let status = fields[2]
        .parse::<Status>()
        .map_err(RecordError::InvalidStatus)?;
    let priority = fields[3]
        .parse::<Priority>()
        .map_err(RecordError::InvalidPriority)?;
    Task::restore(id, fields[4].to_owned(), priority, status).map_err(RecordError::InvalidTask)
}

fn create_temporary_file(path: &Path) -> Result<(PathBuf, File), StorageError> {
    let parent = path.parent().unwrap_or_else(|| Path::new("."));
    let file_name = path
        .file_name()
        .map_or_else(|| String::from("taskboard"), |name| name.to_string_lossy().into_owned());
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0_u128, |duration| duration.as_nanos());

    for attempt in 0_u8..32 {
        let candidate = parent.join(format!(
            ".{file_name}.tmp.{}.{}.{}",
            process::id(),
            timestamp,
            attempt
        ));
        match OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&candidate)
        {
            Ok(file) => return Ok((candidate, file)),
            Err(error) if error.kind() == io::ErrorKind::AlreadyExists => {}
            Err(error) => {
                return Err(StorageError::io(
                    format!("create temporary storage `{}`", candidate.display()),
                    error,
                ));
            }
        }
    }

    Err(StorageError::io(
        format!("allocate temporary storage beside `{}`", path.display()),
        io::Error::new(
            io::ErrorKind::AlreadyExists,
            "temporary filename attempts exhausted",
        ),
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    fn text(bytes: Vec<u8>) -> String {
        String::from_utf8(bytes).expect("storage output is UTF-8")
    }

    #[test]
    fn empty_board_has_version_and_next_id_metadata() {
        let mut output = Vec::new();
        save_to(&mut output, &TaskBoard::new()).expect("memory write succeeds");
        assert_eq!(text(output), "TASKBOARD-V1\nNEXT_ID\t1\n");
    }

    #[test]
    fn round_trip_preserves_values_and_emits_id_order() {
        let input = concat!(
            "TASKBOARD-V1\n",
            "NEXT_ID\t4\n",
            "TASK\t3\tdone\tlow\tThird\n",
            "TASK\t1\tdoing\thigh\tFirst\n",
        );
        let board = load_from(Cursor::new(input)).expect("valid storage");
        assert_eq!(
            board.tasks().iter().map(Task::id).collect::<Vec<_>>(),
            vec![TaskId::new(1).expect("nonzero"), TaskId::new(3).expect("nonzero")]
        );

        let mut output = Vec::new();
        save_to(&mut output, &board).expect("memory write succeeds");
        assert_eq!(
            text(output),
            concat!(
                "TASKBOARD-V1\n",
                "NEXT_ID\t4\n",
                "TASK\t1\tdoing\thigh\tFirst\n",
                "TASK\t3\tdone\tlow\tThird\n",
            )
        );
    }

    #[test]
    fn malformed_records_include_one_based_line_numbers() {
        let error = load_from(Cursor::new(concat!(
            "TASKBOARD-V1\n",
            "NEXT_ID\t2\n",
            "TASK\t1\tflying\thigh\tBroken\n",
        )))
        .expect_err("invalid status must fail");
        assert!(error.to_string().contains("line 3"));
        assert!(error.to_string().contains("invalid status"));
    }

    #[test]
    fn loader_rejects_missing_duplicate_and_inconsistent_metadata() {
        assert!(matches!(
            load_from(Cursor::new("TASKBOARD-V1\n")),
            Err(StorageError::MissingNextId)
        ));
        assert!(matches!(
            load_from(Cursor::new("TASKBOARD-V1\nNEXT_ID\t1\nNEXT_ID\t1\n")),
            Err(StorageError::DuplicateNextId { line: 3 })
        ));
        assert!(matches!(
            load_from(Cursor::new(
                "TASKBOARD-V1\nNEXT_ID\t1\nTASK\t1\ttodo\tlow\tTask\n"
            )),
            Err(StorageError::InvalidSnapshot(TaskError::InvalidNextId))
        ));
    }

    #[test]
    fn loader_rejects_blank_and_unknown_records() {
        assert!(matches!(
            load_from(Cursor::new("TASKBOARD-V1\nNEXT_ID\t1\n\n")),
            Err(StorageError::InvalidRecord {
                source: RecordError::UnknownTag(_),
                ..
            })
        ));
        assert!(matches!(
            load_from(Cursor::new("OTHER\nNEXT_ID\t1\n")),
            Err(StorageError::InvalidHeader { .. })
        ));
    }
}

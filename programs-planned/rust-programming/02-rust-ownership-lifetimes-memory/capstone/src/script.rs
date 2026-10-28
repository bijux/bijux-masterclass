use crate::{
    DocumentHandle, DocumentSnapshot, SnapshotWatcher, Workspace, WorkspaceError,
};
use std::collections::HashMap;
use std::fmt;
use std::rc::Rc;
/// Executes the capstone's deterministic tab-separated command language.
#[derive(Debug)]
pub struct ScriptEngine {
    workspace: Workspace,
    documents: HashMap<String, DocumentHandle>,
    snapshots: HashMap<String, Rc<DocumentSnapshot>>,
    watchers: HashMap<String, SnapshotWatcher>,
}
/// A structural or domain failure while parsing or executing a script.
#[derive(Debug)]
pub enum ScriptError {
    /// An alias field was empty.
    EmptyAlias,
    /// An alias collided with an existing document, snapshot, or watcher alias.
    DuplicateAlias(String),
    /// A document alias was not defined.
    UnknownDocument(String),
    /// A snapshot alias was not defined.
    UnknownSnapshot(String),
    /// A watcher alias was not defined.
    UnknownWatcher(String),
    /// A command contained the wrong number of tab-separated fields.
    InvalidArity {
        /// Parsed command name.
        command: String,
        /// Published command grammar.
        expected: &'static str,
        /// Number of fields actually received.
        actual: usize,
    },
    /// A revision field was not a valid `u64`.
    InvalidRevision(String),
    /// A command name was not recognized.
    UnknownCommand(String),
    /// A workspace operation failed.
    Workspace(WorkspaceError),
    /// A script failure annotated with its one-based source line.
    AtLine {
        /// One-based script line.
        line: usize,
        /// Underlying error.
        source: Box<ScriptError>,
    },
}
impl fmt::Display for ScriptError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyAlias => write!(formatter, "alias must not be empty"),
            Self::DuplicateAlias(alias) => write!(formatter, "alias {alias:?} already exists"),
            Self::UnknownDocument(alias) => {
                write!(formatter, "unknown document alias {alias:?}")
            }
            Self::UnknownSnapshot(alias) => {
                write!(formatter, "unknown snapshot alias {alias:?}")
            }
            Self::UnknownWatcher(alias) => {
                write!(formatter, "unknown watcher alias {alias:?}")
            }
            Self::InvalidArity {
                command,
                expected,
                actual,
            }
            => write!(
            formatter,
            "{command} expects {expected}; received {actual} fields"
            ),
            Self::InvalidRevision(value) => write!(formatter, "invalid revision {value:?}"),
            Self::UnknownCommand(command) => {
                write!(formatter, "unknown script command {command:?}")
            }
            Self::Workspace(error) => error.fmt(formatter),
            Self::AtLine {
                line, source
            }
            => write!(formatter, "line {line}: {source}"),
        }
    }
}
impl std::error::Error for ScriptError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Workspace(error) => Some(error),
            Self::AtLine {
                source, ..
            }
            => Some(source.as_ref()),
            _ => None,
        }
    }
}
impl From<WorkspaceError> for ScriptError {
    fn from(error: WorkspaceError) -> Self {
        Self::Workspace(error)
    }
}
impl Default for ScriptEngine {
    fn default() -> Self {
        Self {
            workspace: Workspace::new(),
            documents: HashMap::new(),
            snapshots: HashMap::new(),
            watchers: HashMap::new(),
        }
    }
}
impl ScriptEngine {
    /// Create an engine with an empty workspace and alias tables.
    pub fn new() -> Self {
        Self::default()
    }
    /// Borrow the underlying workspace for inspection.
    pub fn workspace(&self) -> &Workspace {
        &self.workspace
    }
    /// Execute a complete script, attaching one-based line context to failures.
    pub fn execute(&mut self, script: &str) -> Result<Vec<String>, ScriptError> {
        let mut output = Vec::new();
        for (line_index, raw) in script.lines().enumerate() {
            let line = raw.trim_end();
            if line.trim().is_empty() || line.trim_start().starts_with('#') {
                continue;
            }
            let line_output = self
            .execute_line(line)
            .map_err(|source| ScriptError::AtLine {
                line: line_index + 1,
                source: Box::new(source),
            })?;
            output.extend(line_output);
        }
        Ok(output)
    }
    /// Execute exactly one tab-separated command.
    pub fn execute_line(&mut self, line: &str) -> Result<Vec<String>, ScriptError> {
        let fields = line.split('\t').collect::<Vec<_>>();
        let command = fields
        .first()
        .copied()
        .unwrap_or("")
        .trim()
        .to_ascii_uppercase();
        match command.as_str() {
            "ADD" => self.add(&fields),
            "SHOW" => self.show(&fields),
            "EDIT" => self.edit(&fields),
            "RENAME" => self.rename(&fields),
            "TAG" => self.tag(&fields),
            "SEARCH" => self.search(&fields),
            "SNAPSHOT" => self.snapshot(&fields),
            "WATCH" => self.watch(&fields),
            "DROP-SNAPSHOT" => self.drop_snapshot(&fields),
            "EVICT" => self.evict(&fields),
            "CHECK-WATCH" => self.check_watch(&fields),
            "REMOVE" => self.remove(&fields),
            "MEMORY" => self.memory(&fields),
            "LIST" => self.list(&fields),
            _ => Err(ScriptError::UnknownCommand(command)),
        }
    }
    fn add(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 4, "ADD<TAB>alias<TAB>title<TAB>text")?;
        self.ensure_new_alias(fields[1])?;
        let handle = self.workspace.add(fields[2], fields[3])?;
        self.documents.insert(fields[1].to_owned(), handle);
        Ok(vec![format!("ADDED\t{}\t{handle}", fields[1])])
    }
    fn show(&self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 2, "SHOW<TAB>document-alias")?;
        let handle = self.document(fields[1])?;
        let view = self.workspace.view(handle)?;
        Ok(vec![format!(
        "DOCUMENT\t{}\trev={}\ttitle={}\ttext={}\ttags={}",
        handle,
        view.revision(),
        view.title(),
        view.text(),
        view.tags().join(",")
        )])
    }
    fn edit(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(
        fields,
        4,
        "EDIT<TAB>document-alias<TAB>expected-revision<TAB>replacement-text",
        )?;
        let handle = self.document(fields[1])?;
        let expected = revision(fields[2])?;
        let mut session = self.workspace.begin_edit(handle)?;
        ensure_revision(handle, expected, session.expected_revision())?;
        session.set_text(fields[3]);
        let receipt = self
        .workspace
        .commit(session)
        .map_err(|failure| ScriptError::Workspace(failure.error))?;
        Ok(vec![format!(
        "EDITED\t{}\trev={}",
        fields[1], receipt.revision
        )])
    }
    fn rename(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(
        fields,
        4,
        "RENAME<TAB>document-alias<TAB>expected-revision<TAB>title",
        )?;
        let handle = self.document(fields[1])?;
        let expected = revision(fields[2])?;
        let mut session = self.workspace.begin_edit(handle)?;
        ensure_revision(handle, expected, session.expected_revision())?;
        session.set_title(fields[3]);
        let receipt = self
        .workspace
        .commit(session)
        .map_err(|failure| ScriptError::Workspace(failure.error))?;
        Ok(vec![format!(
        "RENAMED\t{}\trev={}",
        fields[1], receipt.revision
        )])
    }
    fn tag(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(
        fields,
        4,
        "TAG<TAB>document-alias<TAB>expected-revision<TAB>tag",
        )?;
        let handle = self.document(fields[1])?;
        let expected = revision(fields[2])?;
        let mut session = self.workspace.begin_edit(handle)?;
        ensure_revision(handle, expected, session.expected_revision())?;
        session.add_tag(fields[3]);
        let receipt = self
        .workspace
        .commit(session)
        .map_err(|failure| ScriptError::Workspace(failure.error))?;
        Ok(vec![format!(
        "TAGGED\t{}\trev={}",
        fields[1], receipt.revision
        )])
    }
    fn search(&self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 2, "SEARCH<TAB>query")?;
        Ok(self
        .workspace
        .search(fields[1])
        .into_iter()
        .map(|item| {
            format!(
            "MATCH\t{}\trev={}\tline={}\trange={}..{}\t{}",
            item.handle,
            item.revision,
            item.line
            .map_or_else(|| "?".to_owned(), |line| (line + 1).to_string()),
            item.range.start,
            item.range.end,
            item.matched
            )
        })
        .collect())
    }
    fn snapshot(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(
        fields,
        3,
        "SNAPSHOT<TAB>snapshot-alias<TAB>document-alias",
        )?;
        self.ensure_new_alias(fields[1])?;
        let handle = self.document(fields[2])?;
        let snapshot = self.workspace.snapshot(handle)?;
        let key = snapshot.key();
        self.snapshots.insert(fields[1].to_owned(), snapshot);
        Ok(vec![format!(
        "SNAPSHOT\t{}\t{}\trev={}",
        fields[1], key.handle, key.revision
        )])
    }
    fn watch(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(
        fields,
        3,
        "WATCH<TAB>watcher-alias<TAB>snapshot-alias",
        )?;
        self.ensure_new_alias(fields[1])?;
        let snapshot = self
        .snapshots
        .get(fields[2])
        .ok_or_else(|| ScriptError::UnknownSnapshot(fields[2].to_owned()))?;
        self.watchers
        .insert(fields[1].to_owned(), SnapshotWatcher::new(snapshot));
        Ok(vec![format!("WATCHING\t{}\t{}", fields[1], fields[2])])
    }
    fn drop_snapshot(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 2, "DROP-SNAPSHOT<TAB>snapshot-alias")?;
        self.snapshots
        .remove(fields[1])
        .ok_or_else(|| ScriptError::UnknownSnapshot(fields[1].to_owned()))?;
        Ok(vec![format!("DROPPED-SNAPSHOT\t{}", fields[1])])
    }
    fn evict(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 3, "EVICT<TAB>document-alias<TAB>revision")?;
        let handle = self.document(fields[1])?;
        let revision = revision(fields[2])?;
        let removed = self
        .workspace
        .evict_snapshot(crate::SnapshotKey {
            handle, revision
        });
        Ok(vec![format!(
        "EVICTED\t{}\trev={}\t{}",
        fields[1], revision, removed
        )])
    }
    fn check_watch(&self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 2, "CHECK-WATCH<TAB>watcher-alias")?;
        let watcher = self
        .watchers
        .get(fields[1])
        .ok_or_else(|| ScriptError::UnknownWatcher(fields[1].to_owned()))?;
        Ok(vec![format!(
        "WATCH\t{}\t{}",
        fields[1],
        if watcher.upgrade().is_some() {
            "alive"
        }
        else {
            "expired"
        }
        )])
    }
    fn remove(&mut self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 2, "REMOVE<TAB>document-alias")?;
        let handle = self.document(fields[1])?;
        let removed = self.workspace.remove(handle)?;
        self.documents.remove(fields[1]);
        Ok(vec![format!(
        "REMOVED\t{}\trev={}\t{}",
        fields[1], removed.revision, removed.title
        )])
    }
    fn memory(&self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 1, "MEMORY")?;
        let report = self.workspace.memory_report();
        Ok(vec![format!(
        "MEMORY\tdocuments={}\ttext-bytes={}\tcapacity-bytes={}\tsnapshots={}/{}\tunique-snapshots={}",
        report.live_documents,
        report.text_payload_bytes,
        report.live_string_capacity_bytes,
        report.snapshot_cache_entries,
        report.snapshot_retention_limit,
        report.unique_snapshot_allocations
        )])
    }
    fn list(&self, fields: &[&str]) -> Result<Vec<String>, ScriptError> {
        require(fields, 1, "LIST")?;
        Ok(self
        .workspace
        .handles()
        .into_iter()
        .map(|handle| format!("HANDLE\t{handle}"))
        .collect())
    }
    fn document(&self, alias: &str) -> Result<DocumentHandle, ScriptError> {
        self.documents
        .get(alias)
        .copied()
        .ok_or_else(|| ScriptError::UnknownDocument(alias.to_owned()))
    }
    fn ensure_new_alias(&self, alias: &str) -> Result<(), ScriptError> {
        if alias.is_empty() {
            return Err(ScriptError::EmptyAlias);
        }
        if self.documents.contains_key(alias)
        || self.snapshots.contains_key(alias)
        || self.watchers.contains_key(alias)
        {
            return Err(ScriptError::DuplicateAlias(alias.to_owned()));
        }
        Ok(())
    }
}
fn require(
fields: &[&str],
expected: usize,
syntax: &'static str,
) -> Result<(), ScriptError> {
    if fields.len() == expected {
        Ok(())
    }
    else {
        Err(ScriptError::InvalidArity {
            command: fields.first().copied().unwrap_or("").to_owned(),
            expected: syntax,
            actual: fields.len(),
        })
    }
}
fn revision(value: &str) -> Result<u64, ScriptError> {
    value
    .parse()
    .map_err(|_| ScriptError::InvalidRevision(value.to_owned()))
}
fn ensure_revision(
handle: DocumentHandle,
expected: u64,
actual: u64,
) -> Result<(), ScriptError> {
    if expected == actual {
        Ok(())
    }
    else {
        Err(ScriptError::Workspace(WorkspaceError::RevisionConflict {
            handle,
            expected,
            actual,
        }))
    }
}

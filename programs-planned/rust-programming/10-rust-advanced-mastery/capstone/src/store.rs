use std::{
    collections::BTreeMap,
    fs::{self, File, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
};

#[cfg(unix)]
use std::sync::atomic::{AtomicU64, Ordering};

use crate::{
    domain::validate_key, format, InlineBatch, MaxValueBytes, Record, ReservedPrefix,
    Snapshot, StoreError, Validator, ValidatorRegistry,
};

#[cfg(unix)]
static TEMP_SEQUENCE: AtomicU64 = AtomicU64::new(0);

#[derive(Clone, Debug, PartialEq, Eq)]
enum Operation {
    Put(Record),
    Remove(String),
    Clear,
}

pub struct Store<const MAX_RECORD: usize = 4096, const TX_CAP: usize = 32> {
    path: PathBuf,
    validators: ValidatorRegistry,
}

impl<const MAX_RECORD: usize, const TX_CAP: usize> Store<MAX_RECORD, TX_CAP> {
    pub fn new(path: impl Into<PathBuf>) -> Result<Self, StoreError> {
        let mut validators = ValidatorRegistry::default();
        validators.register(MaxValueBytes(MAX_RECORD.saturating_sub(8)))?;
        validators.register(ReservedPrefix("__axiom_"))?;
        Ok(Self {
            path: path.into(),
            validators,
        })
    }

    pub fn path(&self) -> &Path {
        &self.path
    }

    pub fn register_validator<V>(&mut self, validator: V) -> Result<(), StoreError>
    where
        V: Validator + 'static,
    {
        self.validators.register(validator)
    }

    pub fn validator_names(&self) -> impl Iterator<Item = &'static str> + '_ {
        self.validators.names()
    }

    pub fn init(&self) -> Result<Snapshot<MAX_RECORD>, StoreError> {
        self.initialize_records(Vec::new())
    }

    pub fn open_snapshot(&self) -> Result<Snapshot<MAX_RECORD>, StoreError> {
        let bytes = fs::read(&self.path)
            .map_err(|source| StoreError::io("read archive", &self.path, source))?;
        Snapshot::from_bytes(bytes)
    }

    pub fn transaction(&self) -> Transaction<'_, MAX_RECORD, TX_CAP> {
        Transaction {
            store: self,
            operations: InlineBatch::new(),
        }
    }

    pub fn put(&self, record: Record) -> Result<Snapshot<MAX_RECORD>, StoreError> {
        let mut transaction = self.transaction();
        transaction.put(record)?;
        transaction.commit()
    }

    pub(crate) fn initialize_records(
        &self,
        records: Vec<Record>,
    ) -> Result<Snapshot<MAX_RECORD>, StoreError> {
        let bytes = self.prepare_records(records)?;
        let snapshot = Snapshot::from_bytes(bytes)?;
        write_new(&self.path, snapshot.bytes())?;
        Ok(snapshot)
    }

    pub(crate) fn replace_records(
        &self,
        records: Vec<Record>,
    ) -> Result<Snapshot<MAX_RECORD>, StoreError> {
        let bytes = self.prepare_records(records)?;
        let snapshot = Snapshot::from_bytes(bytes)?;
        write_atomic(&self.path, snapshot.bytes())?;
        Ok(snapshot)
    }

    fn prepare_records(&self, mut records: Vec<Record>) -> Result<Vec<u8>, StoreError> {
        records.sort_by(|left, right| left.key().cmp(right.key()));
        let mut previous: Option<&str> = None;
        for record in &records {
            self.validators.validate(record)?;
            if previous == Some(record.key()) {
                return Err(StoreError::DuplicateKey(record.key().to_owned()));
            }
            previous = Some(record.key());
        }

        format::encode_archive::<MAX_RECORD>(&records)
    }
}

pub struct Transaction<'store, const MAX_RECORD: usize, const TX_CAP: usize> {
    store: &'store Store<MAX_RECORD, TX_CAP>,
    operations: InlineBatch<Operation, TX_CAP>,
}

impl<const MAX_RECORD: usize, const TX_CAP: usize> Transaction<'_, MAX_RECORD, TX_CAP> {
    pub fn len(&self) -> usize {
        self.operations.len()
    }

    pub fn is_empty(&self) -> bool {
        self.operations.is_empty()
    }

    pub fn put(&mut self, record: Record) -> Result<(), StoreError> {
        self.push(Operation::Put(record))
    }

    pub fn remove(&mut self, key: impl Into<String>) -> Result<(), StoreError> {
        let key = key.into();
        validate_key(&key)?;
        self.push(Operation::Remove(key))
    }

    pub fn clear(&mut self) -> Result<(), StoreError> {
        self.push(Operation::Clear)
    }

    pub fn commit(self) -> Result<Snapshot<MAX_RECORD>, StoreError> {
        let current = self.store.open_snapshot()?;
        let mut candidate: BTreeMap<String, Record> =
            format::decode_owned::<MAX_RECORD>(current.bytes())?
                .into_iter()
                .map(|record| (record.key().to_owned(), record))
                .collect();

        for operation in self.operations.as_slice() {
            match operation {
                Operation::Put(record) => {
                    candidate.insert(record.key().to_owned(), record.clone());
                }
                Operation::Remove(key) => {
                    candidate.remove(key);
                }
                Operation::Clear => candidate.clear(),
            }
        }

        self.store
            .replace_records(candidate.into_values().collect())
    }

    fn push(&mut self, operation: Operation) -> Result<(), StoreError> {
        self.operations
            .push(operation)
            .map_err(|_| StoreError::Capacity { limit: TX_CAP })
    }
}

fn write_new(path: &Path, bytes: &[u8]) -> Result<(), StoreError> {
    let parent = parent_directory(path)?;
    fs::create_dir_all(parent)
        .map_err(|source| StoreError::io("create parent directory", parent, source))?;

    let mut file = match OpenOptions::new().write(true).create_new(true).open(path) {
        Ok(file) => file,
        Err(source) if source.kind() == std::io::ErrorKind::AlreadyExists => {
            return Err(StoreError::DestinationExists(path.to_owned()));
        }
        Err(source) => return Err(StoreError::io("create archive", path, source)),
    };

    let result = write_and_sync(
        &mut file,
        path,
        bytes,
        "write archive",
        "flush archive",
        "synchronize archive",
    );
    drop(file);

    if let Err(error) = result {
        let _ = fs::remove_file(path);
        return Err(error);
    }

    sync_parent_directory(parent).map_err(|source| StoreError::Durability {
        path: path.to_owned(),
        source,
    })
}

#[cfg(unix)]
fn write_atomic(path: &Path, bytes: &[u8]) -> Result<(), StoreError> {
    let parent = parent_directory(path)?;
    fs::create_dir_all(parent)
        .map_err(|source| StoreError::io("create parent directory", parent, source))?;
    let file_name = path
        .file_name()
        .ok_or_else(|| StoreError::Usage("archive path has no file name".into()))?;
    let (temporary, mut file) = create_temporary(parent, file_name)?;

    let write_result = write_and_sync(
        &mut file,
        &temporary,
        bytes,
        "write temporary archive",
        "flush temporary archive",
        "synchronize temporary archive",
    );
    drop(file);

    if let Err(error) = write_result {
        let _ = fs::remove_file(&temporary);
        return Err(error);
    }

    if let Err(source) = fs::rename(&temporary, path) {
        let _ = fs::remove_file(&temporary);
        return Err(StoreError::io("replace archive", path, source));
    }

    sync_parent_directory(parent).map_err(|source| StoreError::Durability {
        path: path.to_owned(),
        source,
    })
}

#[cfg(unix)]
fn create_temporary(
    parent: &Path,
    file_name: &std::ffi::OsStr,
) -> Result<(PathBuf, File), StoreError> {
    const ATTEMPTS: usize = 128;
    let mut last_path = None;

    for _ in 0..ATTEMPTS {
        let sequence = TEMP_SEQUENCE.fetch_add(1, Ordering::Relaxed);
        let candidate = parent.join(format!(
            ".{}.{}.{}.tmp",
            file_name.to_string_lossy(),
            std::process::id(),
            sequence
        ));
        last_path = Some(candidate.clone());
        match OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&candidate)
        {
            Ok(file) => return Ok((candidate, file)),
            Err(source) if source.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(source) => {
                return Err(StoreError::io(
                    "create temporary archive",
                    &candidate,
                    source,
                ));
            }
        }
    }

    let last_path = last_path.unwrap_or_else(|| parent.join(".axiomstore.tmp"));
    Err(StoreError::io(
        "create temporary archive",
        &last_path,
        std::io::Error::new(
            std::io::ErrorKind::AlreadyExists,
            "temporary archive name space exhausted",
        ),
    ))
}

#[cfg(not(unix))]
fn write_atomic(_path: &Path, _bytes: &[u8]) -> Result<(), StoreError> {
    Err(StoreError::UnsupportedPlatform(
        "AxiomStore replacement commits require Unix rename-overwrite semantics in the reference implementation",
    ))
}

fn write_and_sync(
    file: &mut File,
    path: &Path,
    bytes: &[u8],
    write_operation: &'static str,
    flush_operation: &'static str,
    sync_operation: &'static str,
) -> Result<(), StoreError> {
    file.write_all(bytes)
        .map_err(|source| StoreError::io(write_operation, path, source))?;
    file.flush()
        .map_err(|source| StoreError::io(flush_operation, path, source))?;
    file.sync_all()
        .map_err(|source| StoreError::io(sync_operation, path, source))
}

fn parent_directory(path: &Path) -> Result<&Path, StoreError> {
    path.file_name()
        .ok_or_else(|| StoreError::Usage("archive path has no file name".into()))?;
    Ok(path
        .parent()
        .filter(|parent| !parent.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new(".")))
}

#[cfg(unix)]
fn sync_parent_directory(parent: &Path) -> std::io::Result<()> {
    File::open(parent)?.sync_all()
}

#[cfg(not(unix))]
fn sync_parent_directory(_parent: &Path) -> std::io::Result<()> {
    Ok(())
}

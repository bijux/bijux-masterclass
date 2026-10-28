
#![forbid(unsafe_code)]

use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LogicalPath {
    components: Vec<String>,
}

#[derive(Debug)]
pub enum PathError {
    Empty,
    Absolute,
    Backslash,
    DriveMarker,
    TooLong,
    TooManyComponents,
    EmptyComponent { index: usize },
    Dot { index: usize },
    Parent { index: usize },
    ControlCharacter { index: usize },
    ExistingSymlink { path: PathBuf },
    ExistingNonDirectory { path: PathBuf },
    DestinationExists { path: PathBuf },
    Io {
        operation: &'static str,
        path: PathBuf,
        source: io::Error,
    },
}

impl fmt::Display for PathError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for PathError {}

impl LogicalPath {
    pub fn parse(input: &str) -> Result<Self, PathError> {
        if input.is_empty() {
            return Err(PathError::Empty);
        }
        if input.starts_with('/') || input.starts_with('\\') {
            return Err(PathError::Absolute);
        }
        if input.contains('\\') {
            return Err(PathError::Backslash);
        }
        if input.contains(':') {
            return Err(PathError::DriveMarker);
        }
        if input.len() > 1024 {
            return Err(PathError::TooLong);
        }

        let mut components = Vec::new();
        for (index, part) in input.split('/').enumerate() {
            if index >= 32 {
                return Err(PathError::TooManyComponents);
            }
            if part.is_empty() {
                return Err(PathError::EmptyComponent { index });
            }
            if part == "." {
                return Err(PathError::Dot { index });
            }
            if part == ".." {
                return Err(PathError::Parent { index });
            }
            if part.chars().any(|ch| ch == '\0' || ch.is_control()) {
                return Err(PathError::ControlCharacter { index });
            }
            components.push(part.to_owned());
        }
        Ok(Self { components })
    }

    #[must_use]
    pub fn as_archive_name(&self) -> String {
        self.components.join("/")
    }

    #[must_use]
    pub fn resolve_under(&self, root: &Path) -> PathBuf {
        self.components
            .iter()
            .fold(root.to_path_buf(), |mut path, part| {
                path.push(part);
                path
            })
    }

    pub fn prepare_destination(&self, root: &Path) -> Result<PathBuf, PathError> {
        fs::create_dir_all(root).map_err(|source| PathError::Io {
            operation: "create extraction root",
            path: root.to_path_buf(),
            source,
        })?;
        let root_metadata = fs::symlink_metadata(root).map_err(|source| PathError::Io {
            operation: "inspect extraction root",
            path: root.to_path_buf(),
            source,
        })?;
        if root_metadata.file_type().is_symlink() {
            return Err(PathError::ExistingSymlink {
                path: root.to_path_buf(),
            });
        }

        let mut current = root.to_path_buf();
        for part in &self.components[..self.components.len() - 1] {
            current.push(part);
            match fs::symlink_metadata(&current) {
                Ok(metadata) if metadata.file_type().is_symlink() => {
                    return Err(PathError::ExistingSymlink { path: current });
                }
                Ok(metadata) if !metadata.is_dir() => {
                    return Err(PathError::ExistingNonDirectory { path: current });
                }
                Ok(_) => {}
                Err(error) if error.kind() == io::ErrorKind::NotFound => {
                    fs::create_dir(&current).map_err(|source| PathError::Io {
                        operation: "create extraction ancestor",
                        path: current.clone(),
                        source,
                    })?;
                }
                Err(source) => {
                    return Err(PathError::Io {
                        operation: "inspect extraction ancestor",
                        path: current,
                        source,
                    });
                }
            }
        }

        let destination = current.join(&self.components[self.components.len() - 1]);
        match fs::symlink_metadata(&destination) {
            Ok(_) => Err(PathError::DestinationExists { path: destination }),
            Err(error) if error.kind() == io::ErrorKind::NotFound => Ok(destination),
            Err(source) => Err(PathError::Io {
                operation: "inspect extraction destination",
                path: destination,
                source,
            }),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{LogicalPath, PathError};
    use std::path::{Path, PathBuf};

    #[test]
    fn resolves_valid_name() {
        let path = LogicalPath::parse("docs/a.txt").expect("valid logical path");
        assert_eq!(
            path.resolve_under(Path::new("root")),
            PathBuf::from("root/docs/a.txt")
        );
    }

    #[test]
    fn rejects_cross_platform_escape_syntax() {
        assert!(matches!(
            LogicalPath::parse("a/../b"),
            Err(PathError::Parent { .. })
        ));
        assert!(matches!(LogicalPath::parse("C:/b"), Err(PathError::DriveMarker)));
        assert!(matches!(LogicalPath::parse("a\\b"), Err(PathError::Backslash)));
    }
}

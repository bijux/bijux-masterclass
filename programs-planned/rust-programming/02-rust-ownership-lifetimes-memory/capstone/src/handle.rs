use std::fmt;
use std::num::{NonZeroU64, ParseIntError};
use std::str::FromStr;

/// A stable logical identity for one occupied workspace slot.
///
/// A handle contains both a slot index and a nonzero generation. Reusing a
/// vacant slot increments the generation, so an old handle cannot silently
/// refer to a newly inserted document.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct DocumentHandle {
    slot: usize,
    generation: NonZeroU64,
}

impl DocumentHandle {
    /// Construct a handle while enforcing the nonzero-generation invariant.
    pub fn try_from_parts(
        slot: usize,
        generation: u64,
    ) -> Result<Self, HandleBuildError> {
        let generation = NonZeroU64::new(generation).ok_or(HandleBuildError::ZeroGeneration)?;
        Ok(Self { slot, generation })
    }

    pub(crate) const fn from_nonzero(slot: usize, generation: NonZeroU64) -> Self {
        Self { slot, generation }
    }

    /// Return the slot index encoded by this handle.
    pub const fn slot(self) -> usize {
        self.slot
    }

    /// Return the nonzero generation encoded by this handle.
    pub const fn generation(self) -> u64 {
        self.generation.get()
    }
}

impl fmt::Display for DocumentHandle {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}:{}", self.slot, self.generation)
    }
}

/// A failure to construct a [`DocumentHandle`] from raw parts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HandleBuildError {
    /// Generation zero is reserved and can never identify a live document.
    ZeroGeneration,
}

impl fmt::Display for HandleBuildError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroGeneration => write!(formatter, "document generation must be nonzero"),
        }
    }
}

impl std::error::Error for HandleBuildError {}

/// A failure to parse a `SLOT:GENERATION` document handle.
#[derive(Debug)]
pub enum ParseHandleError {
    /// The input did not contain the required colon separator.
    MissingSeparator,
    /// The slot component was not a valid `usize`.
    InvalidSlot(ParseIntError),
    /// The generation component was not a valid `u64`.
    InvalidGeneration(ParseIntError),
    /// The generation component was zero.
    ZeroGeneration,
}

impl fmt::Display for ParseHandleError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingSeparator => write!(formatter, "handle must be SLOT:GENERATION"),
            Self::InvalidSlot(error) => write!(formatter, "invalid handle slot: {error}"),
            Self::InvalidGeneration(error) => {
                write!(formatter, "invalid handle generation: {error}")
            }
            Self::ZeroGeneration => write!(formatter, "document generation must be nonzero"),
        }
    }
}

impl std::error::Error for ParseHandleError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::InvalidSlot(error) | Self::InvalidGeneration(error) => Some(error),
            Self::MissingSeparator | Self::ZeroGeneration => None,
        }
    }
}

impl FromStr for DocumentHandle {
    type Err = ParseHandleError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        let (slot, generation) = input
            .split_once(':')
            .ok_or(ParseHandleError::MissingSeparator)?;
        let slot = slot.parse().map_err(ParseHandleError::InvalidSlot)?;
        let generation: u64 = generation
            .parse()
            .map_err(ParseHandleError::InvalidGeneration)?;
        let generation = NonZeroU64::new(generation).ok_or(ParseHandleError::ZeroGeneration)?;
        Ok(Self { slot, generation })
    }
}

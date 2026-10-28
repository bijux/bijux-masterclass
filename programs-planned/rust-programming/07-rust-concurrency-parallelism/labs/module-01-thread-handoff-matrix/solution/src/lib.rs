#![forbid(unsafe_code)]

use std::thread;

pub const MAX_INPUTS: usize = 32;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Behavior {
    Normal,
    Yield(usize),
    Panic,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DigestInput {
    pub bytes: Vec<u8>,
    pub behavior: Behavior,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ThreadOutcome {
    Digest(u64),
    Panicked,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RunError {
    TooManyInputs { count: usize, limit: usize },
    MissingOutcome { index: usize },
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf_29ce_4842_2325, |hash, byte| {
        (hash ^ u64::from(*byte)).wrapping_mul(0x100_0000_01b3)
    })
}

pub fn run(inputs: Vec<DigestInput>) -> Result<Vec<ThreadOutcome>, RunError> {
    if inputs.len() > MAX_INPUTS {
        return Err(RunError::TooManyInputs { count: inputs.len(), limit: MAX_INPUTS });
    }

    let count = inputs.len();
    let handles: Vec<_> = inputs
        .into_iter()
        .enumerate()
        .map(|(index, input)| {
            (index, thread::spawn(move || {
                match input.behavior {
                    Behavior::Normal => {}
                    Behavior::Yield(times) => {
                        for _ in 0..times {
                            thread::yield_now();
                        }
                    }
                    Behavior::Panic => panic!("injected worker panic"),
                }
                fnv1a(&input.bytes)
            }))
        })
        .collect();

    let mut outcomes: Vec<Option<ThreadOutcome>> = (0..count).map(|_| None).collect();
    for (index, handle) in handles {
        outcomes[index] = Some(match handle.join() {
            Ok(digest) => ThreadOutcome::Digest(digest),
            Err(_) => ThreadOutcome::Panicked,
        });
    }

    outcomes
        .into_iter()
        .enumerate()
        .map(|(index, outcome)| outcome.ok_or(RunError::MissingOutcome { index }))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::{Behavior, DigestInput, RunError, ThreadOutcome, MAX_INPUTS, fnv1a, run};

    fn input(bytes: &[u8], behavior: Behavior) -> DigestInput {
        DigestInput { bytes: bytes.to_vec(), behavior }
    }

    #[test]
    fn output_is_source_order_despite_varied_completion() {
        let outcomes = run(vec![
            input(b"slow", Behavior::Yield(10_000)),
            input(b"fast", Behavior::Normal),
            input(b"middle", Behavior::Yield(100)),
        ]).expect("bounded input runs");
        assert_eq!(outcomes, vec![
            ThreadOutcome::Digest(fnv1a(b"slow")),
            ThreadOutcome::Digest(fnv1a(b"fast")),
            ThreadOutcome::Digest(fnv1a(b"middle")),
        ]);
    }

    #[test]
    fn all_panics_are_observed_without_early_return() {
        let outcomes = run(vec![
            input(b"a", Behavior::Panic),
            input(b"b", Behavior::Normal),
            input(b"c", Behavior::Panic),
        ]).expect("bounded input runs");
        assert_eq!(outcomes, vec![
            ThreadOutcome::Panicked,
            ThreadOutcome::Digest(fnv1a(b"b")),
            ThreadOutcome::Panicked,
        ]);
    }

    #[test]
    fn rejects_input_above_thread_bound() {
        let inputs = (0..=MAX_INPUTS)
            .map(|_| input(b"x", Behavior::Normal))
            .collect();
        assert_eq!(run(inputs), Err(RunError::TooManyInputs { count: MAX_INPUTS + 1, limit: MAX_INPUTS }));
    }
}

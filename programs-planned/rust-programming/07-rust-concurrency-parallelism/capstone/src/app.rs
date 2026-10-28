use crate::domain::{EngineConfig, FailurePolicy};
use crate::error::AppError;
use crate::parse::parse_manifest;
use crate::report::{render_inspection, render_report, report_is_accepted};
use crate::run_jobs;
use std::ffi::OsString;
use std::fs;

const HELP: &str = "BatchWeave — deterministic bounded concurrent batch processing\n\nUSAGE:\n  batchweave inspect <manifest>\n  batchweave run <manifest> [--workers N] [--queue-capacity N] [--report-threads N] [--fail-fast]\n  batchweave demo\n  batchweave help\n  batchweave version\n\nMANIFEST:\n  The first line is BATCHWEAVE-V1. Each job line contains three tab-separated fields:\n  id<TAB>operation<TAB>payload\n\nOPERATIONS:\n  checksum | word-count | sort-integers | prime-count | panic\n\nEXIT STATUS:\n  0  the command succeeded and every executed job completed\n  1  execution completed with failed, panicked, or cancelled jobs\n  2  usage, input, configuration, or infrastructure failure\n";

const DEMO_MANIFEST: &str = "BATCHWEAVE-V1\nchecksum-readme\tchecksum\treader-first concurrency\ncount-words\tword-count\tone two three four\nsort-values\tsort-integers\t9,-4,7,0\ncount-primes\tprime-count\t100\n";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AppOutput {
    pub stdout: String,
    pub stderr: String,
    pub exit_code: i32,
}

impl AppOutput {
    fn success(stdout: String) -> Self {
        Self {
            stdout,
            stderr: String::new(),
            exit_code: 0,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct RunOptions {
    workers: usize,
    queue_capacity: usize,
    report_threads: usize,
    failure_policy: FailurePolicy,
}

impl Default for RunOptions {
    fn default() -> Self {
        Self {
            workers: 4,
            queue_capacity: 8,
            report_threads: 2,
            failure_policy: FailurePolicy::Continue,
        }
    }
}

pub fn run_arguments<I, S>(arguments: I) -> Result<AppOutput, AppError>
where
    I: IntoIterator<Item = S>,
    S: Into<OsString>,
{
    let arguments: Vec<OsString> = arguments.into_iter().map(Into::into).collect();
    let Some(command) = arguments.first().and_then(|value| value.to_str()) else {
        return Ok(AppOutput::success(HELP.to_owned()));
    };

    match command {
        "help" | "--help" | "-h" => {
            require_exact_arity(&arguments, 1, "batchweave help")?;
            Ok(AppOutput::success(HELP.to_owned()))
        }
        "version" | "--version" | "-V" => {
            require_exact_arity(&arguments, 1, "batchweave version")?;
            Ok(AppOutput::success(format!(
                "batchweave {}\n",
                env!("CARGO_PKG_VERSION")
            )))
        }
        "inspect" => inspect_command(&arguments),
        "run" => run_command(&arguments),
        "demo" => {
            require_exact_arity(&arguments, 1, "batchweave demo")?;
            execute_manifest(DEMO_MANIFEST, RunOptions::default())
        }
        other => Err(AppError::Usage(format!(
            "unknown command {other:?}\n\n{HELP}"
        ))),
    }
}

fn inspect_command(arguments: &[OsString]) -> Result<AppOutput, AppError> {
    require_exact_arity(arguments, 2, "batchweave inspect <manifest>")?;
    let path = path_argument(&arguments[1], "manifest path")?;
    let input = read_manifest(path)?;
    let jobs = parse_manifest(&input)?;
    Ok(AppOutput::success(render_inspection(&jobs)))
}

fn run_command(arguments: &[OsString]) -> Result<AppOutput, AppError> {
    if arguments.len() < 2 {
        return Err(AppError::Usage(
            "usage: batchweave run <manifest> [--workers N] [--queue-capacity N] [--report-threads N] [--fail-fast]"
                .to_owned(),
        ));
    }
    let path = path_argument(&arguments[1], "manifest path")?;
    let options = parse_run_options(&arguments[2..])?;
    let input = read_manifest(path)?;
    execute_manifest(&input, options)
}

fn execute_manifest(input: &str, options: RunOptions) -> Result<AppOutput, AppError> {
    let jobs = parse_manifest(input)?;
    let config = EngineConfig::new(
        options.workers,
        options.queue_capacity,
        options.report_threads,
        options.failure_policy,
    )
    .map_err(|message| crate::error::RunError::InvalidConfiguration(message.to_owned()))?;
    let report = run_jobs(jobs, config)?;
    let exit_code = if report_is_accepted(&report) { 0 } else { 1 };
    Ok(AppOutput {
        stdout: render_report(&report),
        stderr: String::new(),
        exit_code,
    })
}

fn parse_run_options(arguments: &[OsString]) -> Result<RunOptions, AppError> {
    let mut options = RunOptions::default();
    let mut index = 0;
    while index < arguments.len() {
        let flag = arguments[index]
            .to_str()
            .ok_or_else(|| AppError::Usage("options must be valid UTF-8".to_owned()))?;
        match flag {
            "--fail-fast" => {
                options.failure_policy = FailurePolicy::FailFast;
                index += 1;
            }
            "--continue" => {
                options.failure_policy = FailurePolicy::Continue;
                index += 1;
            }
            "--workers" => {
                options.workers = parse_positive_option(arguments, index, flag)?;
                index += 2;
            }
            "--queue-capacity" => {
                options.queue_capacity = parse_positive_option(arguments, index, flag)?;
                index += 2;
            }
            "--report-threads" => {
                options.report_threads = parse_positive_option(arguments, index, flag)?;
                index += 2;
            }
            unknown => {
                return Err(AppError::Usage(format!("unknown run option {unknown:?}")));
            }
        }
    }
    Ok(options)
}

fn parse_positive_option(
    arguments: &[OsString],
    index: usize,
    flag: &str,
) -> Result<usize, AppError> {
    let value = arguments
        .get(index + 1)
        .ok_or_else(|| AppError::Usage(format!("{flag} requires a positive integer")))?;
    value
        .to_str()
        .ok_or_else(|| AppError::Usage(format!("{flag} value must be UTF-8")))?
        .parse::<usize>()
        .map_err(|_| AppError::Usage(format!("{flag} requires a positive integer")))
}

fn read_manifest(path: &str) -> Result<String, AppError> {
    fs::read_to_string(path).map_err(|source| AppError::Io {
        path: path.to_owned(),
        source,
    })
}

fn path_argument<'a>(argument: &'a OsString, name: &str) -> Result<&'a str, AppError> {
    argument
        .to_str()
        .ok_or_else(|| AppError::Usage(format!("{name} must be valid UTF-8 for this course CLI")))
}

fn require_exact_arity(
    arguments: &[OsString],
    expected: usize,
    usage: &str,
) -> Result<(), AppError> {
    if arguments.len() == expected {
        Ok(())
    } else {
        Err(AppError::Usage(format!("usage: {usage}")))
    }
}

#[cfg(test)]
mod tests {
    use super::{parse_run_options, run_arguments};
    use crate::domain::FailurePolicy;
    use std::ffi::OsString;

    #[test]
    fn empty_arguments_render_help() {
        let output = run_arguments(Vec::<String>::new()).expect("help");
        assert_eq!(output.exit_code, 0);
        assert!(output.stdout.contains("deterministic bounded"));
    }

    #[test]
    fn options_are_explicit_and_order_independent() {
        let args = vec![
            OsString::from("--report-threads"),
            OsString::from("3"),
            OsString::from("--fail-fast"),
            OsString::from("--workers"),
            OsString::from("2"),
            OsString::from("--queue-capacity"),
            OsString::from("1"),
        ];
        let options = parse_run_options(&args).expect("valid options");
        assert_eq!(options.workers, 2);
        assert_eq!(options.queue_capacity, 1);
        assert_eq!(options.report_threads, 3);
        assert_eq!(options.failure_policy, FailurePolicy::FailFast);
    }

    #[test]
    fn demo_is_deterministic() {
        let first = run_arguments(["demo"]).expect("demo");
        let second = run_arguments(["demo"]).expect("demo");
        assert_eq!(first, second);
        assert_eq!(first.exit_code, 0);
    }
}

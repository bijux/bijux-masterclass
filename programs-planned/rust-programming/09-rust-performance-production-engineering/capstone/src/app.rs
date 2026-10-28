use crate::config::Config;
use crate::load::{self, LoadOptions};
use crate::parse::parse_record;
use crate::release::BuildInfo;
use crate::server;
use crate::store::{Store, StoreError};
use std::fmt;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;
use std::time::Duration;

#[derive(Debug)]
pub enum AppError {
    Usage(String),
    Io(io::Error),
    Parse { line: usize, message: String },
    Store(StoreError),
    Server(server::ServerError),
}

impl fmt::Display for AppError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Usage(message) => write!(formatter, "usage error: {message}"),
            Self::Io(error) => write!(formatter, "I/O error: {error}"),
            Self::Parse { line, message } => write!(formatter, "line {line}: {message}"),
            Self::Store(error) => write!(formatter, "store error: {error}"),
            Self::Server(error) => write!(formatter, "server error: {error}"),
        }
    }
}

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::Store(error) => Some(error),
            Self::Server(error) => Some(error),
            Self::Usage(_) | Self::Parse { .. } => None,
        }
    }
}

impl From<io::Error> for AppError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

impl From<StoreError> for AppError {
    fn from(value: StoreError) -> Self {
        Self::Store(value)
    }
}

impl From<server::ServerError> for AppError {
    fn from(value: server::ServerError) -> Self {
        Self::Server(value)
    }
}

pub fn analyze_text(input: &str, config: &Config) -> Result<String, AppError> {
    if input.len() > config.max_offline_bytes {
        return Err(AppError::Usage(
            "input exceeds offline byte limit".into(),
        ));
    }

    let mut store = Store::new(config.max_series, config.max_identifier_storage_bytes);
    let mut records = 0_usize;
    for (index, line) in input.lines().enumerate() {
        if line.is_empty() {
            continue;
        }
        records = records
            .checked_add(1)
            .ok_or_else(|| AppError::Usage("record count overflow".into()))?;
        if records > config.max_offline_records {
            return Err(AppError::Usage(
                "input exceeds offline record limit".into(),
            ));
        }
        let record = parse_record(
            line,
            config.max_line_bytes,
            config.max_identifier_bytes,
        )
        .map_err(|error| AppError::Parse {
            line: index + 1,
            message: error.to_string(),
        })?;
        store.apply(record)?;
    }
    store
        .snapshot()
        .render(config.max_snapshot_bytes)
        .map_err(Into::into)
}

fn read_bounded_utf8(path: &Path, maximum: usize) -> Result<String, AppError> {
    let file = File::open(path)?;
    let read_limit = u64::try_from(maximum)
        .map_err(|_| AppError::Usage("byte limit does not fit u64".into()))?
        .checked_add(1)
        .ok_or_else(|| AppError::Usage("byte limit overflow".into()))?;
    let mut input = String::new();
    file.take(read_limit).read_to_string(&mut input)?;
    if input.len() > maximum {
        return Err(AppError::Usage(
            "input exceeds offline byte limit".into(),
        ));
    }
    Ok(input)
}

pub fn analyze_file(path: &Path, config: &Config) -> Result<String, AppError> {
    let input = read_bounded_utf8(path, config.max_offline_bytes)?;
    analyze_text(&input, config)
}

fn help() -> String {
    [
        "metricrail analyze <events.tsv>",
        "metricrail serve <address>",
        "metricrail load <address> <events.tsv> [connections]",
        "metricrail version",
        "metricrail help",
    ]
    .join("\n")
}

pub async fn run_cli(args: Vec<String>) -> Result<String, AppError> {
    let config = Config::default();
    config
        .validate()
        .map_err(|error| AppError::Usage(format!("invalid configuration: {error}")))?;

    match args.as_slice() {
        [] => Ok(help()),
        [command] if command == "help" => Ok(help()),
        [command] if command == "version" => Ok(BuildInfo::current().render()),
        [command, path] if command == "analyze" => analyze_file(Path::new(path), &config),
        [command, address] if command == "serve" => {
            let server = server::spawn(address, config).await?;
            let bound = server.address;
            tracing::info!(%bound, "MetricRail ready");
            tokio::signal::ctrl_c().await?;
            server.shutdown().await?;
            Ok(format!("stopped {bound}"))
        }
        [command, address, path] if command == "load" => {
            run_load(address, path, 1, &config).await
        }
        [command, address, path, connections] if command == "load" => {
            let connections = connections
                .parse::<usize>()
                .map_err(|_| AppError::Usage("connections must be an integer".into()))?;
            run_load(address, path, connections, &config).await
        }
        _ => Err(AppError::Usage(help())),
    }
}

async fn run_load(
    address: &str,
    path: &str,
    connections: usize,
    config: &Config,
) -> Result<String, AppError> {
    let input = read_bounded_utf8(Path::new(path), config.max_offline_bytes)?;
    let records: Vec<String> = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(str::to_owned)
        .collect();
    if records.len() > config.max_offline_records {
        return Err(AppError::Usage(
            "input exceeds offline record limit".into(),
        ));
    }

    let options = LoadOptions {
        connections,
        request_timeout: Duration::from_millis(config.load_request_timeout_ms),
        max_line_bytes: config.max_line_bytes,
    };
    let report = load::run(address, records, options).await?;
    let render_percentile = |percentile| {
        report
            .response_latency_percentile(percentile)
            .map(|duration| duration.as_micros().to_string())
            .unwrap_or_else(|| "n/a".into())
    };
    Ok(format!(
        "offered={}\ncompleted={}\nrejected={}\nfailed={}\nelapsed_ms={}\nresponse_p50_us={}\nresponse_p95_us={}\nresponse_p99_us={}\n",
        report.offered,
        report.completed,
        report.rejected,
        report.failed,
        report.elapsed.as_millis(),
        render_percentile(50),
        render_percentile(95),
        render_percentile(99),
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn offline_analysis_is_deterministic() {
        let input = "z\tb\t1\t1\n\
                     a\tc\t1\t2\n\
                     a\tb\t1\t3\n";
        let first = analyze_text(input, &Config::default()).expect("analysis");
        let second = analyze_text(input, &Config::default()).expect("analysis");
        assert_eq!(first, second);
        assert!(first.starts_with("a\tb\t"));
    }

    #[test]
    fn physical_line_is_preserved_in_error() {
        let input = "a\tx\t1\t1\nbad\n";
        match analyze_text(input, &Config::default()) {
            Err(AppError::Parse { line, .. }) => assert_eq!(line, 2),
            other => panic!("unexpected result: {other:?}"),
        }
    }
}

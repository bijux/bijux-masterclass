use std::io;
use std::time::{Duration, Instant};
use tokio::io::{AsyncBufRead, AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpStream;
use tokio::task::JoinSet;

#[derive(Debug, Clone, Copy)]
pub struct LoadOptions {
    pub connections: usize,
    pub request_timeout: Duration,
    pub max_line_bytes: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LoadOutcome {
    Completed {
        index: usize,
        latency: Duration,
    },
    Rejected {
        index: usize,
        code: String,
        latency: Duration,
    },
    Failed {
        index: usize,
        message: String,
    },
}

impl LoadOutcome {
    fn index(&self) -> usize {
        match self {
            Self::Completed { index, .. }
            | Self::Rejected { index, .. }
            | Self::Failed { index, .. } => *index,
        }
    }
}

#[derive(Debug)]
pub struct LoadReport {
    pub offered: usize,
    pub completed: usize,
    pub rejected: usize,
    pub failed: usize,
    pub outcomes: Vec<LoadOutcome>,
    pub elapsed: Duration,
}

impl LoadReport {
    /// Return the nearest-rank percentile for requests that received a terminal
    /// protocol response. Transport failures and timeouts are reported
    /// separately and are not silently folded into response latency.
    pub fn response_latency_percentile(&self, percentile: u8) -> Option<Duration> {
        if percentile == 0 || percentile > 100 {
            return None;
        }

        let mut latencies: Vec<Duration> = self
            .outcomes
            .iter()
            .filter_map(|outcome| match outcome {
                LoadOutcome::Completed { latency, .. }
                | LoadOutcome::Rejected { latency, .. } => Some(*latency),
                LoadOutcome::Failed { .. } => None,
            })
            .collect();
        if latencies.is_empty() {
            return None;
        }

        latencies.sort_unstable();
        let numerator = usize::from(percentile)
            .checked_mul(latencies.len())?;
        let rank = numerator
            .checked_add(99)?
            .checked_div(100)?;
        latencies.get(rank.saturating_sub(1)).copied()
    }
}

async fn read_bounded_response<R: AsyncBufRead + Unpin>(
    reader: &mut R,
    maximum: usize,
) -> io::Result<String> {
    let mut bytes = Vec::with_capacity(maximum.min(256));
    loop {
        let (consumed, complete, too_long) = {
            let available = reader.fill_buf().await?;
            if available.is_empty() {
                if bytes.is_empty() {
                    return Err(io::Error::new(
                        io::ErrorKind::UnexpectedEof,
                        "server closed without a response",
                    ));
                }
                break;
            }
            let (data_length, consumed, complete) =
                if let Some(position) = available.iter().position(|&byte| byte == b'\n') {
                    (position, position + 1, true)
                } else {
                    (available.len(), available.len(), false)
                };
            let too_long = bytes
                .len()
                .checked_add(data_length)
                .is_none_or(|length| length > maximum);
            if !too_long {
                bytes.extend_from_slice(&available[..data_length]);
            }
            (consumed, complete, too_long)
        };
        reader.consume(consumed);
        if too_long {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "response exceeds configured line limit",
            ));
        }
        if complete {
            break;
        }
    }
    if bytes.last() == Some(&b'\r') {
        bytes.pop();
    }
    String::from_utf8(bytes)
        .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "response is not UTF-8"))
}

async fn exchange(address: &str, record: &str, max_response_bytes: usize) -> io::Result<String> {
    let stream = TcpStream::connect(address).await?;
    let (read, mut write) = stream.into_split();
    let mut reader = BufReader::new(read);
    write.write_all(b"INGEST\t").await?;
    write.write_all(record.as_bytes()).await?;
    write.write_all(b"\n").await?;
    write.flush().await?;
    read_bounded_response(&mut reader, max_response_bytes).await
}

async fn send_one(
    address: String,
    index: usize,
    record: String,
    request_timeout: Duration,
    max_line_bytes: usize,
) -> LoadOutcome {
    if record.len().saturating_add("INGEST\t".len()) > max_line_bytes {
        return LoadOutcome::Failed {
            index,
            message: "request exceeds configured line limit".into(),
        };
    }

    let started = Instant::now();
    let response = match tokio::time::timeout(request_timeout, exchange(&address, &record, max_line_bytes)).await {
        Ok(Ok(response)) => response,
        Ok(Err(error)) => {
            return LoadOutcome::Failed {
                index,
                message: error.to_string(),
            };
        }
        Err(_) => {
            return LoadOutcome::Failed {
                index,
                message: "request deadline exceeded".into(),
            };
        }
    };

    let latency = started.elapsed();
    if response.trim_end() == "OK" {
        LoadOutcome::Completed { index, latency }
    } else if let Some(rest) = response.trim_end().strip_prefix("ERR\t") {
        let code = rest.split('\t').next().unwrap_or("UNKNOWN").to_owned();
        LoadOutcome::Rejected {
            index,
            code,
            latency,
        }
    } else {
        LoadOutcome::Failed {
            index,
            message: format!("unexpected response: {}", response.trim_end()),
        }
    }
}

pub async fn run(
    address: &str,
    records: Vec<String>,
    options: LoadOptions,
) -> io::Result<LoadReport> {
    if options.connections == 0 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "connections must be nonzero",
        ));
    }
    if options.request_timeout.is_zero() {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "request timeout must be nonzero",
        ));
    }
    if options.max_line_bytes == 0 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "line limit must be nonzero",
        ));
    }

    let offered = records.len();
    let started = Instant::now();
    let mut pending = records.into_iter().enumerate();
    let mut tasks = JoinSet::new();
    let parallelism = options.connections.min(offered);

    for _ in 0..parallelism {
        if let Some((index, record)) = pending.next() {
            let address = address.to_owned();
            tasks.spawn(send_one(
                address,
                index,
                record,
                options.request_timeout,
                options.max_line_bytes,
            ));
        }
    }

    let mut outcomes = Vec::with_capacity(offered);
    while let Some(result) = tasks.join_next().await {
        let outcome = result
            .map_err(|error| io::Error::other(format!("load task failed: {error}")))?;
        outcomes.push(outcome);

        if let Some((index, record)) = pending.next() {
            let address = address.to_owned();
            tasks.spawn(send_one(
                address,
                index,
                record,
                options.request_timeout,
                options.max_line_bytes,
            ));
        }
    }

    outcomes.sort_by_key(LoadOutcome::index);
    let completed = outcomes
        .iter()
        .filter(|outcome| matches!(outcome, LoadOutcome::Completed { .. }))
        .count();
    let rejected = outcomes
        .iter()
        .filter(|outcome| matches!(outcome, LoadOutcome::Rejected { .. }))
        .count();
    let failed = outcomes
        .iter()
        .filter(|outcome| matches!(outcome, LoadOutcome::Failed { .. }))
        .count();

    Ok(LoadReport {
        offered,
        completed,
        rejected,
        failed,
        outcomes,
        elapsed: started.elapsed(),
    })
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn nearest_rank_percentiles_use_terminal_responses_only() {
        let report = LoadReport {
            offered: 5,
            completed: 3,
            rejected: 1,
            failed: 1,
            outcomes: vec![
                LoadOutcome::Completed {
                    index: 0,
                    latency: Duration::from_micros(10),
                },
                LoadOutcome::Rejected {
                    index: 1,
                    code: "CAPACITY".into(),
                    latency: Duration::from_micros(40),
                },
                LoadOutcome::Completed {
                    index: 2,
                    latency: Duration::from_micros(20),
                },
                LoadOutcome::Failed {
                    index: 3,
                    message: "deadline".into(),
                },
                LoadOutcome::Completed {
                    index: 4,
                    latency: Duration::from_micros(30),
                },
            ],
            elapsed: Duration::from_millis(1),
        };

        assert_eq!(
            report.response_latency_percentile(50),
            Some(Duration::from_micros(20))
        );
        assert_eq!(
            report.response_latency_percentile(95),
            Some(Duration::from_micros(40))
        );
        assert_eq!(report.response_latency_percentile(0), None);
        assert_eq!(report.response_latency_percentile(101), None);
    }

    #[test]
    fn percentile_is_absent_without_a_protocol_response() {
        let report = LoadReport {
            offered: 1,
            completed: 0,
            rejected: 0,
            failed: 1,
            outcomes: vec![LoadOutcome::Failed {
                index: 0,
                message: "connect failed".into(),
            }],
            elapsed: Duration::from_millis(1),
        };
        assert_eq!(report.response_latency_percentile(50), None);
    }
}

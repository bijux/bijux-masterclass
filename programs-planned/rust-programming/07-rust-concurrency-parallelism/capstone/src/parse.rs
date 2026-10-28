use crate::domain::{
    Job, JobId, MANIFEST_HEADER, MAX_JOBS, MAX_PAYLOAD_BYTES, MAX_TOTAL_PAYLOAD_BYTES,
    Operation,
};
use crate::error::ManifestError;
use std::collections::BTreeSet;
use std::str::FromStr;

pub fn parse_manifest(input: &str) -> Result<Vec<Job>, ManifestError> {
    let mut lines = input.lines().enumerate();
    let Some((_, header)) = lines.next() else {
        return Err(ManifestError::Empty);
    };
    if header.trim_end_matches('\r') != MANIFEST_HEADER {
        return Err(ManifestError::InvalidHeader { found: header.to_owned() });
    }

    let mut jobs = Vec::new();
    let mut ids = BTreeSet::new();
    let mut total_payload = 0usize;

    for (zero_line, raw) in lines {
        let line = zero_line + 1;
        let raw = raw.trim_end_matches('\r');
        if raw.is_empty() || raw.starts_with('#') {
            continue;
        }
        if jobs.len() == MAX_JOBS {
            return Err(ManifestError::TooManyJobs { count: jobs.len() + 1, limit: MAX_JOBS });
        }
        let fields: Vec<_> = raw.split('\t').collect();
        if fields.len() != 3 {
            return Err(ManifestError::MalformedLine {
                line,
                message: "expected exactly three tab-separated fields: id, operation, payload".to_owned(),
            });
        }
        let id = JobId::new(fields[0]).map_err(|message| ManifestError::MalformedLine {
            line,
            message: message.to_owned(),
        })?;
        if !ids.insert(id.clone()) {
            return Err(ManifestError::DuplicateId { line, id: id.to_string() });
        }
        let operation = Operation::from_str(fields[1]).map_err(|message| ManifestError::MalformedLine {
            line,
            message: format!("{message}: {:?}", fields[1]),
        })?;
        let payload_bytes = fields[2].len();
        if payload_bytes > MAX_PAYLOAD_BYTES {
            return Err(ManifestError::PayloadTooLarge { line, count: payload_bytes, limit: MAX_PAYLOAD_BYTES });
        }
        total_payload = total_payload.checked_add(payload_bytes).ok_or(
            ManifestError::TotalPayloadTooLarge { line, count: usize::MAX, limit: MAX_TOTAL_PAYLOAD_BYTES },
        )?;
        if total_payload > MAX_TOTAL_PAYLOAD_BYTES {
            return Err(ManifestError::TotalPayloadTooLarge { line, count: total_payload, limit: MAX_TOTAL_PAYLOAD_BYTES });
        }
        jobs.push(Job {
            index: jobs.len(),
            id,
            operation,
            payload: fields[2].to_owned(),
        });
    }
    Ok(jobs)
}

#[cfg(test)]
mod tests {
    use super::parse_manifest;
    use crate::domain::Operation;
    use crate::error::ManifestError;

    #[test]
    fn parses_comments_blank_lines_and_stable_indices() {
        let input = "BATCHWEAVE-V1\n# comment\na\tchecksum\thello\n\nb\tword-count\tone two\n";
        let jobs = parse_manifest(input).expect("valid manifest");
        assert_eq!(jobs.len(), 2);
        assert_eq!(jobs[0].index, 0);
        assert_eq!(jobs[1].operation, Operation::WordCount);
    }

    #[test]
    fn rejects_duplicate_ids_and_extra_tabs() {
        let duplicate = "BATCHWEAVE-V1\na\tchecksum\tx\na\tchecksum\ty\n";
        assert!(matches!(parse_manifest(duplicate), Err(ManifestError::DuplicateId { .. })));
        let extra = "BATCHWEAVE-V1\na\tchecksum\tx\ty\n";
        assert!(matches!(parse_manifest(extra), Err(ManifestError::MalformedLine { .. })));
    }
}

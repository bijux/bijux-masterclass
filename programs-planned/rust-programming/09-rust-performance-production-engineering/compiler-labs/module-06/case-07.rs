fn main() { let request_id = 42_u64; let operation = "ingest"; let line = format!("request_id={request_id} operation={operation}"); assert!(!line.contains("payload")); }

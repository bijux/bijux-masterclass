fn main() { for request_id in 0..100_000 { println!("metric_requests{{request_id=\"{request_id}\"}} 1"); } }

fn main() { let offered = 10; let first_attempts = 10; let retries = 3; let amplification = (first_attempts + retries) as f64 / offered as f64; assert_eq!(amplification, 1.3); }

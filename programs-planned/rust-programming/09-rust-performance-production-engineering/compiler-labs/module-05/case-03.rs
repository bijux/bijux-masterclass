fn utilization(active: usize, capacity: usize) -> Option<f64> { (capacity != 0).then(|| active as f64 / capacity as f64) } fn main() { assert_eq!(utilization(1, 2), Some(0.5)); }

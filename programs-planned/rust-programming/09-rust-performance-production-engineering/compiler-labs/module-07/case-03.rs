fn burn(failures: u64, budget: u64) -> Option<f64> { (budget != 0).then(|| failures as f64 / budget as f64) } fn main() { assert_eq!(burn(5, 10), Some(0.5)); }

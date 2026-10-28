#[derive(Default)] struct Counters { calls: usize } impl Counters { fn record(&mut self) { self.calls += 1; } } fn main() { let mut c = Counters::default(); c.record(); assert_eq!(c.calls, 1); }

struct Counter { current: u8, end: u8 }
impl Iterator for Counter {
    type Item = u8;
    fn next(&mut self) -> Option<Self::Item> {
        if self.current >= self.end { None } else { let value=self.current; self.current+=1; Some(value) }
    }
}
fn main() { assert_eq!(Counter{current:0,end:3}.collect::<Vec<_>>(), vec![0,1,2]); }

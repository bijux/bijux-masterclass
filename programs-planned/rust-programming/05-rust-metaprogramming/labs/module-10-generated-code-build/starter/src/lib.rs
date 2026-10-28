#![forbid(unsafe_code)]

include!(concat!(env!("OUT_DIR"), "/generated.rs"));

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_reads_the_schema() {
        assert_eq!(COMMAND_COUNT, 2);
    }
}

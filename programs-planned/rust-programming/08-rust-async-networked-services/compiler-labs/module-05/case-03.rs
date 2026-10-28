#![allow(dead_code)]
#[derive(Debug, PartialEq)] enum Command { Ping, Submit(String) }
fn parse(line: &str) -> Result<Command, &'static str> { if line == "PING" { Ok(Command::Ping) } else if let Some(value)=line.strip_prefix("SUBMIT ") { Ok(Command::Submit(value.to_owned())) } else { Err("unsupported command") } }
fn main() { assert_eq!(parse("PING"), Ok(Command::Ping)); }

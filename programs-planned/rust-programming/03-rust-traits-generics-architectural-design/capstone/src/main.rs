use std::{env,fs,process::ExitCode};
use review_engine::{default_registry,EngineBuilder,FileSource,TextReporter,TsvSource};

fn usage()->&'static str{"usage:\n  review-engine check <submissions.tsv> <policy.txt>\n  review-engine list-rules\n  review-engine explain <rule-name>\n  review-engine demo"}

fn run(args:&[String])->Result<u8,String>{
 let registry=default_registry();
 match args{
  [command] if command=="list-rules"=>{for name in registry.names(){println!("{name}");}Ok(0)}
  [command,name] if command=="explain"=>{let text=registry.explain(name).ok_or_else(||format!("unknown rule {name:?}"))?;println!("{name}: {text}");Ok(0)}
  [command,submissions,policy] if command=="check"=>{let policy_text=fs::read_to_string(policy).map_err(|e|format!("cannot read policy {policy}: {e}"))?;let policy=registry.parse(&policy_text).map_err(|e|e.to_string())?;let outcome=EngineBuilder::new().with_source(FileSource::new(submissions)).with_reporter(TextReporter).with_policy(policy).build().run().map_err(|e|e.to_string())?;print!("{}",outcome.output);Ok(if outcome.accepted(){0}else{1})}
  [command] if command=="demo"=>{let submissions="S-001\tada\t92\trust,cli\tA dependable command-line tool\nS-002\troot\t55\tprototype\tDraft\n";let policy=registry.parse("min-score\t70\nrequire-tag\trust\ntitle-length\t5\t80\ndeny-owner\troot\n").map_err(|e|e.to_string())?;let outcome=EngineBuilder::new().with_source(TsvSource::new(submissions)).with_reporter(TextReporter).with_policy(policy).build().run().map_err(|e|e.to_string())?;print!("{}",outcome.output);Ok(if outcome.accepted(){0}else{1})}
  _=>Err(usage().into()),
 }
}
fn main()->ExitCode{let args:Vec<String>=env::args().skip(1).collect();match run(&args){Ok(0)=>ExitCode::SUCCESS,Ok(code)=>ExitCode::from(code),Err(e)=>{eprintln!("error: {e}");ExitCode::from(2)}}}

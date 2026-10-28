use std::process::Command;

#[test]
fn demo_reports_rejection(){
 let output=Command::new(env!("CARGO_BIN_EXE_review-engine")).arg("demo").output().expect("run");
 assert_eq!(output.status.code(),Some(1));
 let stdout=String::from_utf8(output.stdout).expect("utf8");
 assert!(stdout.contains("accepted: false"));
 assert!(stdout.contains("S-002"));
}

#[test]
fn list_rules_is_stable(){let output=Command::new(env!("CARGO_BIN_EXE_review-engine")).arg("list-rules").output().expect("run");assert!(output.status.success());assert_eq!(String::from_utf8(output.stdout).expect("utf8"),"min-score\nrequire-tag\ntitle-length\ndeny-owner\n");}

use review_engine::{default_registry,PolicyError,Source,TsvSource};

#[test]fn unknown_rule_retains_line(){let error = default_registry().parse("unknown\tx").err().expect("error"); assert_eq!(error, PolicyError::UnknownRule{line:1,name:"unknown".into()});}
#[test]fn malformed_submission_retains_line(){let e=TsvSource::new("S-1\ta\t1\t\tt\nbad").load().err().expect("error");assert!(e.to_string().contains("line 2"));}

use review_engine::{default_registry,EngineBuilder,MemorySource,Submission,SubmissionId,TextReporter};

fn submission(id:&str,owner:&str,score:u8,tags:&[&str],title:&str)->Submission{Submission::new(SubmissionId::new(id).expect("id"),owner,score,tags.iter().map(|s|(*s).to_owned()).collect(),title).expect("submission")}

#[test]
fn policy_order_and_submission_order_are_deterministic(){
 let policy=default_registry().parse("min-score\t70\nrequire-tag\trust").expect("policy");
 let source=MemorySource::new(vec![submission("S-1","ada",50,&[],"One"),submission("S-2","bob",60,&[],"Two")]);
 let out=EngineBuilder::new().with_source(source).with_reporter(TextReporter).with_policy(policy).build().run().expect("run");
 let keys:Vec<_>=out.review.findings().iter().map(|f|(f.submission.to_string(),f.rule.to_string())).collect();
 assert_eq!(keys,vec![("S-1".into(),"min-score-70".into()),("S-1".into(),"require-tag-rust".into()),("S-2".into(),"min-score-70".into()),("S-2".into(),"require-tag-rust".into())]);
}

#[test]
fn warnings_do_not_reject(){let policy=default_registry().parse("title-length\t10\t20").expect("policy");let out=EngineBuilder::new().with_source(MemorySource::new(vec![submission("S-1","ada",99,&["rust"],"tiny")])).with_reporter(TextReporter).with_policy(policy).build().run().expect("run");assert!(out.accepted());assert_eq!(out.review.warning_count(),1);}

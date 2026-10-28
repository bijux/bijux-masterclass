use std::{
    fs,
    path::PathBuf,
    time::{SystemTime, UNIX_EPOCH},
};

use axiomstore::{Record, Store, ValidationIssue, Validator};

#[cfg(unix)]
use axiomstore::LendingRecords;

fn temp_path(name: &str) -> PathBuf {
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "axiomstore-{name}-{}-{unique}.ax",
        std::process::id()
    ))
}

struct NoQuestionMark;

impl Validator for NoQuestionMark {
    fn name(&self) -> &'static str {
        "no-question-mark"
    }

    fn validate(&self, record: &Record) -> Result<(), ValidationIssue> {
        if record.value().contains('?') {
            Err(ValidationIssue::new(
                "question-mark",
                "value may not contain ?",
            ))
        } else {
            Ok(())
        }
    }
}

#[cfg(unix)]
#[test]
fn init_put_and_borrowed_list_form_one_public_story() {
    let path = temp_path("public");
    let store = Store::<256, 4>::new(&path).expect("store");
    assert!(store.init().expect("initialize").is_empty());
    store
        .put(Record::new("beta", "two").expect("record"))
        .expect("put beta");
    store
        .put(Record::new("alpha", "one").expect("record"))
        .expect("put alpha");

    let snapshot = store.open_snapshot().expect("open");
    let mut cursor = snapshot.records();
    let first = cursor
        .next()
        .expect("first")
        .expect("valid")
        .to_owned()
        .expect("owned");
    let second = cursor
        .next()
        .expect("second")
        .expect("valid")
        .to_owned()
        .expect("owned");
    assert_eq!((first.key(), first.value()), ("alpha", "one"));
    assert_eq!((second.key(), second.value()), ("beta", "two"));
    assert!(cursor.next().is_none());
    fs::remove_file(path).expect("remove archive");
}

#[cfg(unix)]
#[test]
fn failed_dynamic_validation_leaves_previous_bytes_unchanged() {
    let path = temp_path("validation");
    let mut store = Store::<64, 4>::new(&path).expect("store");
    store
        .register_validator(NoQuestionMark)
        .expect("unique validator");
    store.init().expect("initialize");
    store
        .put(Record::new("ok", "value").expect("record"))
        .expect("initial put");
    let before = fs::read(&path).expect("read previous bytes");

    let error = store
        .put(Record::new("bad", "why?").expect("record"))
        .expect_err("validator should reject");
    assert!(error.to_string().contains("no-question-mark"));
    assert_eq!(fs::read(&path).expect("read preserved bytes"), before);
    fs::remove_file(path).expect("remove archive");
}

#[test]
fn duplicate_validator_names_are_rejected_without_registration() {
    let path = temp_path("validators");
    let mut store = Store::<64, 4>::new(path).expect("store");
    store
        .register_validator(NoQuestionMark)
        .expect("first registration");
    let error = store
        .register_validator(NoQuestionMark)
        .expect_err("duplicate name");
    assert!(error.to_string().contains("duplicate validator"));
    assert_eq!(
        store.validator_names().filter(|name| *name == "no-question-mark").count(),
        1
    );
}

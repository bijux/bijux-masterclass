#![cfg(unix)]

use std::{
    collections::BTreeMap,
    fs,
    path::PathBuf,
    time::{SystemTime, UNIX_EPOCH},
};

use axiomstore::{LendingRecords, Record, Store};

#[derive(Clone, Debug)]
enum Op {
    Put(&'static str, &'static str),
    Remove(&'static str),
    Clear,
}

fn temp_path(label: &str) -> PathBuf {
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "axiomstore-tx-{label}-{}-{unique}.ax",
        std::process::id()
    ))
}

fn apply_model(model: &mut BTreeMap<String, String>, operation: &Op) {
    match operation {
        Op::Put(key, value) => {
            model.insert((*key).into(), (*value).into());
        }
        Op::Remove(key) => {
            model.remove(*key);
        }
        Op::Clear => model.clear(),
    }
}

fn run_sequence(sequence: &[Op]) {
    let path = temp_path("model");
    let store = Store::<256, 8>::new(&path).expect("store");
    store.init().expect("initialize");
    let mut transaction = store.transaction();
    let mut model = BTreeMap::new();

    for operation in sequence {
        apply_model(&mut model, operation);
        match operation {
            Op::Put(key, value) => transaction
                .put(Record::new(*key, *value).expect("record"))
                .expect("capacity"),
            Op::Remove(key) => transaction.remove(*key).expect("capacity"),
            Op::Clear => transaction.clear().expect("capacity"),
        }
    }

    let snapshot = transaction.commit().expect("commit");
    let mut actual = BTreeMap::new();
    let mut cursor = snapshot.records();
    while let Some(view) = cursor.next() {
        let view = view.expect("valid record");
        actual.insert(view.key().to_owned(), view.value().to_owned());
    }
    assert_eq!(actual, model, "sequence: {sequence:?}");
    fs::remove_file(path).expect("remove archive");
}

fn enumerate(prefix: &mut Vec<Op>, alphabet: &[Op], depth: usize) {
    run_sequence(prefix);
    if prefix.len() == depth {
        return;
    }
    for operation in alphabet {
        prefix.push(operation.clone());
        enumerate(prefix, alphabet, depth);
        prefix.pop();
    }
}

#[test]
fn bounded_operation_sequences_match_an_independent_map_model() {
    let alphabet = [
        Op::Put("a", "1"),
        Op::Put("b", "2"),
        Op::Remove("a"),
        Op::Clear,
    ];
    enumerate(&mut Vec::new(), &alphabet, 3);
}

#[test]
fn capacity_failure_does_not_publish_staged_operations() {
    let path = temp_path("capacity");
    let store = Store::<256, 1>::new(&path).expect("store");
    store.init().expect("initialize");
    let mut transaction = store.transaction();
    transaction
        .put(Record::new("a", "1").expect("record"))
        .expect("first operation");
    assert!(
        transaction
            .put(Record::new("b", "2").expect("record"))
            .is_err()
    );
    assert!(store.open_snapshot().expect("old snapshot").is_empty());
    fs::remove_file(path).expect("remove archive");
}

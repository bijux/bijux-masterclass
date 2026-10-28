use criterion::{Criterion, criterion_group, criterion_main};
use metricrail::config::Config;
use metricrail::parse::parse_record;
use metricrail::store::Store;
use std::hint::black_box;

fn benchmark_parse(criterion: &mut Criterion) {
    let config = Config::default();
    criterion.bench_function("parse_record_common", |bencher| {
        bencher.iter(|| {
            parse_record(
                black_box("acme\trequest_latency_ms\t1723075200000\t18.5"),
                config.max_line_bytes,
                config.max_identifier_bytes,
            )
            .expect("valid benchmark record")
        });
    });
}

fn benchmark_apply(criterion: &mut Criterion) {
    let config = Config::default();
    let record = parse_record(
        "acme\trequest_latency_ms\t1723075200000\t18.5",
        config.max_line_bytes,
        config.max_identifier_bytes,
    )
    .expect("valid benchmark record");
    criterion.bench_function("apply_new_series", |bencher| {
        bencher.iter_batched(
            || Store::new(1024, 1024 * 1024),
            |mut store| {
                store.apply(black_box(record.clone())).expect("apply");
                black_box(store.len())
            },
            criterion::BatchSize::SmallInput,
        );
    });
}

fn benchmark_snapshot(criterion: &mut Criterion) {
    let config = Config::default();
    let mut store = Store::new(4096, 1024 * 1024);
    for index in 0..1000_u64 {
        let line = format!("tenant\tmetric-{index}\t{index}\t1");
        let record = parse_record(
            &line,
            config.max_line_bytes,
            config.max_identifier_bytes,
        )
        .expect("valid benchmark record");
        store.apply(record).expect("apply");
    }
    criterion.bench_function("render_snapshot_1000_series", |bencher| {
        bencher.iter(|| {
            store
                .snapshot()
                .render(black_box(config.max_snapshot_bytes))
                .expect("snapshot")
        });
    });
}

criterion_group!(benches, benchmark_parse, benchmark_apply, benchmark_snapshot);
criterion_main!(benches);

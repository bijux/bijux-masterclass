use std::env;

fn main() {
    println!("cargo::rerun-if-env-changed=METRICRAIL_SOURCE_REVISION");
    println!("cargo::rerun-if-env-changed=METRICRAIL_PROFILE");

    let target = env::var("TARGET").unwrap_or_else(|_| "unknown".into());
    let profile = env::var("METRICRAIL_PROFILE")
        .or_else(|_| env::var("PROFILE"))
        .unwrap_or_else(|_| "unknown".into());
    let source_revision =
        env::var("METRICRAIL_SOURCE_REVISION").unwrap_or_else(|_| "unknown".into());

    println!("cargo::rustc-env=METRICRAIL_TARGET={target}");
    println!("cargo::rustc-env=METRICRAIL_PROFILE={profile}");
    println!("cargo::rustc-env=METRICRAIL_SOURCE_REVISION={source_revision}");
}

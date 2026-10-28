#![allow(dead_code)]
enum Service { Starting, Ready, Quiescing, Draining, Stopped }
fn label(state: Service) -> &'static str { match state { Service::Starting => "starting", Service::Ready => "ready", Service::Stopped => "stopped" } }
fn main() {}

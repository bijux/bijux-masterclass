#![allow(dead_code)]
#[derive(Clone, Copy)] enum Service { Starting, Ready, Quiescing, Draining, Stopped }
fn accepts(state: Service) -> bool { match state { Service::Ready => true, Service::Starting | Service::Quiescing | Service::Draining | Service::Stopped => false } }
fn main() { assert!(!accepts(Service::Quiescing)); }

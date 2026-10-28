use crate::{ArgumentSpec, CommandError};

#[derive(Clone, Copy)]
pub struct HandlerDescriptor {
    pub about: &'static str,
    pub usage: &'static str,
    pub arguments: &'static [ArgumentSpec],
    pub invoke: fn(&[String]) -> Result<String, CommandError>,
}

#[derive(Clone, Copy)]
pub struct CommandSpec {
    pub name: &'static str,
    pub handler: HandlerDescriptor,
}

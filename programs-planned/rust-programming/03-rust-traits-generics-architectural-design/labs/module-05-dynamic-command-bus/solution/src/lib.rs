#![forbid(unsafe_code)]
//! Reference design for the dynamic-command-bus laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Command { pub name: String, pub payload: String }
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Response(pub String);
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum DispatchError { Unknown(String), Rejected(String) }

pub trait Handler {
    fn command_name(&self) -> &str;
    fn handle(&self, command: &Command) -> Result<Response, DispatchError>;
}

pub struct Bus<'a> { handlers: Vec<Box<dyn Handler + 'a>> }
impl<'a> Bus<'a> {
    pub fn new() -> Self { Self { handlers: Vec::new() } }
    pub fn register<H: Handler + 'a>(&mut self, handler: H) { self.handlers.push(Box::new(handler)); }
    pub fn dispatch(&self, command: &Command) -> Result<Response, DispatchError> {
        self.handlers.iter()
            .find(|handler| handler.command_name() == command.name)
            .ok_or_else(|| DispatchError::Unknown(command.name.clone()))?
            .handle(command)
    }
    pub fn names(&self) -> impl Iterator<Item = &str> {
        self.handlers.iter().map(|h| h.command_name())
    }
}
impl Default for Bus<'_> { fn default() -> Self { Self::new() } }

pub struct Echo;
impl Handler for Echo {
    fn command_name(&self) -> &str { "echo" }
    fn handle(&self, command: &Command) -> Result<Response, DispatchError> { Ok(Response(command.payload.clone())) }
}

pub struct Prefixed<'a> { pub name: &'a str, pub prefix: &'a str }
impl Handler for Prefixed<'_> {
    fn command_name(&self) -> &str { self.name }
    fn handle(&self, command: &Command) -> Result<Response, DispatchError> {
        Ok(Response(format!("{}{}", self.prefix, command.payload)))
    }
}

pub struct RejectEmpty;
impl Handler for RejectEmpty {
    fn command_name(&self) -> &str { "nonempty" }
    fn handle(&self, command: &Command) -> Result<Response, DispatchError> {
        if command.payload.is_empty() { Err(DispatchError::Rejected("empty payload".into())) }
        else { Ok(Response(command.payload.clone())) }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn dispatches_heterogeneous_handlers_in_registration_order() {
        let prefix = "answer=";
        let mut bus = Bus::new();
        bus.register(Echo);
        bus.register(Prefixed { name: "prefix", prefix });
        assert_eq!(bus.names().collect::<Vec<_>>(), vec!["echo", "prefix"]);
        assert_eq!(bus.dispatch(&Command { name: "prefix".into(), payload: "42".into() }), Ok(Response("answer=42".into())));
    }
    #[test] fn unknown_is_typed_error() {
        let bus = Bus::new();
        assert_eq!(bus.dispatch(&Command { name: "x".into(), payload: String::new() }), Err(DispatchError::Unknown("x".into())));
    }
}

#![allow(dead_code)]
struct Request<B> { body: B }
struct Response<B> { body: B }
async fn handle(request: Request<String>) -> Response<String> { Response { body: request.body.to_uppercase() } }
fn main() { let future = handle(Request { body: "ok".into() }); drop(future); }

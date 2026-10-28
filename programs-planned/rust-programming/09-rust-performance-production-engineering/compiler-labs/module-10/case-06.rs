#[derive(PartialEq)] enum Stage{Canary,Full} fn promote(stage:Stage)->Stage{match stage{Stage::Canary=>Stage::Full}} fn main(){let _=promote(Stage::Canary);}

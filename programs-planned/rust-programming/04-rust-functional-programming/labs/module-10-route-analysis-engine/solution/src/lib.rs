#![forbid(unsafe_code)]

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Leg {
    pub route: String,
    pub from: String,
    pub to: String,
    pub distance: u64,
    pub line: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Diagnostic {
    FieldCount { line: usize },
    InvalidDistance { line: usize, value: String },
    EmptyRoute { route: String },
    Disconnected {
        route: String,
        line: usize,
        expected: String,
        found: String,
    },
    Overflow { route: String },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RouteSummary {
    pub route: String,
    pub origin: String,
    pub destination: String,
    pub legs: usize,
    pub distance: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Analysis {
    pub accepted: Vec<RouteSummary>,
    pub diagnostics: Vec<Diagnostic>,
}

pub fn parse_line(line: usize, text: &str) -> Result<Leg, Diagnostic> {
    let fields: Vec<_> = text.split('|').collect();
    if fields.len() != 4 {
        return Err(Diagnostic::FieldCount { line });
    }
    let distance = fields[3]
        .parse()
        .map_err(|_| Diagnostic::InvalidDistance {
            line,
            value: fields[3].to_owned(),
        })?;
    Ok(Leg {
        route: fields[0].to_owned(),
        from: fields[1].to_owned(),
        to: fields[2].to_owned(),
        distance,
        line,
    })
}

pub fn parse_all<'a, I>(lines: I) -> Result<Vec<Leg>, Diagnostic>
where
    I: IntoIterator<Item = &'a str>,
{
    lines
        .into_iter()
        .enumerate()
        .map(|(index, line)| parse_line(index + 1, line))
        .collect()
}

pub fn inspect_all<'a, I>(lines: I) -> (Vec<Leg>, Vec<Diagnostic>)
where
    I: IntoIterator<Item = &'a str>,
{
    lines.into_iter().enumerate().fold(
        (Vec::new(), Vec::new()),
        |(mut accepted, mut diagnostics), (index, line)| {
            match parse_line(index + 1, line) {
                Ok(leg) => accepted.push(leg),
                Err(error) => diagnostics.push(error),
            }
            (accepted, diagnostics)
        },
    )
}

fn summarize(route: String, legs: Vec<Leg>) -> Result<RouteSummary, Diagnostic> {
    let mut legs = legs.into_iter();
    let Some(first) = legs.next() else {
        return Err(Diagnostic::EmptyRoute { route });
    };
    let origin = first.from;
    let mut destination = first.to;
    let mut distance = first.distance;
    let mut count = 1;

    for leg in legs {
        if leg.from != destination {
            return Err(Diagnostic::Disconnected {
                route,
                line: leg.line,
                expected: destination,
                found: leg.from,
            });
        }
        destination = leg.to;
        distance = distance
            .checked_add(leg.distance)
            .ok_or_else(|| Diagnostic::Overflow {
                route: route.clone(),
            })?;
        count += 1;
    }

    Ok(RouteSummary {
        route,
        origin,
        destination,
        legs: count,
        distance,
    })
}

pub fn analyze(legs: Vec<Leg>, mut diagnostics: Vec<Diagnostic>) -> Analysis {
    let mut groups: BTreeMap<String, Vec<Leg>> = BTreeMap::new();
    for leg in legs {
        groups.entry(leg.route.clone()).or_default().push(leg);
    }

    let mut accepted = Vec::new();
    for (route, legs) in groups {
        match summarize(route, legs) {
            Ok(summary) => accepted.push(summary),
            Err(error) => diagnostics.push(error),
        }
    }
    Analysis {
        accepted,
        diagnostics,
    }
}

pub fn query<'a>(
    analysis: &'a Analysis,
    prefix: &'a str,
    max_distance: Option<u64>,
) -> impl Iterator<Item = &'a RouteSummary> + 'a {
    analysis.accepted.iter().filter(move |summary| {
        let within_distance = match max_distance {
            Some(maximum) => summary.distance <= maximum,
            None => true,
        };
        summary.route.starts_with(prefix) && within_distance
    })
}

fn render_diagnostic(diagnostic: &Diagnostic) -> String {
    match diagnostic {
        Diagnostic::FieldCount { line } => format!("ERR\tline {line}\tfield-count"),
        Diagnostic::InvalidDistance { line, value } => {
            format!("ERR\tline {line}\tinvalid-distance\t{value}")
        }
        Diagnostic::EmptyRoute { route } => format!("ERR\t{route}\tempty-route"),
        Diagnostic::Disconnected {
            route,
            line,
            expected,
            found,
        } => format!(
            "ERR\t{route}\tline {line}\tdisconnected\texpected={expected}\tfound={found}"
        ),
        Diagnostic::Overflow { route } => format!("ERR\t{route}\toverflow"),
    }
}

pub fn render(analysis: &Analysis) -> String {
    analysis
        .accepted
        .iter()
        .map(|summary| {
            format!(
                "OK\t{}\t{}\t{}\t{}\t{}",
                summary.route,
                summary.origin,
                summary.destination,
                summary.legs,
                summary.distance
            )
        })
        .chain(analysis.diagnostics.iter().map(render_diagnostic))
        .collect::<Vec<_>>()
        .join("\n")
}

pub fn exit_class(analysis: &Analysis) -> u8 {
    if analysis.diagnostics.is_empty() { 0 } else { 1 }
}

#[cfg(test)]
mod tests {
    use super::{
        Diagnostic, RouteSummary, analyze, exit_class, inspect_all, parse_all, query, render,
    };

    #[test]
    fn empty_route_group_is_a_typed_reducer_error() {
        assert_eq!(
            super::summarize("r".to_owned(), vec![]),
            Err(Diagnostic::EmptyRoute {
                route: "r".to_owned(),
            })
        );
    }

    #[test]
    fn valid_route_reduces_in_source_order() {
        let legs = parse_all(["r1|a|b|2", "r1|b|c|3"]).unwrap();
        let analysis = analyze(legs, vec![]);
        assert_eq!(analysis.accepted[0].distance, 5);
        assert_eq!(analysis.accepted[0].destination, "c");
        assert_eq!(exit_class(&analysis), 0);
    }

    #[test]
    fn parse_and_route_diagnostics_can_accumulate() {
        let (legs, diagnostics) = inspect_all(["r|a|b|2", "broken", "r|x|y|3"]);
        let analysis = analyze(legs, diagnostics);
        assert_eq!(analysis.diagnostics.len(), 2);
        assert_eq!(exit_class(&analysis), 1);
    }

    #[test]
    fn disconnected_route_is_not_partially_summarized() {
        let legs = parse_all(["r|a|b|2", "r|x|y|3"]).unwrap();
        let analysis = analyze(legs, vec![]);
        assert!(analysis.accepted.is_empty());
        assert!(matches!(analysis.diagnostics[0], Diagnostic::Disconnected { .. }));
    }

    #[test]
    fn lazy_query_preserves_summary_storage() {
        let analysis = super::Analysis {
            accepted: vec![
                RouteSummary {
                    route: "red".to_owned(),
                    origin: "a".to_owned(),
                    destination: "b".to_owned(),
                    legs: 1,
                    distance: 4,
                },
                RouteSummary {
                    route: "blue".to_owned(),
                    origin: "a".to_owned(),
                    destination: "c".to_owned(),
                    legs: 1,
                    distance: 9,
                },
            ],
            diagnostics: vec![],
        };
        assert_eq!(query(&analysis, "r", Some(5)).count(), 1);
        assert_eq!(analysis.accepted.len(), 2);
    }

    #[test]
    fn rendering_is_deterministic() {
        let legs = parse_all(["z|a|b|1", "a|x|y|2"]).unwrap();
        let analysis = analyze(legs, vec![]);
        assert_eq!(render(&analysis), render(&analysis));
        assert!(render(&analysis).starts_with("OK\ta\t"));
    }
}

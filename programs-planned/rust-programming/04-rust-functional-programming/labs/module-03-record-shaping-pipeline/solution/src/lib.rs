#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Survey {
    pub payload: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Observation {
    pub record_index: usize,
    pub field_index: usize,
    pub label: String,
    pub score: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ShapeError {
    LengthMismatch { labels: usize, scores: usize },
    MissingLabel { field: usize },
    MissingScore { field: usize },
    InvalidScore { field: usize, value: String },
}

pub fn fields(surveys: &[Survey]) -> impl Iterator<Item = (usize, usize, &str)> {
    surveys
        .iter()
        .enumerate()
        .filter_map(|(record_index, survey)| {
            survey
                .payload
                .as_deref()
                .map(|payload| (record_index, payload))
        })
        .flat_map(|(record_index, payload)| {
            payload
                .split(',')
                .enumerate()
                .map(move |(field_index, value)| (record_index, field_index, value.trim()))
        })
        .filter(|(_, _, value)| !value.is_empty())
}

pub fn shape(
    record_index: usize,
    labels: &str,
    scores: &str,
) -> Result<Vec<Observation>, ShapeError> {
    let labels: Vec<_> = labels.split(',').map(str::trim).collect();
    let raw_scores: Vec<_> = scores.split(',').map(str::trim).collect();

    if labels.len() != raw_scores.len() {
        return Err(ShapeError::LengthMismatch {
            labels: labels.len(),
            scores: raw_scores.len(),
        });
    }

    let mut observations = Vec::new();
    for (field_index, (label, raw_score)) in
        labels.into_iter().zip(raw_scores).enumerate()
    {
        match (label.is_empty(), raw_score.is_empty()) {
            (true, true) => continue,
            (true, false) => return Err(ShapeError::MissingLabel { field: field_index }),
            (false, true) => return Err(ShapeError::MissingScore { field: field_index }),
            (false, false) => {}
        }

        let score = raw_score
            .parse::<i64>()
            .map_err(|_| ShapeError::InvalidScore {
                field: field_index,
                value: raw_score.to_owned(),
            })?;
        observations.push(Observation {
            record_index,
            field_index,
            label: label.to_ascii_lowercase(),
            score,
        });
    }
    Ok(observations)
}

pub fn labels_with_aliases<'a>(
    primary: &'a [&'a str],
    aliases: &'a [&'a str],
) -> impl Iterator<Item = (&'static str, &'a str)> + 'a {
    primary
        .iter()
        .copied()
        .map(|value| ("primary", value))
        .chain(
            aliases
                .iter()
                .copied()
                .map(|value| ("alias", value)),
        )
}

#[cfg(test)]
mod tests {
    use super::{Observation, ShapeError, Survey, fields, labels_with_aliases, shape};

    #[test]
    fn filtering_preserves_original_positions() {
        let surveys = vec![
            Survey { payload: None },
            Survey {
                payload: Some(" a, ,b ".to_owned()),
            },
        ];
        assert_eq!(
            fields(&surveys).collect::<Vec<_>>(),
            vec![(1, 0, "a"), (1, 2, "b")]
        );
    }

    #[test]
    fn length_is_checked_before_zip_can_truncate() {
        assert_eq!(
            shape(0, "a,b", "1"),
            Err(ShapeError::LengthMismatch {
                labels: 2,
                scores: 1,
            })
        );
    }

    #[test]
    fn empty_pairs_are_skipped_without_renumbering_later_fields() {
        assert_eq!(
            shape(4, "a,,b", "1,,2").unwrap(),
            vec![
                Observation {
                    record_index: 4,
                    field_index: 0,
                    label: "a".to_owned(),
                    score: 1,
                },
                Observation {
                    record_index: 4,
                    field_index: 2,
                    label: "b".to_owned(),
                    score: 2,
                },
            ]
        );
    }

    #[test]
    fn one_sided_empty_slots_are_not_silently_repaired() {
        assert_eq!(shape(0, "a,,b", "1,x,2"), Err(ShapeError::MissingLabel { field: 1 }));
        assert_eq!(shape(0, "a,b", "1,"), Err(ShapeError::MissingScore { field: 1 }));
    }

    #[test]
    fn malformed_score_remains_a_typed_error() {
        assert_eq!(
            shape(2, "a", "x"),
            Err(ShapeError::InvalidScore {
                field: 0,
                value: "x".to_owned(),
            })
        );
    }

    #[test]
    fn valid_shape_preserves_record_and_field_identity() {
        assert_eq!(
            shape(1, " A,b ", "2,3").unwrap(),
            vec![
                Observation {
                    record_index: 1,
                    field_index: 0,
                    label: "a".to_owned(),
                    score: 2,
                },
                Observation {
                    record_index: 1,
                    field_index: 1,
                    label: "b".to_owned(),
                    score: 3,
                },
            ]
        );
    }

    #[test]
    fn aliases_follow_primary_labels_with_origin_metadata() {
        let labels: Vec<_> = labels_with_aliases(&["a", "b"], &["x"]).collect();
        assert_eq!(
            labels,
            vec![("primary", "a"), ("primary", "b"), ("alias", "x")]
        );
    }
}

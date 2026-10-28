use std::ops::{Add, Mul};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct BoundedIndex<const N: usize>(usize);

impl<const N: usize> BoundedIndex<N> {
    pub fn new(value: usize) -> Option<Self> {
        (value < N).then_some(Self(value))
    }

    pub fn get(self) -> usize {
        self.0
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Matrix<T, const R: usize, const C: usize> {
    cells: [[T; C]; R],
}

impl<T, const R: usize, const C: usize> Matrix<T, R, C> {
    pub fn new(cells: [[T; C]; R]) -> Self {
        Self { cells }
    }

    pub fn get(&self, row: BoundedIndex<R>, column: BoundedIndex<C>) -> &T {
        &self.cells[row.get()][column.get()]
    }

    pub fn iter(&self) -> impl Iterator<Item = &T> {
        self.cells.iter().flat_map(|row| row.iter())
    }
}

impl<T, const R: usize, const K: usize> Matrix<T, R, K>
where
    T: Copy + Default + Add<Output = T> + Mul<Output = T>,
{
    pub fn multiply<const C: usize>(&self, rhs: &Matrix<T, K, C>) -> Matrix<T, R, C> {
        let mut output = [[T::default(); C]; R];

        for (row_index, output_row) in output.iter_mut().enumerate() {
            for (column_index, output_cell) in output_row.iter_mut().enumerate() {
                let mut sum = T::default();
                for (left, right_row) in
                    self.cells[row_index].iter().zip(rhs.cells.iter())
                {
                    sum = sum + *left * right_row[column_index];
                }
                *output_cell = sum;
            }
        }

        Matrix::new(output)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn multiplication_checks_shape_in_the_type() {
        let left = Matrix::new([[1, 2], [3, 4]]);
        let right = Matrix::new([[5], [6]]);
        assert_eq!(left.multiply(&right), Matrix::new([[17], [39]]));
    }

    #[test]
    fn witness_rejects_zero_capacity() {
        assert!(BoundedIndex::<0>::new(0).is_none());
    }

    #[test]
    fn empty_inner_dimension_uses_the_documented_identity() {
        let left: Matrix<u64, 1, 0> = Matrix::new([[]]);
        let right: Matrix<u64, 0, 1> = Matrix::new([]);
        assert_eq!(left.multiply(&right), Matrix::new([[0]]));
    }

    #[test]
    fn iteration_is_row_major() {
        let matrix = Matrix::new([[1, 2], [3, 4]]);
        assert_eq!(matrix.iter().copied().collect::<Vec<_>>(), vec![1, 2, 3, 4]);
    }
}

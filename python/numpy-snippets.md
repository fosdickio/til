# NumPy Snippets

## Indexing
- [Indexing Documentation](https://numpy.org/doc/stable/reference/arrays.indexing.html)

```python
import numpy as np

# nd1[row, column]
nd1[3, 2]

# Select the first 3 rows (indices 0-2) and the second and third columns (indices 1-2)
nd1[0:3, 1:3]

# Select all of the rows in column 3
nd1[:, 3]

# Select the last cell
nd1[-1, -1]
```

## NumPy Arrays
- [Array Creation Documentation](https://numpy.org/doc/stable/user/basics.creation.html)
- [`array` Documentation](https://numpy.org/doc/stable/reference/generated/numpy.array.html)
- [`ndarray` Documentation](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html) - NumPy n-dimensional array type

```python
# List to 1D array
np.array([1, 2, 3]

# List of tuples to 2D array
np.array([(1, 2, 3), (4, 5, 6)]
```

- [`empty` Documentation](https://numpy.org/doc/stable/reference/generated/numpy.empty.html)
- [`ones` Documentation](https://numpy.org/doc/stable/reference/generated/numpy.ones.html)
- [`zeros` Documentation](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html)

```python
# Initialize 1D and 2D arrays with "empty" values (values may vary)
np.empty(5)
np.empty(3, 5)

# 1D and 2D arrays filled with 1s
np.ones(5)
np.ones(3, 5)

# 1D and 2D arrays filled with 0s
np.zeros(5)
np.zeros(3, 5)
```

- [Data Types Documentation](https://numpy.org/doc/stable/user/basics.types.html)

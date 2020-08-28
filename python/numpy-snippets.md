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

### Array Creation
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
```python
np.ones((5, 4), dtype=np.int_)
```

- [Random Sampling Documentation](https://numpy.org/doc/stable/reference/random/index.html)
```python
# Generate 2D random arrays of floats
np.random.random((5, 4))
np.random.rand(5, 4)

# Random 2D array with integers in [0, 10)
np.random.randint(0, 10, size=(2, 3))
```

### Array Attributes
- [`ndarray` Documentation](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
```python
a = np.random.random((5, 4))

a.shape[0] # Number of rows
a.shape[1] # Number of columns
len(a.shape) # Number of dimensions present in the array

a.size # Total number of elements
a.dtype # Data-type of the array
```

### Array Operations
- [Mathematical Functions Documentation](https://numpy.org/doc/stable/reference/routines.math.html)
```python
a = np.random.randint(0, 10, size=(5, 4))

a.sum() # Sum of all elements in the array
a.sum(axis=0) # Sum of each column
a.sum(axis=1) # Sum of each row

a.min(axis=0) # Minimum of each column
a.max(axis=1) # Maximum of each row
a.mean() # Mean of all elements in the array
```

- [Sorting/Searching/Counting Documentation](https://numpy.org/doc/stable/reference/routines.sort.html)


- [Boolean Array Indexing Documentation](https://numpy.org/doc/stable/reference/arrays.indexing.html#boolean-array-indexing)
```python
np.array([(20, 25, 10, 23, 26), (0, 2, 50, 20, 0)])
mean = a.mean()

# Replace values less than the mean with the mean
a[a < mean]
```

- [Arithmetic Operations Documentation](https://numpy.org/doc/stable/reference/routines.math.html#arithmetic-operations)
```python
a = np.array([(1, 2, 3, 4, 5), (10, 20, 30, 40, 50)])
b = np.array([(100, 200, 300, 400, 500), (1, 2, 3, 4, 5)])

# Addition
a + b

# Multiplication
a * 2
a * b

# Division
a / 2.0
a / b
```

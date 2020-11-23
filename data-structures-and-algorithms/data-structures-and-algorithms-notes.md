# Data Structures and Algorithms Notes

## Arrays and Linked Lists
- Arrays allow fast reads.
- Linked lists allow fast inserts and deletes.

## Recursion
- Every recursive function has two parts: the base case, and the recursive case.
  - The recursive case is when the function calls itself.
  - The base case is when the function doesn’t call itself again (so it doesn’t go into an ininite loop).

### The Stack
- All function calls go onto the call stack.

### Divide and Conquer
- Divide and conquer works by breaking a problem down into smaller and smaller pieces.  If you’re using divide and conquer on a list, the base case is probably an empty array or an array with one element.

### Quicksort
- If you’re implementing quicksort, choose a random element as the pivot.
- The average runtime of quicksort is O(n log n)!

### Hash Tables
- There are many diferent ways to deal with collisions.
  - The simplest one is this: if multiple keys map to the same slot, start a linked list at that slot.
- Hash tables are as fast as arrays at searching (getting a value at an index).
- Hash tables are as fast as linked lists at inserts and deletes.
- In the worst case, hash tables are slow at searching, insters, and deletes, so it’s important that you don’t hit worst-case performance with hash tables.
  - To avoid worst-case performance, you need to avoid collisions. To avoid collisions, you need:
    - A low load factor
    - A good hash function
- You can make a hash table by combining a hash function
with an array.

### Dijkstra's Algorithm
- Breadth-first search is used to calculate the shortest path for an unweighted graph.
- Dijkstra’s algorithm is used to calculate the shortest path for a weighted graph.
- Dijkstra’s algorithm works when all the weights are positive.
- If you have negative weights, use the Bellman-Ford algorithm.

### Greedy Algorithms
- Greedy algorithms optimize locally, hoping to end up with a global optimum.
- NP-complete problems have no known fast solution.
- If you have an NP-complete problem, your best bet is to use an approximation algorithm.
- Greedy algorithms are easy to write and fast to run, so they make good approximation algorithms.

# Compiler Notes

## Introduction

```sh
# Compile and run a C program
cc fact.c -o fact.exe
./fact.exe

# See machine code for a C program
cc fact.c -S
```

The [Compiler Explorer](https://godbolt.org/) works great for seeing different types of code compiled for different CPU architectures.

```py
# Look at simulated CPU (virtual machine) code in Python
import dis

dis(fact)
```

**Classic Approach:** Source &rarr; Tokens &rarr; Parse Tree &rarr; Checking (Types) &rarr; Code Generation

```sh
# See how Python tokenizes pieces of code
python3 -m tokenize fact.py

# See parse tree data structure in Python
python -m ast fact.py
```

You can use LLVM to generate machine code for different CPU architectures.

```sh
clang fact.ll -o out.exe

# Generate assembly code in fact.s
clang -S fact.c
cat fact.c
```

```sh
# View the compiler phases for the Scala compiler (modern compilers are much more involved than just the classic approach)
scalac -Xshow-phases
```

## Compiler Optimization

| Optimization             | Before                                                      | After                | Considerations                                                                                        |
| ------------------------ | ----------------------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------- |
| Constant Folding         | `print 23 + 45;`                                            | `print 68;`          |                                                                                                       |
| Algebraic Simplification | `print (x * y) + (x * y)`                                   | `print 2 * (x * y);` |                                                                                                       |
| Function Inlining        | `func square(x) { return x * x };` <br> `print square(10);` | `print 100;`         | - Size of function (small functions preferred) <br> - Side effects (mutation of variables, I/O, etc.) |

## Syntatic Sugar

-   "Syntatic sugar" is nice for the programmer, but not really needed.
-   New features can be implemented using existing features

| Syntatic Sugar     | Before                                                            | After                                                                                  |
| ------------------ | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| De-initialization  | `var x = 1 + y;`                                                  | `var x;` <br> `x = y + y;`                                                             |
| Syntax Translation | `for (var x = 1; x < 10; x = x + 1) {` <br> &emsp; `...` <br> `}` | `var x = 1;` <br> `while x < 10 {` <br> &emsp; `...` <br> &emsp; `x = x + 1;` <br> `}` |

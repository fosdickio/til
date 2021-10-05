# An Introduction to C

## A Brief History

The C programming language was developed in 1972 by Dennis Ritchie and Ken Thompson at Bell Telephone Laboratories.

In 1990, the ANSI C Standard was adopted (unchanged) by a joint technical committee of the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC) and published as the first edition of the C Standard, C90 (ISO/IEC 9899:1990). The second edition of the C Standard, C99, was published in 1999 (ISO/IEC 9899:1999), and a third edition, C11, in 2011 (ISO/IEC 9899:2011). The latest version of the C Standard (as of this writing) is the fourth version, published in 2018 as C17 (ISO/IEC 9899:2018). A new major revision referred to as C2x is under development by ISO/IEC. According to 2018 polling data from JetBrains, 52 percent of C programmers use C99, 36 percent use C11, and 23 percent use an embedded version of C.

## The C Standard

The C Standard (ISO/IEC 9899:2018) defines the language and is the final authority on language behavior. A good choice (in 2019) with GCC 8 and later is `-std=c17`.

## Getting Started

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  puts("Hello, world!");
  return EXIT_SUCCESS;
}
```

### Preprocessor Directives

`<stdio.h>` contains the declarations for C Standard I/O functions, and `<stdlib.h>` contains the declarations for general utility functions.

### The _main_ Function

The `main` function defines the main entry point for the program that’s executed in a hosted environment when the program is invoked from the command line or from another program. C defines two possible execution environments: freestanding and hosted. A freestanding environment may not provide an operating system and is typically used in embedded programming.

The `puts` function is a C Standard Library function that writes a string argument to `stdout`, which typically represents the console or terminal window, and appends a newline character to the output. `"Hello, world!"` is a string literal that behaves like a read-only string.

`EXIT_SUCCESS` is an object-like macro that commonly expands to 0 and is typically defined as follows:

```c
#define EXIT_SUCCESS 0
```

Each occurrence of `EXIT_SUCCESS` is replaced by a 0, which is then returned to the host environment from the call to `main`.

### Checking Function Return Values

The `puts` function returns the value of the macro `EOF` (a negative integer) if a write error occurs; otherwise, it returns a nonnegative integer value.

Although it’s unlikely that the `puts` function will fail and return `EOF` for a simple program, it’s possible.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  if (puts("Hello, world!") == EOF) {
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
```

### Formatted Output

The `puts` function is a nice, simple way to write a string to `stdout`, but eventually you’ll need to print formatted output by using the `printf` function — for example, to print arguments other than strings. The `printf` function takes a format string that defines how the output is formatted, followed by a variable number of arguments that are the actual values you want to print.

```c
printf("%s\n", "Hello, world!");
```

The `printf` function returns status differently than the `puts` function. The `printf` function returns the number of characters printed if it’s successful, or a negative value if an output or encoding error occurred.

## GNU Compiler Collection

The GNU Compiler Collection (GCC) includes frontends for C, C++, and Objective-C, as well as other languages (https://gcc.gnu.org/).

GCC has been adopted as the standard compiler for Linux systems, although versions are also available for Microsoft Windows, macOS, and other platforms.

## Portability

Five kinds of portability issues are enumerated in Annex J of the C Standard documents:

- Implementation-defined behavior
- Unspecified behavior
- Undefined behavior
- Locale-specific behavior
- Common extensions

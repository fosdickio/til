# Go Notes

## Background
- Go was conceived in September 2007 by Robert Griesemer, Rob Pike, and Ken Thompson, all at Google, and was announced in November 2009.
- The goals of the language and its accompanying tools were to be expressive, efficient in both compilation and execution, and effective in writing reliable and robust programs.
- The Go project includes the language itself, its tools and standard libraries, and a cultural agenda of radical simplicity.
- It has garbage collection, a package system, first-class functions, lexical scope, a system call interface, and immutable strings in which text is generally encoded in UTF-8.
- It has comparatively few features and is unlikely to add more.
- The language is mature and stable, and guarantees backwards compatibility: older Go programs can be compiled and run with newer versions of compilers and standard libraries.

## Introduction
- Go natively handles Unicode, so it can process text in all the world's languages.
- Package `main` is special. It defines a stand alone executable program, not a library.
- The `gofmt` tool rewrites code into the standard format, and the `go` tool’s `fmt` subcommand applies `gofmt` to all the files in the specified pack- age, or the ones in the current directory by default.
- A slice expression of the form `s[m:n]` yields a slice that refers to elements `m` through `n-1`.
  - If `m` or `n` is omitted, it defaults to `0` or `len(s)` respectively (so we can abbreviate the desired slice as `os.Args[1:]`).
- A variable can be initialized as part of it's declaration.
  - If it is not explicitly initialized, it is implicitly initialized to the zero value for it's type (`0` for numeric types and the empty string `""` for strings).
- The `:=` symbool is part of a short variable declaration, a statement that declares one or more variables and gives them appropriate types based on the initializer values.
- The `for` loop is the only loop statement in Go.
  - Parentheses are never used around the components of a `for` loop.

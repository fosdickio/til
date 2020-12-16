# Elixir Notes

## Installation
```bash
brew update && brew install erlang elixir
elixir --version
```

## Mix Projects

### Create a Mix Project
```bash
mix new project_name
```

## Running Projects

### Run an Elixir File
The file gets compiled into bytecode (in memory) and then run on an Erlang virtual machine. 
```bash
elixir lib/project_name.ex
```

### IEX (Interactive Elixir)
Fire up an `iex` (Interactive Elixir) session and then use the `c` helper function to compile and run the file.  The `c` helper function compiles the given file in memory, the module is loaded into the session, and any code outside of the module is interpreted. 
```bash
iex
iex> c "lib/project_name.ex"
```

Alternatively, you can tell `iex` to interpret an Elixir file while starting by passing the relative path of the file:.
```bash
iex lib/project_name.ex
```

When you start a standard `iex` session, it doesn't know about the paths and dependencies of a `mix` project. So, to start a session in the context of a project, you need to pass the `-S mix` option.
```bash
iex -S mix
```

Finally, to recompile a module while in `iex`, use the `r` helper function.
```bash
iex> r Servy
```

To see all the helper functions at your disposal, use the `h` helper function.
```bash
iex> h
```

## High-Level Transformations

### Nested Function Calls
The following examples are 3 different ways of writing the same code.
```bash
# Intermediate variables
def handle(request) do
  conv = parse(request)
  conv = route(conv)
  format_response(conv)
end

# Nested function calls
format_response(route(parse(request)))

# Pipe operators
# Note: at compile time this code is transformed to the nested call version. 
request
|> parse
|> route
|> format_response
```

## Pattern Matching

### Terms
A term is a value of any data type: a string, an atom, a map, a list, etc.

### Atoms / Maps
Elixir atoms are prefixed by a colon.  For example, below is a map that uses atoms as keys.
```bash
%{ :method => "GET", :path => "/wildthings" }
```

It's so common to use atoms as keys that Elixir gives us a shortcut.
```bash
%{ method: "GET", path: "/wildthings" }
```

If the keys are anything but atoms, you must use the general `=>` form. For example, below is a map with strings as keys.
```bash
%{ "method" => "GET", "path" => "/wildthings" }
```

## Immutable Data
Programming with immutable data is a hallmark of functional programming.

### Accessing Map Values with Atoms vs. Strings

Suppose we have the following map defined in an iex session:
In the below map, the keys are atoms, so to get the values associated with the keys we can use the square-bracket syntax.
```bash
iex> conv = %{ method: "GET", path: "/wildthings" }

iex> conv[:path]
"/wildthings"
```

When the keys are atoms, you can also use the dot notation.
```bash
iex> conv.path
"/wildthings"
```

Supposing that we instead use strings for the map keys, we must use strings with the square-bracket syntax.
```bash
iex> conv = %{ "method" => "GET", "path" => "/wildthings" }

iex> conv["path"]
"/wildthings"
```

### Bytes
A sequence of bytes in Elixir is referred to as a binary.  Double-quoted Elixir strings are represented internally as a sequence of bytes.  Thus, double-quoted strings are binaries.

A string is a UTF-8 encoded binary.  As an example, the character "ö" takes 2 bytes to be represented in UTF-8.  So, even though the string has 20 characters, the number of bytes in that string is 21.

```bash
iex> resp_body = "Bears, Liöns, Tigers"
"Bears, Liöns, Tigers"

iex> String.length(resp_body)
20

iex> byte_size(resp_body)
21
```

## Function Clauses
In Elixir you don't use conditional expressions as often as you would in imperative languages.  Instead, it's more idiomatic to control the flow of a program using function clauses and pattern matching.

### Regular Expressions
To define a regular expression literal in Elixir, `~r` is called a sigil and the braces `{ }` are delimiters for the regular expression itself.
```bash
~r{regexp}
```

The ~r is called a sigil and the braces { } are delimiters for the regular expression itself. For example, here's a regular expression that matches /bears?id=1, /lions?id=7, /tigers?id=100, and so on:
```bash
iex> regex = ~r{\/(\w+)\?id=(\d+)}
```

The example below matches a literal / character followed by one or more word characters, followed by the literal ?id= followed by one or more digits.
```bash
iex> regex = ~r{\/(\w+)\?id=(\d+)}
iex> Regex.match?(regex, path)
true

iex> regex = ~r{\/(?<thing>\w+)\?id=(?<id>\d+)}
iex> Regex.named_captures(regex, path)
%{"id" => "1", "thing" => "bears"}`
```

## Files and Paths
The `File` and `Path` modules define familiar functions for working with files and paths.

You can expand the path to the pages directory relative to the directory of the current file (`__DIR__`) like so:
```bash
@pages_path Path.expand("../../pages", __DIR__)
```

If you're running the application using `iex -S mix`, you can optionally expand the path using a slightly different approach.  `File.cwd!` returns the current working directory. 
```bash
@pages_path Path.expand("pages", File.cwd!)
```

## Organizing Code

### Import Options
By default, when you use import it imports all the module's functions and macros into the current namespace.  You can use the only option to explicitly import specific functions.  Using only is optional, but it's recommended so as to avoid importing all the functions into the current namespace and potentially ending up with name collisions.
```bash
import Servy.Parser, only: [parse: 1]
```

Conversely, there's a rarely used except option to import all the functions except those that are specified.  Using the `:functions` atom imports only functions whereas using the `:macros` atom only imports macros. 
```bash
import SomeModule, only: :functions
import SomeModule, only: :macros
```

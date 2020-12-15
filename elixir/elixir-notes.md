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
The following examples are 3 different ways of writing the same code
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

## Terms
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

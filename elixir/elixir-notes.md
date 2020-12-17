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

## Modeling with Structs

### Keyword Lists
Keywords lists are just a tiny dose of syntactic sugar.  Internally, keyword lists are represented as a list of tuples containing two values: an atom (the key) and the associated value.
```bash
# Keyword List
[ method: "", path: "", resp_body: "", status: nil ]

# How it looks internally
[ {:method, ""}, {:path, ""}, {:resp_body, ""}, {:status, nil} ]
```

Keyword lists are most commonly used as a simple list of options. In contrast, maps are the go-to data structure for storing key/value pairs.

### Updating Structs
The syntax for updating a struct is just like updating a map.

```bash
# Verify that the argument is a Conv struct.
%Conv{ method: "GET", path: "/wildthings" } = conv

# Stipulate a Conv struct.
# This verifies that the value being updated (conv) is indeed a struct of the type Conv, not a generic map.
# This is yet another compile-time check that comes with using a struct as compared to a map. 
%Conv{ conv | status: 200, resp_body: "Bears, Lions, Tigers" }
```

## Heads and Tails

### Lists
A list in Elixir is implemented as a series of linked lists.  The head is always the first element of the list.  The tail "points" or "links" to the list that consists of the head and tail of the remaining elements.  So, lists are by definition recursive data structures.

The familiar way to make a list is by separating each element by a comma.
```bash
iex> nums = [1, 2, 3]
[1, 2, 3]
```

But now you know that a list is either empty or it consists of a head and a tail which is itself a list.  It follows then that you can create the same list using the `[head | tail]` expression.
```bash
iex> nums = [1 | [2, 3]]
[1, 2, 3]
```

In the same way, you can add elements to the head of a list (prepend) using the [head | tail] expression.
```bash
iex> [0 | nums]
[0, 1, 2, 3]
```

### Accessing Head and Tail
```bash
iex> [head | tail] = [1, 2, 3]
iex> head
1
iex> tail
[2, 3]
```

The head and tail of a list can also be accessed with the functions hd and tl:
```bash
iex> nums = [1, 2, 3]

iex> hd(nums)
1

iex> tl(nums)
[2, 3]
```

## Recursion
```elixir
defmodule Recurse do
  def loopy([head | tail]) do
    IO.puts "Head: #{head} Tail: #{inspect(tail)}"
    loopy(tail)
  end

  def loopy([]), do: IO.puts "Done!"
end

Recurse.loopy([1, 2, 3, 4, 5])
```

### Tail-Call Optimization
Elixir performs tail-call optimization to keep the memory footprint of recursion to a minimum.  When the last thing a function does is call itself (a tail call), Elixir performs tail-call optimization.  This doesn't push any new frames onto the call stack, so no additional memory is consumed.
```elixir
defmodule Recurse do

  # The triple/1 function is a public function which calls the private triple/2 
  # function with the list of numbers and an accumulator (current_list) that 
  # starts off as an empty list ([]).
  def triple(list) do
    triple(list, [])
  end

  # The first triple/2 function head matches a non-empty list of numbers and 
  # calls itself (a tail call) with the list's tail and a new list where the 
  # head is the original head multiplied by 3 and the tail is the current 
  # accumulator list.
  defp triple([head|tail], current_list) do
    triple(tail, [head*3 | current_list])
  end

  # Finally, the second triple/2 function head (the terminal clause) matches an 
  # empty list and returns the list of accumulated numbers reversed. It needs 
  # to be reversed because each tripled number was added to the head of the 
  # accumulator list: [head*3 | current_list].
  defp triple([], current_list) do
    current_list |> Enum.reverse()
  end
end

IO.inspect Recurse.triple([1, 2, 3, 4, 5])
```

## Enum
Enum provides a set of algorithms to work with enumerables.  In Elixir, an enumerable is any data type that implements the Enumerable
protocol.  Lists (`[1, 2, 3]`), Maps (`%{foo: 1, bar: 2}`) and Ranges (`1..3`) are
common data types used as enumerables.

### Capturing Expressions
You can use the `&` operator to capture named functions.  For example, below is an example of capturing the `String.upcase` function.
```elixir
> phrases = ["lions", "tigers", "bears", "oh my"]

> Enum.map(phrases, &String.upcase(&1))
["LIONS", "TIGERS", "BEARS", "OH MY"]
```

The `&` capture operator creates an anonymous function that calls `String.upcase`.  The `&1` is a placeholder for the first argument passed to the function.  It's shorthand for the below code.
```elixir
> Enum.map(phrases, fn(x) -> String.upcase(x) end)
["LIONS", "TIGERS", "BEARS", "OH MY"]
```

You can also use the `&` operator to capture expressions.  Take an example where we triple a list of numbers by calling `map` with a list and an anonymous "tripler" function.
```elixir
> Enum.map([1, 2, 3], fn(x) -> x * 3 end)
[3, 6, 9]

# Shorthand version using the & capture operator
> Enum.map([1, 2, 3], &(&1 * 3))
[3, 6, 9]
```

Alternatively, you can capture the expression as an anonymous function, bind it to a variable, and then pass the function to the higher-order map function.
```elixir
> triple = &(&1 * 3)
#Function<6.118419387/1 in :erl_eval.expr/5>

> Enum.map([1, 2, 3], triple)
[3, 6, 9]
```

## Comprehensions

### EEX
EEx must be declared as a dependency. To do that, edit `mix.exs` to add `:eex` to the `extra_applications` list inside the `application` function.
```elixir
def application do
  [
    extra_applications: [:logger, :eex]
  ]
end
```

In EEx, all expressions that output something to the template must use the equals sign (`=`).  In the below case, it's the comprehension that returns the final string that we want to inject into the template.  Thus, there is a need to use `<%=` rather than `<%` in order to have the result output to the template.
```elixir
<%= for bear <- bears do %>
  <li><%= bear.name %> - <%= bear.type %></li>
<% end %>
```

#### Inspecting in EEx Templates
The [`inspect` function](https://hexdocs.pm/elixir/Kernel.html#inspect/2) can be used to get a representation of a list and then output it to the template.  The `inspect` function is defined in the Kernel module and it's automatically imported.
```elixir
<%= inspect(bears) %>
```

#### Precompiling Templates
You can use the `EEx.eval_file` function to read a template file and evaluate the embedded Elixir using a set of bindings.  It's simple and it gets the job done.  However, if your aim was to write a high-performance web server, then using `eval_file` isn't a good choice because it has to read the template file from disk, parse it, and evaluate it every time the matching route is called.

Rather, we would like to precompile the template so that we can do all of the inefficient stuff once and then run a function every time the route is called.  The [EEx module](https://hexdocs.pm/eex/EEx.html) offers an easy way to do that.  The [`EEx.function_from_file/5` macro](https://hexdocs.pm/eex/EEx.html#function_from_file/5) generates a function definition from the file contents.
```elixir
defmodule Servy.BearView do
  require EEx

  @templates_path Path.expand("../../templates", __DIR__)

  EEx.function_from_file :def, :index, Path.join(@templates_path, "index.eex"), [:bears]
end
```

Notice the `index` function takes a `bears` argument.  At compile time, the `index` function is generated and it's body returns the pre-compiled template. 

### Pattern Matching Comprehensions
Imagine we have a list of tuples where the first element is a person's name and the second element indicates whether they prefer dogs or cats.  We can then use a pattern to destructure the tuples given to us by the generator in order to find all of the dog lovers.
```elixir
> prefs = [ {"Betty", :dog}, {"Bob", :dog}, {"Becky", :cat} ]

> for {name, :dog} <- prefs, do: name
["Betty", "Bob"]
```

We can also use filter expression to do the filtering.  Comprehensions have inherent support for a filter expression.  For example, here's how to get the dog lovers using a filter expression.
```elixir
> for {name, pet_choice} <- prefs, pet_choice == :dog, do: name
["Betty", "Bob"]
```

#### Atomize Keys
Let's say we have a map where our keys are strings, but we want to convert the keys to atoms.  By default, the values returned by the `do` block of a comprehension are packaged into a list.  However, you can use the `:into` option to package the returned values into any `Collectable` (and a map is a collectable).
```elixir
> style = %{"width" => 10, "height" => 20, "border" => "2px"}
> for {key, val} <- style, into: %{}, do: {String.to_atom(key), val}
%{border: "2px", height: 20, width: 10}
```

### Comprehensions with Multiple Generators
Comprehensions can have multiple generators which effectively act like nested loops.  Using multiple generators is a powerful way to combine lists of elements (or any enumerable).
```elixir
ranks = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A" ]
suits = [ "♣", "♦", "♥", "♠" ]

deck = for rank <- ranks, suit <- suits, do: {rank, suit}

IO.inspect deck
```

If we then wanted to deal 13 random cards from the deck, we could do the following.
```elixir
deck
|> Enum.shuffle
|> Enum.take(13)
|> IO.inspect
```

## Test Automation
```bash
# Run specific tests
mix test test/my_test1.exs test/my_test2.exs

# Run all tests
mix test

# Run a specific test by specifying a line number associated with it
mix test test/my_test.exs:7
```

### Doctests
Doctests are specified by an indentation of four spaces followed by the `iex>` prompt in a documentation string.  The expected result should start at the next line after `iex>` or `...>` line(s) and is terminated either by a newline or a new `iex>` prefix.
```elixir
defmodule KVServer.Command do
  @doc ~S"""
  Parses the given `line` into a command.

  ## Examples
      iex> KVServer.Command.parse("CREATE shopping\r\n")
      {:ok, {:create, "shopping"}}
  """
  def parse(_line) do
    ...
  end
end
```

To run our doctests, we’ll create a file at `test/kv_server/command_test.exs` and call `doctest KVServer.Command` in the test case.
```elixir
defmodule KVServer.CommandTest do
  use ExUnit.Case, async: true
  doctest KVServer.Command
end
```

### Assertion Macros
You can reference the [ExUnit assertions documentation](https://hexdocs.pm/ex_unit/ExUnit.Assertions.html) for more information regarding assertion macros.

### Speeding Up Tests
By default, ExUnit executes each test case (test file/module) serially.  Thus, as the number of test cases increases, so does the time it takes to execute those tests.  You can speed up the execution of multiple test cases by running them concurrently rather than serially.  To allow a test case to run concurrently, simply set the `async` option to `true` on this existing line.
```elixir
use ExUnit.Case, async: true
```

It's important to note that individual tests within the test case are always run serially. Setting async to true allows the test case as a whole to run in parallel with other test cases.  It's important to note that you won't be able to use this trick if a test case accesses shared state or resources with another test cases.

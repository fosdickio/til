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

## External Libraries
You can add external dependencies in your project's `mix.exs` file (using a list of tuples).  They can then be installed using `mix deps.get`.

For an update on version formatting, type `h Version` in an `iex` session to see a list of examples and explanations. 

## Erlang |> Elixir
Here's a summary of things to keep in mind when transcoding Erlang to Elixir:
- Erlang atoms start with a lowercase letter, whereas Elixir atoms start with a colon (`:)`. For example, `ok` in Erlang becomes `:ok` in Elixir.
- Erlang variables start with an uppercase letter, whereas Elixir variables start with a lowercase letter.  For example, `Socket` in Erlang becomes `socket` in Elixir.
- Erlang modules are always referenced as atoms.  For example, `gen_tcp` in Erlang becomes `:gen_tcp` in Elixir.
- Function calls in Erlang use a colon (`:`) whereas function calls in Elixir always us a dot (`.`).  For example, `gen_tcp:listen` in Erlang becomes `:gen_tcp.listen` in Elixir.
- It's important to note that **Erlang strings aren't the same as Elixir strings**.  In Erlang, a double-quoted string is a list of characters whereas in Elixir a double-quoted string is a sequence of bytes (a binary).  Thus, double-quoted Erlang and Elixir strings aren't compatible.  So, if an Erlang function takes a string argument, you can't pass it an Elixir string.  Instead, Elixir has a character list which you can create using single-quotes rather than double-quotes.  For example, `'hello'` is a list of characters that's compatible with the Erlang string `"hello"`.

## Web Server Sockets
![Sockets](img/sockets.png)

## Concurrent, Isolated Processes
The `spawn/1` function takes a zero-arity anonymous function.
```elixir
spawn(fn() -> serve(client_socket) end)
```

There's also a `spawn/3` function that takes the module name, the function name (as an atom), and the list of arguments passed to the function.  This is commonly referred to as referred to as MFA (for module, function, arguments).
```elixir
spawn(Servy.HttpServer, :start, [4000])
```

In either case, `spawn` creates a process and immediately returns the PID of that process.  The process that called `spawn` does not block; it continues execution.  Meanwhile, the spawned process runs its function concurrently, in the background.  When that function returns, the spawned process exits normally and the Erlang VM takes care of cleaning up its memory.

### Spawning Multiple Processes
Just how lightweight and fast is it to spawn a single process? We're talking an initial memory footprint of 1-2 KB and a few microseconds to spawn. You can spawn thousands of processes on a single machine without the Erlang VM breaking a sweat.
```elixir
iex> Enum.map(1..10_000, fn(x) -> spawn(fn -> IO.puts x * x end) end)
```

### Erlang VM Observer
You can start the [Observer GUI](https://erlang.org/doc/apps/observer/observer_ug.html) using the below command.
```bash
iex> :observer:start
```

You can use the `inspect` function to print the PID of the current process.
```elixir
IO.puts "#{inspect self()}: Working on it!\n"
```

### Getting System Info
```elixir
# Get current process id
iex> self()

# 2 ways to count the number of processes
iex> Process.list |> Enum.count
iex> :erlang.system_info(:process_count)
```

## Sending and Receiving Messages
```elixir
caller_pid = self()
spawn(fn -> send(caller_pid, {:result, "My message"}) end)
Process.info(caller_pid, :messages)
receive do {:result, message} -> message end
```

`flush` consumes all the messages in the `iex` process' mailbox and prints them out.  It comes in handy when you're playing around in the `iex` shell and don't want to go through the trouble of receiving all the messages.
```elixir
iex> flush()
```

### Processes
- They are lightweight and fast to spawn
- They run concurrently, and even in parallel if you have multiple CPU cores
- They are isolated from other processes
- They don't share anything with other processes
- They have their own private mailbox
- They communicate with other processes only by sending and receiving messages

### Scheduler
The Erlang VM scheduler allocates a slice of CPU time to a process. And when that time is up, the scheduler pre-empts (suspends) the running process and allocates time to another process. In this way, the scheduler tries its best to be fair to all processes. 

Suppose during its allocated time that a process calls `receive` and has to wait for a message to arrive.  The scheduler knows that it would be a waste of precious CPU cycles to continue allocating time to that blocked process.  So, the scheduler pre-empts (suspends) the blocked process before it's scheduled time is up.  That way, other processes that want to do actual work aren't held up by a process that's just waiting around.

The same is true for a process that calls `:timer.sleep` or runs an I/O operation such as `File.read`.  There is no sense in giving that process any more CPU time.  The scheduler dutifully pre-empts the process and then resumes it when the process wakes back up or finishes the I/O operation.

### Send a Request to an API
```elixir
iex> {:ok, response} = HTTPoison.get "https://jsonplaceholder.typicode.com/users/1"

iex> response.body
"{
  "id": 1,
  ...
}"

body_map = Poison.Parser.parse!(response.body, %{})

iex> city = body_map |> Map.get("address") |> Map.get("city")
"Gwenborough"

iex> city = get_in(body_map, ["address", "city"])
"Gwenborough"
```

## Asynchronous Tasks
```elixir
task = Task.async(fn -> Servy.Tracker.get_location("bigfoot") end)

task = Task.async(Servy.Tracker, :get_location, ["bigfoot"])
```

### After Clauses
```elixir
def get_result(pid) do
  receive do
    {^pid, :result, value} -> value
  after 2000 ->
    raise "Timed out!"
  end
end
```

### Task Timeouts
By default, `Task.await` has a built-in timeout of 5 seconds.  If the task doesn't complete within that time, an exception is raised.  You can override the default timeout by passing a specific timeout value (in milliseconds) as the second argument to `Task.await`.
```elixir
iex> task = Task.async(fn -> :timer.sleep(7000); "Done!" end)

iex> Task.await(task, 7000)
"Done!"
```

### Running a Task with a Cut-Off Time
`Task.await` waits for a message to arrive, you can only call `Task.await` once for any given task.  In certain situations you may want to be able to check if a long-running task has finished.  That's where `Task.yield` comes in handy.

The first time we call `Task.yield`, it starts waiting for 5 seconds and because a message doesn't arrive by that cut-off time, `nil` is returned. Then we call `Task.yield` again which starts waiting for 5 seconds and, because a message arrives during that time, the tuple `{:ok, "Done"}` is returned.  In this way, you can check if a long-running task has finished or not and act accordingly.
```elixir
case Task.yield(task, 5000)
  {:ok, result} ->
    result
  nil ->
    Logger.warn "Timed out!"
    Task.shutdown(task)
end
```

In this example, if a message doesn't arrive within the 5 second cut-off, then we shut down the task by calling `Task.shutdown`.  If a message arrives while shutting down the task, then `Task.shutdown` returns `{:ok, result}`.  Otherwise, it returns `nil`.

## Stateful Server Processes

### Finding Registered Processes
```elixir
iex> Process.whereis(:pledge_server)
nil

iex> Process.register(pid, :pledgy)
true

iex> Process.whereis(:pledgy)
#PID<0.158.0>
```

### Agents
The [`Agent` module](https://hexdocs.pm/elixir/Agent.html) is a simple wrapper around a server process that stores state and offers access to that state through a thin client interface.  To start an agent, you call the `Agent.start` function and pass it a function that returns the initial state.
```elixir
iex> {:ok, agent} = Agent.start(fn -> [] end)
{:ok, #PID<0.90.0>}
```

That spawns a process that's holding onto an Elixir list in its memory.  Notice the agent variable is bound to a PID.

To add a pledge to the agent's state, you call the `Agent.update` function with a PID and a function that updates the state.
```elixir
iex> Agent.update(agent, fn(state) -> [ {"larry", 10} | state ] end)
:ok
```

Notice the function is passed the current state which the function then transforms into the new state. Let's add another pledge to the head of the list just to make things interesting:
```elixir
iex> Agent.update(agent, fn(state) -> [ {"moe", 20} | state ] end)
:ok

Then to retrieve the current state, you call the `Agent.get` function with a PID and a function that returns the state.
```elixir
iex> Agent.get(agent, fn(state) -> state end)
[{"moe", 20}, {"larry", 10}]
```

## OTP GenServer

### Task, Agent, or GenServer?
- Use a `Task` if you want to perform a one-off computation or query asynchronously.
- Use an `Agent` if you just need a simple process to hold state.
- Use a `GenServer` if you need a long-running server process that store states and performs work concurrently.
- Use a dedicated `GenServer` process if you need to serialize access to a shared resource or service used by multiple concurrent processes.
- Use a `GenServer` process if you need to schedule background work to be performed on a periodic interval.

### GenServer Callback Functions
Erlang's `gen_server` behavior expects the callback module to implement six callback functions.  Elixir's `GenServer` module conveniently provides default implementations of all six callback functions.  When you add `use GenServer `to a module, the default callbacks are injected into the module.  You then add application-specific behavior by overriding any of the default implementations. 

### Debugging and Tracing
Erlang has a `sys` module that's like a Swiss Army Knife for debugging processes.
```elixir
iex> :sys.get_state(pid)
%Servy.PledgeServer.State{cache_size: 3, pledges: [{"wilma", 15}, {"fred", 25}]}

iex> :sys.trace(pid, true)
:ok

iex> Servy.PledgeServer.create_pledge("moe", 20)
*DBG* pledge_server got call {create_pledge,<<"moe">>,20} from <0.152.0>
*DBG* pledge_server sent <<"pledge-275">> to <0.152.0>, new state #{'__struct__'=>'Elixir.Servy.PledgeServer.State',cache_size=>3,pledges=>[{<<109,111,101>>,20},{<<108,97,114,114,121>>,10},{<<119,105,108,109,97>>,15}]}

iex> :sys.get_status(pid)
{:status, #PID<0.169.0>, {:module, :gen_server},
 [["$initial_call": {Servy.PledgeServer, :init, 1},
   "$ancestors": [#PID<0.167.0>, #PID<0.63.0>]], :running, #PID<0.169.0>,
  [trace: true],
  [header: 'Status for generic server pledge_server',
   data: [{'Status', :running}, {'Parent', #PID<0.169.0>},
    {'Logged events', []}],
   data: [{'State',
     %Servy.PledgeServer.State{cache_size: 3,
      pledges: [{"wilma", 15}, {"fred", 25}]}}]]]}
```

## Linking Processes

### Normal vs. Abnormal Process Termination
When a process terminates, whether normally (it finishes doing all its work) or abnormally (due to a crash), it notifies the linked process by sending it an exit signal.

In the case of a process terminating normally, the exit signal reason is always the atom `:normal`.  Since the process exited normally, the linked process does not terminate.

In the case of a process terminating abnormally, the exit signal reason will be anything other than the atom `:normal`.  By default, if the exit signal indicates that the process terminated abnormally, the linked process terminates with the same reason unless the linked process is trapping exits.  If it's trapping exits, then the exit signal is converted to a message that's sent to the mailbox of the linked process. 

### Monitoring a Process
Sometimes a process needs to monitor another process to detect if it crashes (or terminates normally), but you don't want their fates to be tied together.  That's where using a monitor can be handy.  Whereas a link is bidirectional, a monitor is unidirectional.

For example, let's say we have a process chugging away.  We want the `iex` process to passively monitor that process without linking itself to it.  To do that, use `Process.monitor/1` rather than `Process.link/1`.
```elixir
iex> pid = spawn(Servy.HttpServer, :start, [4000])

iex> Process.monitor(pid)
#Reference<0.2181247014.667942918.240804>

iex> Process.exit(pid, :kaboom)

iex> flush()
{:DOWN, #Reference<0.2181247014.667942918.240804>, :process, #PID<0.323.0>,
 :kaboom}
```

The `iex` process received a notification message in its mailbox.  The message includes the atom `:DOWN`, the monitor reference we saw earlier, the PID of the process that terminated, and a reason that indicates why the process terminated. 

## Fault Recovery with OTP Supervisors

### Overriding Child Spec Fields
```elixir
# Option #1
use GenServer, restart: :temporary

# Option #2
# This option opens the door to making it a multi-clause function.
def child_spec(arg) do
  %{
    id: __MODULE__,
    start: {__MODULE__, :start_link, [arg]},
    restart: :permanent,
    shutdown: 5000,
    type: :worker
  }
end
```

## Final OTP Application

```elixir
# Run an application with it's default environment
mix run --no-halt
```

### Passing Environment Variables
The --erl option is the way you pass flags (switches) to the Erlang VM.  Using `-servy port 5000` tells the VM to set the port environment parameter to the value 5000 for the servy application.  Using this same form, you can set environment parameters for any application running in the VM.
```elixir
elixir --erl "-servy port 5000" -S mix run --no-halt
```

It's also worth mentioning that you can also programmatically override any application environment parameter using the `Application.put_env/3` function.
```elixir
Application.put_env(:servy, :port, 5000)
```

### Configuration Techniques
You can add the default port to the application's environment in the `mix.exs` file.
```elixir
def application do
  [
    extra_applications: [:logger],
    mod: {Servy, []},
    env: [port: 3000]
  ]
end
```

You may also add the line to the `config/config.exs` file.
```elixir
config :servy, port: 3000
```

When you `mix run` it loads `config.exs`.  However, if this application is run as a dependency of another application, then the contents of `config.exs` will have no effect because `config.exs` is never loaded.  In other words, any configuration changes made to `config.exs` are restricted to this project.

### Creating a Project with a Supervisor
When you create a new project using `mix new`, you can pass it the `--sup` option and Mix will generate an `Application` callback module that starts a supervisor. 

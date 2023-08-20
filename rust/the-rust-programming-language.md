# The Rust Programming Language

## Getting Started

### Installation

#### Updating

- Once Rust is installed via `rustup`, you can update to a newly released version using:

```
$ rustup update
```

### Cargo

```
$ cargo new hello_cargo
```

- The `cargo build` command creates an executable file in `target/debug/hello_cargo`

```$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

- Because the default build is a debug build, Cargo puts the binary in a directory named `debug`

```
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

- Running `cargo build` for the first time also causes Cargo to create a new file at the top level: `Cargo.lock`
  - This file keeps track of the exact versions of dependencies in your project
  - You won’t ever need to change this file manually; Cargo manages its contents for you
- You can also use `cargo run` to compile the code and then run the resultant executable all in one command:

```
$ cargo run
Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
Running `target/debug/hello_cargo`
Hello, world!
```

- Cargo also provides a command called `cargo check`
  - This command quickly checks your code to make sure it compiles but doesn’t produce an executable:

```
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

#### Cargo as Convention

- With simple projects, Cargo doesn’t provide a lot of value over just using `rustc`, but it will prove its worth as your programs become more intricate
- Once programs grow to multiple files or need a dependency, it’s much easier to let Cargo coordinate the build

#### Building for Release

- When your project is finally ready for release, you can use `cargo build --release` to compile it with optimizations
  - This command will create an executable in `target/release` instead of `target/debug`
  - The optimizations make your Rust code run faster, but turning them on lengthens the time it takes for your program to compile

## Common Programming Concepts

- `&` indicates that this argument is a reference
  - This gives you a way to let multiple parts of your code access one piece of data without needing to copy that data into memory multiple times

### Variables and Mutability

#### Constants

- Constants are values that are bound to a name and are not allowed to change

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

#### Shadowing

- Shadowing is when you declare a new variable with the same name as a previous variable

```rust
fn main() {
    let x = 5;

    let x = x + 1;

    {
        let x = x * 2;
        println!("The value of x in the inner scope is: {x}");
    }

    println!("The value of x is: {x}");
}
```

```
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished dev [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/variables`
The value of x in the inner scope is: 12
The value of x is: 6
```

- Shadowing is different from marking a variable as `mut` because we’ll get a compile-time error if we accidentally try to reassign to this variable without using the `let` keyword
- The other difference between `mut` and shadowing is that because we’re effectively creating a new variable when we use the `let` keyword again, we can change the type of the value but reuse the same name

```rust
    let spaces = "   ";
    let spaces = spaces.len();
```

If we try to use `mut` for this, we’ll get a compile-time error:

```rust
    let mut spaces = "   ";
    spaces = spaces.len();
```

```
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
error[E0308]: mismatched types
 --> src/main.rs:3:14
  |
2 |     let mut spaces = "   ";
  |                      ----- expected due to this value
3 |     spaces = spaces.len();
  |              ^^^^^^^^^^^^ expected `&str`, found `usize`

For more information about this error, try `rustc --explain E0308`.
error: could not compile `variables` due to previous error

```

### Data Types

-

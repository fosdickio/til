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
- The `trim` method on a `String` instance will eliminate any whitespace at the beginning and end
- The `parse` method on strings converts a string to another type

```rust
    let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

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

#### Scalar Types

- A scalar type represents a single value
- Rust has four primary scalar types: integers, floating-point numbers, Booleans, and characters

##### Integer Types

| Length  | Signed  | Unsigned |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| arch    | `isize` | `usize`  |

- Each signed variant can store numbers from -(2^(n-1)) to (2^(n-1) - 1) inclusive, where n is the number of bits that variant uses
  - Example: an `i8` can store numbers from -(2^7) to (2^7 - 1), which equals -128 to 127
- Unsigned variants can store numbers from 0 to 2^n - 1
  - Example: a u8 can store numbers from 0 to 2^8 - 1, which equals 0 to 255
- The `isize` and `usize` types depend on the architecture of the computer your program is running on
  - 64 bits if you’re on a 64-bit architecture and 32 bits if you’re on a 32-bit architecture

| Number literals | Example       |
| --------------- | ------------- |
| Decimal         | `98_222`      |
| Hex             | `0xff`        |
| Octal           | `0o77`        |
| Binary          | `0b1111_0000` |
| Byte (u8 only)  | `b'A'`        |

##### Floating-Point Types

- Rust’s floating-point types are `f32` and `f64`, which are 32 bits and 64 bits in size, respectively
- The default type is `f64` because on modern CPUs, it’s roughly the same speed as `f32` but is capable of more precision
- All floating-point types are signed.

```rust
fn main() {
    let x = 2.0; // f64

    let y: f32 = 3.0; // f32
}
```

##### Numeric Operationns

- Rust supports the basic mathematical operations you’d expect for all the number types: addition, subtraction, multiplication, division, and remainder
- Integer division truncates toward zero to the nearest integer

##### The Boolean Type

- A Boolean type in Rust has two possible values: `true` and `false`
- Booleans are one byte in size
- It's specified using `bool`

##### The Character Type

- You can specify `char` literals with single quotes, as opposed to string literals, which use double quotes
- Rust’s `char` type is four bytes in size and represents a Unicode Scalar Value, which means it can represent a lot more than just ASCII
  - Accented letters; Chinese, Japanese, and Korean characters; emoji; and zero-width spaces are all valid char values in Rust
- Unicode Scalar Values range from `U+0000` to `U+D7FF` and `U+E000` to U`+10FFFF` inclusive

```rust
fn main() {
    let c = 'z';
    let z: char = 'ℤ';
    let heart_eyed_cat = '😻';
}
```

#### Compound Types

##### The Tuple Type

- A tuple is a general way of grouping together a number of values with a variety of types into one compound type
- Tuples have a fixed length: once declared, they cannot grow or shrink in size

```rust
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);

    // Destructuring
    let (x, y, z) = tup;
}
```

##### The Array Type

- Unlike a tuple, every element of an array must have the same type
- Unlike arrays in some other languages, arrays in Rust have a fixed length

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];
}
```

- Arrays are useful when you want your data allocated on the stack rather than the heap or when you want to ensure you always have a fixed number of elements
- An array isn’t as flexible as the vector type
  - A vector is a similar collection type provided by the standard library that is allowed to grow or shrink in size
  - If you’re unsure whether to use an array or a vector, chances are you should use a vector

### Functions

- Rust code uses snake case as the conventional style for function and variable names, in which all letters are lowercase and underscores separate words
- In function signatures, you must declare the type of each parameter
- Function bodies are made up of a series of statements optionally ending in an expression
  - Statements are instructions that perform some action and do not return a value
  - Expressions evaluate to a resultant value

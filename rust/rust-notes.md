# Rust Notes

## Why Rust?
- **Speed** - no penalty for abstraction
- **Safety** - ensures memory safety using ownership and its borrowing concept (no garbage collection)

## Macros
- An expression that has an exclamation mark (`!`) before the parenthesis (`()`)
- Used in *metaprogramming* (code that writes code)
- Instead of generating a function call like functions, they are expanded into source code that gets compiled with the rest of the program

## Comments

### Doc Comments (`///` and `//!`)
```rust
/// This is an doc comment outside the function
/// Generate docs for the following item
/// This shows my code outside a module or a function
fn main() {
    //! This a doc comment that is inside the function   
    //! This comment shows my code inside a module or a function  
    //! Generate docs for the enclosing item
    println!("{} can support {} notation.", "Doc comments", "Markdown");
```

## Variables
- Immutable by default
- By convention, you would write a variable name using `snake_case`

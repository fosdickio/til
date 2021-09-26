# Kotlin Notes

## Basic Literals

### Integer Numbers

Here are several examples of valid integer number literals separated by commas: `0`, `10`, `100`.

If an integer value contains a lot of digits, we can add underscores to divide the digits into blocks to make this number more readable: for example, `1_000_000` is much easier to read than `1000000`.

You can add as many underscores as you would like: `1__000_000`, `1_2_3`. Remember, underscores can’t appear at the start or at the end of the number. If you write `_10` or `100_`, you get an error.

### Characters

To write a single character, we wrap a symbol in single quotes as follows: `'A'`, `'x'`, `'0'`. Character literals can represent alphabet letters, digits from `'0'` to `'9'`, whitespaces (`' '`), or some other symbols (e.g., `'$'`).

### Strings

To write strings, we wrap characters in double quotes instead of single ones. Here are some valid examples: `"text"`, `"123456"`.

## Variables

- `val` (for _value_) declares an **immutable variable**.
- `var` (for _variable_) declares a **mutable variable**, which can be changed (as many times as needed).

There is one restriction for mutable variables (the ones declared with the keyword `var`) though. When reassigning their values, you can only use new values of the same type as the initial one. So, the piece of code below is not correct:

```kotlin
var number = 10
number = 11 // OK
number = "twelve" // Error!
```

## Types

### Numbers

**Integer numbers** (0, 1, 2, ...) are represented by the following four types: `Long`, `Int`, `Short`, `Byte` (from the largest to the smallest).

- `Byte`: 8 bits (1 byte), range varies from -128 to 127;
- `Short`: 16 bits (2 bytes), range varies from -32768 to 32767;
- `Int`: 32 bits (4 bytes), range varies from −(231) to (231)−1;
- `Long`: 64 bits (8 bytes), range varies from −(263) to (263)−1.

The most common integer types are `Int` and `Long`. Try to stick to `Int` in practice. If you need more freedom for your numbers, use `Long`.

```kotlin
val zero = 0 // Int
val one = 1  // Int
val oneMillion = 1_000_000  // Int

val twoMillion = 2_000_000L // Long because it is tagged with L
val bigNumber = 1_000_000_000_000_000 // Long, Kotlin automatically chooses it (Int is too small)
val ten: Long = 10 // Long because the type is specified

val shortNumber: Short = 15 // Short because the type is specified
val byteNumber: Byte = 15   // Byte because the type is specified
```

**Floating-point types** represent numbers with fractional parts. Kotlin has two such types: `Double` (64 bits) and `Float` (32 bits). These types can store only a limited number of decimal digits (~6-7 for `Float` and ~14-16 for `Double`). The `Double` type is more common in practice.

```kotlin
val pi = 3.1415  // Double
val e = 2.71828f // Float because it is tagged with f
val fraction: Float = 1.51 // Float because the type is specified
```

To display the maximum and minimum value of a numeric type (including `Double` and `Float`), you need to write the type name followed by a dot `.` and then either `MIN_VALUE` or `MAX_VALUE`.

```kotlin
println(Int.MIN_VALUE)  // -2147483648
println(Int.MAX_VALUE)  // 2147483647
println(Long.MIN_VALUE) // -9223372036854775808
println(Long.MAX_VALUE) // 9223372036854775807
```

It is also possible to get the size of an integer type in bytes or bits (1 byte = 8 bits).

```kotlin
println(Int.SIZE_BYTES) // 4
println(Int.SIZE_BITS) // 32
```

### Characters

Kotlin has a `Char` type to represent various letter characters (uppercase and lowercase), digits, and other symbols. Each character is a letter character in single quotes. The size is similar to the `Short` type (2 bytes = 16 bits).

```kotlin
val lowerCaseLetter = 'a'
val upperCaseLetter = 'Q'
val number = '1'
val space = ' '
val dollar = '$'
```

### Booleans

Kotlin provides a type called `Boolean`. It can store only two values: `true` and `false`. It represents only one bit of information, but its size is not precisely defined.

```kotlin
val enabled = true
val bugFound = false
```

### Strings

The `String` type represents a sequence of characters in double quotes.

```kotlin
val creditCardNumber = "1234 5678 9012 3456"
```

#### String Templates

To add a variable value to a string, write the dollar sign `$` before a variable name.

```kotlin
val city = "Paris"
val temp = "24"

println("The temperature in $city is $temp degrees Celsius.")
```

You can use string templates to put the result of an arbitrary expression in a string. To do that, include the entire expression in curly braces `{...}` after the dollar sign `$`.

```kotlin
// {language.length} is an expression that will be evaluated
val language = "Kotlin"
println("$language has ${language.length} letters in the name")
```

## Increment and Decrement

### Prefix and Postfix

```kotlin
var a = 10
val b = ++a
println(a)  // a = 11
println(b)  // b = 11

var a = 10
val b = a++
println(a)  // a = 11
println(b)  // b = 10
```

### Order of Precedence

Below is list of operations in decreasing order of priority:

1. Parentheses ( (expr) );
2. Postfix increment/decrement ( expr++, expr--);
3. Unary plus/minus, prefix increment/decrement ( -expr, ++expr, --expr );
4. Multiplication, division, and modulus ( \*, /, % );
5. Addition and subtraction ( +, - );
6. Assignment operations ( =, +=, -=, \*=, /=, %= ).

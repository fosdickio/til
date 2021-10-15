# The Java Language

## Text Encoding

One of the ways in which Java supports internationalization is through the Unicode character set. Unicode is a worldwide standard that supports the scripts of most languages. The latest version of Java bases its character and string data on the Unicode 6.0 standard, which uses at least two bytes to represent each symbol internally.

The Java `char` type and `String` class natively support Unicode values. Internally, the text is stored using either `char[]` or `byte[]`; however, the Java language and APIs make this transparent to you and you will not generally have to think about it.

One of the most common file encodings for Unicode, called UTF-8, preserves ASCII values in their single byte form. This encoding is used by default in compiled Java class files, so storage remains compact for English text.

A Unicode character can be represented with this escape sequence `\uxxxx`.

## Comments

### javadoc

_javadoc_ creates HTML documentation for classes by reading the source code and pulling out the embedded comments and `@` tags.

| Tag           | Description                           | Applies To                 |
| ------------- | ------------------------------------- | -------------------------- |
| `@see`        | Associated class name                 | Class, method, or variable |
| `@code`       | Source code content                   | Class, method, or variable |
| `@link`       | Associated URL                        | Class, method, or variable |
| `@author`     | Author name                           | Class                      |
| `@version`    | Version string                        | Class                      |
| `@param`      | Parameter name and description        | Method                     |
| `@return`     | Description of return value           | Method                     |
| `@exception`  | Exception name and description        | Method                     |
| `@deprecated` | Declares an item to be obsolete       | Class, method, or variable |
| `@since`      | Notes API version when item was added | Variable                   |

## Types

### Primitive Types

| Type      | Definition                               | Approximate Range or Precision |
| --------- | ---------------------------------------- | ------------------------------ |
| `boolean` | Logical value                            | `true` or `false`              |
| `char`    | 16-bit, Unicode character                | 64K characters                 |
| `byte`    | 8-bit, signed, two’s complement integer  | -128 to 127                    |
| `short`   | 16-bit, signed, two’s complement integer | -32,768 to 32,767              |
| `int`     | 32-bit, signed, two’s complement integer | -2.1e9 to 2.1e9                |
| `long`    | 64-bit, signed, two’s complement integer | -9.2e18 to 9.2e18              |
| `float`   | 32-bit, IEEE 754, floating-point value   | 6-7 significant decimal places |
| `double`  | 64-bit, IEEE 754                         | 15 significant decimal places  |

### Integer Literals

A binary number is denoted by the leading characters `0b` or `0B` (zero “b”), followed by a combination of zeros and ones:

```java
int i = 0b01001011; // i = 75 decimal
```

A hexadecimal number is denoted by the leading characters `0x` or `0X` (zero “x”), followed by a combination of digits and the characters a–f or A–F, which represent the decimal values 10–15:

```java
  int i = 0xFFFF; // i = 65535 decimal
```

Integer literals are of type `int` unless they are suffixed with an `L`, denoting that they are to be produced as a long value:

```java
long l = 13L;
long l = 13;  // equivalent: 13 is converted from type int
long l = 40123456789L;
long l = 40123456789; // error: too big for an int without conversion
```

When using Java 7 or later, you can add a bit of formatting to your numeric literals by utilizing the “\_” underscore character between digits. So if you have particularly large strings of digits, you can break them up.

```java
int SOME_NUMBER = 567_68_0515;
int for_no_reason = 1___2___3;
int JAVA_ID = 0xDEAD_BEEF;
long grandTotal = 40_123_456_789L;
```

### Floating-Point Literals

Floating-point literals are of type `double` unless they are suffixed with an `f` or `F` denoting that they are to be produced as a float value.

### Character Literals

A literal character value can be specified either as a single-quoted character or as an escaped ASCII or Unicode sequence:

```java
char a = 'a';
char newline = '\n';
char smiley = '\u263a';
```

### Strings

Strings in Java are objects; they are therefore a reference type. Literal string values in Java source code are turned into `String` objects by the compiler.

## Expressions

### The instanceof Operator

The `instanceof` operator can be used to determine the type of an object at runtime. It tests to see if an object is of the same type or a subtype of the target type.

## Array Types

### Array Creation and Initialization

Java supports the C-style curly braces `{}` construct for creating an array and initializing its elements:

```java
int [] primes = { 2, 3, 5, 7, 7+4 };
```

### Using Arrays

`length` is the only accessible field of an array; it is a variable, not a method.

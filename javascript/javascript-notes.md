# JavaScript Notes

## JavaScript is Interpreted
- Each browser has its own JavaScript engine, which either interprets the code or uses some sort of lazy compilation
  - V8: Chrome and Node.js
  - SpiderMonkey: Firefox
  - JavaScriptCore: Safari
  - Chakra: Microsoft Edge/IE
- They each implement the ECMAScript standard, but may differ for anything not defined by the standard

## Syntax
```javascript
const name = 'GitHub';
const arr = ['Some text', 42, true, function() {
    console.log('hi')
}];
for (let i = 0; i < arr.length; i++) {
    console.log(arr[i]);
}
```

## Types
- Dynamic typing
- Primitive types (no methods, immutable)
  - `undefined`
  - `null`
  - `boolean`
  - `number`
  - `string`
  - `symbol`
- Objects

### Primitives vs. Objects
- Primitives are immutable and stored by value
- Objects are mutable and stored by reference

## Typecasting / Coercion

### Explicit vs. Implicit Coercion
```javascript
const x = 42;
const explicit = String(x);  // explicit === "42"
const implicit = x + "";     // implicit === "42"
```

### `==` vs. `===`
- `==` coerces the types
- `===` requires equivalent types

![Javascript Equality](img/javascript-equality.png)

### Coercion
- Which values are falsy?
  - `undefined`
  - `null`
  - `false`
  - `+0`, `-0`, `NaN`
- Which values are truthy?
  - `{}`
  - `[]`
  - Everything else

## Prototypal Inheritance
- Non-primitive types have a few properties/methods associated with them
  - `Array.prototype.push()`
  - `String.prototype.toUpperCase()`
- Each object stores a reference to it's prototype
    - Properties/methods defined most tightly to the instance have priority
    - Most primitive types have object wrappers
- JavaScript will automatically “box” (wrap) primitive values so you have access to methods

```javascript
42.toString()        // Errors
const x = 42;
x.toString()         // "42"
x.__proto__          // [Number: 0]
x instanceof Number  // false
```

## Scope

### Variable lifetime
- Lexical scoping (`var`): from when they’re declared until when their function ends
- Block scoping (`const`, `let`): until the next `}` is reached

### Hoisting
- Function definitions are hoisted, but not lexically-scoped initializations

```javascript
function thisIsHoisted() {
    console.log('This is hoisted.')
}

const thisIsNotHoisted = function() {
    console.log('This is NOT hoisted.')
}
```

## The Global Object
- All variables and functions are actually parameters and methods on the global object
  - Browser global object is the `window` object
  - Node.js global object is the `global` object

## Closures
- Functions that refer to variables declared by parent function still have access to those variables
- This is possible because of JavaScript’s scoping

## Immediately Invoked Function Expression
- A function expression that gets invoked immediately
- Creates closure
- Doesn’t add to or modify global object

## First-Class Functions
- Functions are treated the same way as any other value
  - Can be assigned to variables, array values, object values
  - Can be passed as arguments to other functions
  - Can be returned from functions
- Allows for the creation of higher-order functions
  - Either takes one or more functions as arguments or returns a function
  - `map()`, `filter()`, `reduce()`

## Synchronous? Async? Single-Threaded?
- JavaScript is a single-threaded, synchronous language
- JavaScript has functions that act asynchronously

### Asynchronous JavaScript
- Execution stack
- Browser APIs
- Function queue
- Event loop
- Asynchronous functions
  - `setTimeout()`
  - `XMLHttpRequest()`, `jQuery.ajax()`, `fetch()`
  - Database calls

### Callbacks
- Control flow with asynchronous calls
- Execute function once asynchronous call returns value

### Promises
- Alleviate "callback hell"
- Allows you to write code that assumes a value is returned within a success function
- Only needs a single error handler

### Async/Await
- Introduced in ES2017
- Allows people to write async code as if it were synchronous

## `this`
- Refers to an object that’s set at the creation of a new execution context (function invocation)
- In the global execution context, it refers to the global object
- If the function is called as a method of an object, `this` is bound to the object the method is called on

## Document Object Model
- When a browser renders HTML for a webpage, the HTML is defined in a tree-like structure
  - Browsers construct this tree in memory before painting the page
  - This tree is called the Document Object Model
- The DOM can be modified using JavaScript

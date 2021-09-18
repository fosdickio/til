# Node.js

Node was initially conceived for the purpose of making asynchronous programming easy and convenient.

## The Node Command

The `process` binding, just like the `console` binding, is available globally in Node. It provides various ways to inspect and manipulate the current program.

## Modules

The CommonJS module system is based on the `require` function. This system is built into Node and is used to load anything from built-in modules to downloaded packages to files that are part of your own program.

When a string that does not look like a relative or absolute path is given to `require`, it is assumed to refer to either a built-in module or a module installed in a `node_modules` directory. For example, `require("fs")` will give you Node’s built-in file system module.

## Installing with NPM

After running `npm install`, NPM will have created a directory called `node_modules`. Inside that directory will be a directory that contains the library. You can open it and look at the code. When we call `require("ini")`, this library is loaded, and we can call its parse property to parse a configuration file.

## Versions

A semantic version consists of three numbers, separated by periods, such as `2.3.0`. Every time new functionality is added, the middle number has to be incremented. Every time compatibility is broken, so that existing code that uses the package might not work with the new version, the first number has to be incremented.

A caret character (`^`) in front of the version number for a dependency in `package.json` indicates that any version compatible with the given number may be installed. So, for example, `"^2.3.0"` would mean that any version greater than or equal to 2.3.0 and less than 3.0.0 is allowed.

The `npm` command is also used to publish new packages or new versions of packages. If you run `npm publish` in a directory that has a `package.json` file, it will publish a package with the name and version listed in the JSON file to the registry. Anyone can publish packages to NPM — though only under a package name that isn’t in use yet since it would be somewhat scary if random people could update existing packages.

## The File System Module

One of the most commonly used built-in modules in Node is the `fs` module, which stands for _file system_. It exports functions for working with files and directories.

```js
let { readFile } = require("fs");
readFile("file.txt", "utf8", (error, text) => {
  if (error) throw error;
  console.log("The file contains:", text);
});
```

There are several ways in which text can be encoded to binary data, but most modern systems use UTF-8. So unless you have reasons to believe another encoding is used, pass `"utf8"` when reading a text file. If you do not pass an encoding, Node will assume you are interested in the binary data and will give you a `Buffer` object instead of a string. This is an array-like object that contains numbers representing the bytes (8-bit chunks of data) in the files.

A similar function, `writeFile`, is used to write a file to disk.

```js
const { writeFile } = require("fs");
writeFile("graffiti.txt", "Node was here", (err) => {
  if (err) console.log(`Failed to write file: ${err}`);
  else console.log("File written.");
});
```

Here it was not necessary to specify the encoding — `writeFile` will assume that when it is given a string to write, rather than a `Buffer` object, it should write it out as text using its default character encoding, which is UTF-8.

The `fs` module contains many other useful functions: `readdir` will return the files in a directory as an array of strings, `stat` will retrieve information about a file, `rename` will rename a file, `unlink` will remove one, and so on.

There is an object `promises` exported from the `fs` package since version 10.1 that contains most of the same functions as `fs` but uses promises rather than callback functions.

```js
const { readFile } = require("fs").promises;
readFile("file.txt", "utf8").then((text) =>
  console.log("The file contains:", text)
);
```

Many of the functions in fs also have a synchronous variant, which has the same name with `Sync` added to the end.

## The HTTP Module

Another central module is called `http`. It provides functionality for running HTTP servers and making HTTP requests.

```js
const { createServer } = require("http");
let server = createServer((request, response) => {
  response.writeHead(200, { "Content-Type": "text/html" });
  response.write(`
    <h1>Hello!</h1>
    <p>You asked for <code>${request.url}</code></p>`);
  response.end();
});
server.listen(8000);
console.log("Listening! (port 8000)");
```

The function passed as argument to `createServer` is called every time a client connects to the server. The `request` and `response` bindings are objects representing the incoming and outgoing data. The first contains information about the request, such as its `url` property, which tells us to what URL the request was made.

To send something back, you call methods on the response object. The first, `writeHead`, will write out the response headers.

Next, the actual response body (the document itself) is sent with `response.write`. You are allowed to call this method multiple times if you want to send the response piece by piece, for example to stream data to the client as it becomes available. Finally, `response.end` signals the end of the response.

The call to `server.listen` causes the server to start waiting for connections on port 8000.

A real web server usually does more than the one in the example — it looks at the request’s method (the `method` property) to see what action the client is trying to perform and looks at the request’s URL to find out which resource this action is being performed on.

To act as an HTTP _client_, we can use the `request` function in the `http` module.

```js
const { request } = require("http");
let requestStream = request(
  {
    hostname: "fosdick.io",
    path: "/index.html",
    method: "GET",
    headers: { Accept: "text/html" },
  },
  (response) => {
    console.log("Server responded with status code", response.statusCode);
  }
);
requestStream.end();
```

There’s a similar `request` function in the `https` module that can be used to make requests to `https:` URLs.

Making requests with Node’s raw functionality is rather verbose. There are much more convenient wrapper packages available on NPM. For example, `node-fetch` provides the promise-based `fetch` interface that we know from the browser.

## Streams

_Writable streams_ are a widely used concept in Node. Such objects have a `write` method that can be passed a string or a `Buffer` object to write something to the stream. Their `end` method closes the stream and optionally takes a value to write to the stream before closing. Both of these methods can also be given a callback as an additional argument, which they will call when the writing or closing has finished.

It is possible to create a writable stream that points at a file with the `createWriteStream` function from the `fs` module. Then you can use the `write` method on the resulting object to write the file one piece at a time, rather than in one shot as with `writeFile`.

Objects that emit events in Node have a method called `on` that is similar to the `addEventListener` method in the browser. You give it an event name and then a function, and it will register that function to be called whenever the given event occurs.

Readable streams have `"data"` and `"end"` events. The first is fired every time data comes in, and the second is called whenever the stream is at its end. This model is most suited for _streaming_ data that can be immediately processed, even when the whole document isn’t available yet.

```js
/**
 * This code creates a server that reads request bodies and streams them back to
 * the client as all-uppercase text.
 */
const { createServer } = require("http");
createServer((request, response) => {
  response.writeHead(200, { "Content-Type": "text/plain" });
  request.on("data", (chunk) => response.write(chunk.toString().toUpperCase()));
  request.on("end", () => response.end());
}).listen(8000);
```

The `chunk` value passed to the data handler will be a binary `Buffer`.

```js
/**
 * The following piece of code, when run with the uppercasing server active, 
 will send a request to that server and write out the response it gets.
 */
const { request } = require("http");
request(
  {
    hostname: "localhost",
    port: 8000,
    method: "POST",
  },
  (response) => {
    response.on("data", (chunk) => process.stdout.write(chunk.toString()));
  }
).end("Hello server");
// → HELLO SERVER
```

The example writes to `process.stdout` (the process’s standard output, which is a writable stream) instead of using `console.log`. We can’t use `console.log` because it adds an extra newline character after each piece of text that it writes, which isn’t appropriate here since the response may come in as multiple chunks.

## A File Server

This section details the implementation of a file system to create an HTTP server that allows remote access to a file system.

```js
const { createServer } = require("http");

const methods = Object.create(null);

createServer((request, response) => {
  let handler = methods[request.method] || notAllowed;
  handler(request)
    .catch((error) => {
      if (error.status != null) return error;
      return { body: String(error), status: 500 };
    })
    .then(({ body, status = 200, type = "text/plain" }) => {
      response.writeHead(status, { "Content-Type": type });
      if (body && body.pipe) body.pipe(response);
      else response.end(body);
    });
}).listen(8000);

async function notAllowed(request) {
  return {
    status: 405,
    body: `Method ${request.method} not allowed.`,
  };
}

var { parse } = require("url");
var { resolve, sep } = require("path");

var baseDirectory = process.cwd();

function urlPath(url) {
  let { pathname } = parse(url);
  let path = resolve(decodeURIComponent(pathname).slice(1));
  if (path != baseDirectory && !path.startsWith(baseDirectory + sep)) {
    throw { status: 403, body: "Forbidden" };
  }
  return path;
}

const { createReadStream } = require("fs");
const { stat, readdir } = require("fs").promises;
const mime = require("mime");

methods.GET = async function (request) {
  let path = urlPath(request.url);
  let stats;
  try {
    stats = await stat(path);
  } catch (error) {
    if (error.code != "ENOENT") throw error;
    else return { status: 404, body: "File not found" };
  }
  if (stats.isDirectory()) {
    return { body: (await readdir(path)).join("\n") };
  } else {
    return { body: createReadStream(path), type: mime.getType(path) };
  }
};

const { rmdir, unlink } = require("fs").promises;

methods.DELETE = async function (request) {
  let path = urlPath(request.url);
  let stats;
  try {
    stats = await stat(path);
  } catch (error) {
    if (error.code != "ENOENT") throw error;
    else return { status: 204 };
  }
  if (stats.isDirectory()) await rmdir(path);
  else await unlink(path);
  return { status: 204 };
};

const { createWriteStream } = require("fs");

function pipeStream(from, to) {
  return new Promise((resolve, reject) => {
    from.on("error", reject);
    to.on("error", reject);
    to.on("finish", resolve);
    from.pipe(to);
  });
}

methods.PUT = async function (request) {
  let path = urlPath(request.url);
  await pipeStream(request, createWriteStream(path));
  return { status: 204 };
};

const { mkdir } = require("fs").promises;

methods.MKCOL = async function (request) {
  let path = urlPath(request.url);
  let stats;
  try {
    stats = await stat(path);
  } catch (error) {
    if (error.code != "ENOENT") throw error;
    await mkdir(path);
    return { status: 204 };
  }
  if (stats.isDirectory()) return { status: 204 };
  else return { status: 400, body: "Not a directory" };
};
```

Method handlers are `async` functions that get the request object as argument and return a promise that resolves to an object that describes the response.

When the value of `body` is a readable stream, it will have a `pipe` method that is used to forward all content from a readable stream to a writable stream. If not, it is assumed to be either `null` (no body), a string, or a buffer, and it is passed directly to the response’s end method.

`urlPath` uses the `resolve` function from the `path` module, which resolves relative paths. It then verifies that the result is _below_ the working directory. The `process.cwd` function (where `cwd` stands for “current working directory”) can be used to find this working directory. The `sep` binding from the `path` package is the system’s path separator — a backslash on Windows and a forward slash on most other systems.

The `mime` package (content type indicators like `text/plain` are also called MIME _types_) knows the correct type for a large number of file extensions.

When an HTTP response does not contain any data, the status code 204 (“no content”) can be used to indicate this. Since the response to deletion doesn’t need to transmit any information beyond whether the operation succeeded, that is a sensible thing to return here.

## Summary

Node comes with a number of built-in modules, including the `fs` module for working with the file system and the `http` module for running HTTP servers and making HTTP requests.

All input and output in Node is done asynchronously, unless you explicitly use a synchronous variant of a function, such as `readFileSync`. When calling such asynchronous functions, you provide callback functions, and Node will call them with an error value and (if available) a result when it is ready.

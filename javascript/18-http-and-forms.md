# HTTP and Forms

> Communication must be stateless in nature such that each request from client to server must contain all of the information necessary to understand the request, and cannot take advantage of any stored context on the server.
>
> -- Roy Fielding, _Architectural Styles and the Design of Network-based Software Architectures_

## Fetch

The interface through which browser JavaScript can make HTTP requests is called `fetch`.

```js
fetch("example/data.txt").then((response) => {
  console.log(response.status);
  // → 200
  console.log(response.headers.get("Content-Type"));
  // → text/plain
});
```

Calling `fetch` returns a promise that resolves to a `Response` object holding information about the server’s response, such as its status code and its headers. The headers are wrapped in a `Map`-like object that treats its keys (the header names) as case insensitive because header names are not supposed to be case sensitive.

Note that the promise returned by `fetch` resolves successfully even if the server responded with an error code. It might also be rejected if there is a network error or if the server that the request is addressed to can’t be found.

The first argument to `fetch` is the URL that should be requested. When that URL doesn’t start with a protocol name (such as `http:`), it is treated as relative, which means it is interpreted relative to the current document. When it starts with a slash (`/`), it replaces the current path, which is the part after the server name.

To get at the actual content of a response, you can use its `text` method. Because the initial promise is resolved as soon as the response’s headers have been received and because reading the response body might take a while longer, this again returns a promise.

```js
fetch("example/data.txt")
  .then((resp) => resp.text())
  .then((text) => console.log(text));
// → This is the content of data.txt
```

A similar method, called `json`, returns a promise that resolves to the value you get when parsing the body as JSON or rejects if it’s not valid JSON.

By default, `fetch` uses the `GET` method to make its request and does not include a request body. You can configure it differently by passing an object with extra options as a second argument.

```js
fetch("example/data.txt", { method: "DELETE" }).then((resp) => {
  console.log(resp.status);
  // → 405
});
```

To add a request body, you can include a `body` option. To set headers, there’s the headers option.

```js
fetch("example/data.txt", { headers: { Range: "bytes=8-19" } })
  .then((resp) => resp.text())
  .then(console.log);
// → the content
```

## HTTP Sandboxing

Browsers protect us by disallowing scripts to make HTTP requests to other domains (names such as _themafia.org_ and _mybank.com_). This can be an annoying problem when building systems that want to access several domains for legitimate reasons. Fortunately, servers can include a header like this in their response to explicitly indicate to the browser that it is okay for the request to come from another domain:

```
Access-Control-Allow-Origin: *
```

## Focus

We can control focus from JavaScript with the `focus` and `blur` methods. The first moves focus to the DOM element it is called on, and the second removes focus. The value in `document.activeElement` corresponds to the currently focused element.

```html
<input type="text" />

<script>
  document.querySelector("input").focus();
  console.log(document.activeElement.tagName);
  // → INPUT
  document.querySelector("input").blur();
  console.log(document.activeElement.tagName);
  // → BODY
</script>
```

For some pages, the user is expected to want to interact with a form field immediately. JavaScript can be used to focus this field when the document is loaded, but HTML also provides the `autofocus` attribute, which produces the same effect while letting the browser know what we are trying to achieve.

Browsers traditionally also allow the user to move the focus through the document by pressing the tab key. We can influence the order in which elements receive focus with the `tabindex` attribute.

```html
<input type="text" tabindex="1" /> <a href=".">(help)</a>
<button onclick="console.log('ok')" tabindex="2">OK</button>
```

A `tabindex` of `-1` makes tabbing skip over an element, even if it is normally focusable.

## The Form as a Whole

When a field is contained in a `<form>` element, its DOM element will have a form property linking back to the form’s DOM element. The `<form>` element, in turn, has a property called `elements` that contains an array-like collection of the fields inside it.

The name attribute of a form field determines the way its value will be identified when the form is submitted. It can also be used as a property name when accessing the form’s `elements` property, which acts both as an array-like object (accessible by number) and a map (accessible by name).

```html
<form action="example/submit.html">
  Name: <input type="text" name="name" /><br />
  Password: <input type="password" name="password" /><br />
  <button type="submit">Log in</button>
</form>

<script>
  let form = document.querySelector("form");
  console.log(form.elements[1].type);
  // → password
  console.log(form.elements.password.type);
  // → password
  console.log(form.elements.name.form == form);
  // → true
</script>
```

A button with a `type` attribute of `submit` will, when pressed, cause the form to be submitted. Pressing `ENTER` when a form field is focused has the same effect.

Submitting a form normally means that the browser navigates to the page indicated by the form’s `action` attribute, using either a `GET` or a `POST` request. But before that happens, a "`submit`" event is fired. You can handle this event with JavaScript and prevent this default behavior by calling `preventDefault` on the event object.

## Text Fields

Fields created by `<textarea>` tags, or `<input>` tags with a type of text or password, share a common interface. Their DOM elements have a value property that holds their current content as a string value. Setting this property to another string changes the field’s content.

The `selectionStart` and `selectionEnd` properties of text fields give us information about the cursor and selection in the text. When nothing is selected, these two properties hold the same number, indicating the position of the cursor.

The "`change`" event for a text field does not fire every time something is typed. Rather, it fires when the field loses focus after its content was changed. To respond immediately to changes in a text field, you should register a handler for the "`input`" event instead, which fires for every time the user types a character, deletes text, or otherwise manipulates the field’s content.

```html
<input type="text" /> length: <span id="length">0</span>

<script>
  /*
  Shows a text field and a counter displaying the current length of the text in the field
  */
  let text = document.querySelector("input");
  let output = document.querySelector("#length");
  text.addEventListener("input", () => {
    output.textContent = text.value.length;
  });
</script>
```

## Select Fields

When given the `multiple` attribute, a `<select>` tag will allow the user to select any number of options, rather than just a single option.

The `<option>` tags for a `<select>` field can be accessed as an array-like object through the field’s options property. Each option has a property called `selected`, which indicates whether that option is currently selected.

## File Fields

The `files` property of a file field element is an array-like object (again, not a real array) containing the files chosen in the field. It is initially empty. The reason there isn’t simply a `file` property is that file fields also support a `multiple` attribute, which makes it possible to select multiple files at the same time.

Objects in the `files` object have properties such as `name` (the filename), `size` (the file’s size in bytes, which are chunks of 8 bits), and `type` (the media type of the file, such as `text/plain` or `image/jpeg`).

What it does not have is a property that contains the content of the file. Getting at that is a little more involved. Since reading a file from disk can take time, the interface must be asynchronous to avoid freezing the document.

```html
<input type="file" multiple />

<script>
  let input = document.querySelector("input");
  input.addEventListener("change", () => {
    for (let file of Array.from(input.files)) {
      let reader = new FileReader();
      reader.addEventListener("load", () => {
        console.log(
          "File",
          file.name,
          "starts with",
          reader.result.slice(0, 20)
        );
      });
      reader.readAsText(file);
    }
  });
</script>
```

Reading a file is done by creating a `FileReader` object, registering a "`load`" event handler for it, and calling its `readAsText` method, giving it the file we want to read. Once loading finishes, the reader’s `result` property contains the file’s content.

FileReaders also fire an "`error`" event when reading the file fails for any reason. The error object itself will end up in the reader’s `error` property. This interface was designed before promises became part of the language. You could wrap it in a promise like this:

```js
function readFileText(file) {
  return new Promise((resolve, reject) => {
    let reader = new FileReader();
    reader.addEventListener("load", () => resolve(reader.result));
    reader.addEventListener("error", () => reject(reader.error));
    reader.readAsText(file);
  });
}
```

## Storing Data Client-Side

The `localStorage` object can be used to store data in a way that survives page reloads. This object allows you to file string values under names.

```js
localStorage.setItem("username", "fosdick.io");
console.log(localStorage.getItem("username"));
// → fosdick.io
localStorage.removeItem("username");
```

A value in `localStorage` sticks around until it is overwritten. It is removed with `removeItem`, or the user clears their local data.

Sites from different domains get different storage compartments. That means data stored in `localStorage` by a given website can, in principle, be read (and overwritten) only by scripts on that same site.

Browsers do enforce a limit on the size of the data a site can store in `localStorage`. That restriction, along with the fact that filling up people’s hard drives with junk is not really profitable, prevents the feature from eating up too much space.

Reading a field that does not exist from `localStorage` will yield `null`. Passing `null` to `JSON.parse` will make it parse the string "`null`" and return `null`. Thus, the `||` operator can be used to provide a default value in a situation like this.

There is another object, similar to `localStorage`, called `sessionStorage`. The difference between the two is that the content of `sessionStorage` is forgotten at the end of each _session_, which for most browsers means whenever the browser is closed.

## Summary

HTML fields can be inspected and manipulated with JavaScript. They fire the "`change`" event when changed, fire the "`input`" event when text is typed, and receive keyboard events when they have keyboard focus.

When the user has selected a file from their local file system in a file picker field, the `FileReader` interface can be used to access the content of this file from a JavaScript program.

The `localStorage` and `sessionStorage` objects can be used to save information in a way that survives page reloads. The first object saves the data forever (or until the user decides to clear it), and the second saves it until the browser is closed.

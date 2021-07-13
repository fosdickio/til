# Handling Browser Events

## Event Handlers

Browsers actively notify can actively notify your code when an event occurs. This can be done by registering functions as _handlers_ for specific events.

```js
<p>Click this document to activate the handler.</p>

<script>
  window.addEventListener("click", () => {
    console.log("Clicked!");
  });
</script>
```

The `window` binding refers to a built-in object provided by the browser. It represents the browser window that contains the document. Calling its `addEventListener` method registers the second argument to be called whenever the event described by its first argument occurs.

## Events and DOM nodes

Each browser event handler is registered in a context. This means they can be found on DOM elements and some other types of objects. Event listeners are called only when the event happens in the context of the object they are registered on.

```js
<button>Click me</button>
<p>No handler here!</p>

<script>
  let button = document.querySelector("button");
  button.addEventListener("click", () => {
    console.log("Button clicked.");
  });
</script>
```

Giving a node an `onclick` attribute has a similar effect. This works for most types of events — you can attach a handler through the attribute whose name is the event name with `on` in front of it.

But a node can have only one `onclick` attribute, so you can register only one handler per node that way. The `addEventListener` method allows you to add any number of handlers so that it is safe to add handlers even if there is already another handler on the element.

The `removeEventListener` method (called with arguments similar to `addEventListener`) removes a handler.

```js
<button>One click button</button>
<script>
  let button = document.querySelector("button");
  function once() {
    console.log("Done.");
    button.removeEventListener("click", once);
  }
  button.addEventListener("click", once);
</script>
```

To unregister a handler, you'll want to give the function a name to be able to pass the same function value to both methods.

## Event objects

Event handler functions are passed the _event_ object as an argument, which holds additional information about the event. For example, if we want to know _which_ mouse button was pressed, we can look at the event object's `button` property.

```js
<button>Click me using different buttons</button>

<script>
  let button = document.querySelector("button");
  button.addEventListener("mousedown", event => {
    if (event.button == 0) {
      console.log("Left button");
    } else if (event.button == 1) {
      console.log("Middle button");
    } else if (event.button == 2) {
      console.log("Right button");
    }
  });
</script>
```

The information stored in an `event` object differs per type of event. The object's `type` property always holds a string identifying the event (such as `"click"` or `"mousedown"`).

## Propagation

For most event types, handlers registered on nodes with children will also receive events that happen in the children. If a button inside a paragraph is clicked, event handlers on the paragraph will also see the click event.

If both the paragraph and the button have a handler, the more specific handler (the one on the button) gets to go first. The event is said to _propagate_ outward, from the node where it happened to that node's parent node and on to the root of the document. Finally, after all handlers registered on a specific node have had their turn, handlers registered on the whole window get a chance to respond to the event.

At any point, an event handler can call the `stopPropagation` method on the event object to prevent handlers further up from receiving the event. For examples, this can be useful when you have a button inside another clickable element and you don't want clicks on the button to activate the outer element's click behavior.

Most event objects have a `target` property that refers to the node where they originated. You can use this property to ensure that you’re not accidentally handling something that propagated up from a node you do not want to handle.

It is also possible to use the `target` property to cast a wide net for a specific type of event. For example, if you have a node containing a long list of buttons, it may be more convenient to register a single click handler on the outer node and have it use the target property to figure out whether a button was clicked, rather than register individual handlers on all of the buttons.

```js
<button>A</button>
<button>B</button>
<button>C</button>

<script>
  document.body.addEventListener("click", event => {
    if (event.target.nodeName == "BUTTON") {
      console.log("Clicked", event.target.textContent);
    }
  });
</script>
```

## Default Actions

Many events have a default action associated with them. For most types of events, the JavaScript event handlers are called _before_ the default behavior takes place. If the handler doesn’t want this normal behavior to happen, typically because it has already taken care of handling the event, it can call the `preventDefault` method on the event object. This can be used to implement your own keyboard shortcuts or context menu.

```js
<a href="https://developer.mozilla.org/">MDN</a>

<script>
  let link = document.querySelector("a");
  link.addEventListener("click", event => {
    console.log("Nope.");
    event.preventDefault();
  });
</script>
```

Depending on the browser, some events can’t be intercepted at all. On Chrome, for example, the keyboard shortcut to close the current tab (`CTRL+W` or `CMD+W`) cannot be handled by JavaScript.

## Key Events

When a key on the keyboard is pressed, your browser fires a `"keydown"` event. When it is released, you get a `"keyup"` event. Despite its name, `"keydown"` fires not only when the key is physically pushed down. When a key is pressed and held, the event fires again every time the key _repeats_.

For special keys such as `ENTER`, it holds a string that names the key (`"Enter"`, in this case). Modifier keys such as `SHIFT`, `CONTROL`, `ALT`, and `META` (`COMMAND` on Mac) generate key events just like normal keys. But when looking for key combinations, you can also find out whether these keys are held down by looking at the `shiftKey`, `ctrlKey`, `altKey`, and `metaKey` properties of keyboard and mouse events.

```js
<p>Press CTRL+Space to continue.</p>

<script>
  window.addEventListener("keydown", event => {
    if (event.key == " " && event.ctrlKey) {
      console.log("Continuing!");
    }
  });
</script>
```

The DOM node where a key event originates depends on the element that has focus when the key is pressed. Most nodes cannot have focus unless you give them a tabindex attribute, but things like links, buttons, and form fields can. When nothing in particular has focus, `document.body` acts as the target node of key events.

When the user is typing text, using key events to figure out what is being typed is problematic. Some platforms, most notably the virtual keyboard on Android phones, don’t fire key events.

To notice when something was typed, elements that you can type into, such as the `<input>` and `<textarea>` tags, fire `"input"` events whenever the user changes their content. To get the actual content that was typed, it is best to directly read it from the focused field.

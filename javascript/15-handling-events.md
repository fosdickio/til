# Handling Browser Events

## Event Handlers

Browsers actively notify can actively notify your code when an event occurs. This can be done by registering functions as _handlers_ for specific events.

```html
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

```html
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

```html
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

## Event Objects

Event handler functions are passed the _event_ object as an argument, which holds additional information about the event. For example, if we want to know _which_ mouse button was pressed, we can look at the event object's `button` property.

```html
<button>Click me using different buttons</button>

<script>
  let button = document.querySelector("button");
  button.addEventListener("mousedown", (event) => {
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

```html
<button>A</button>
<button>B</button>
<button>C</button>

<script>
  document.body.addEventListener("click", (event) => {
    if (event.target.nodeName == "BUTTON") {
      console.log("Clicked", event.target.textContent);
    }
  });
</script>
```

## Default Actions

Many events have a default action associated with them. For most types of events, the JavaScript event handlers are called _before_ the default behavior takes place. If the handler doesn’t want this normal behavior to happen, typically because it has already taken care of handling the event, it can call the `preventDefault` method on the event object. This can be used to implement your own keyboard shortcuts or context menu.

```html
<a href="https://developer.mozilla.org/">MDN</a>

<script>
  let link = document.querySelector("a");
  link.addEventListener("click", (event) => {
    console.log("Nope.");
    event.preventDefault();
  });
</script>
```

Depending on the browser, some events can’t be intercepted at all. On Chrome, for example, the keyboard shortcut to close the current tab (`CTRL+W` or `CMD+W`) cannot be handled by JavaScript.

## Key Events

When a key on the keyboard is pressed, your browser fires a `"keydown"` event. When it is released, you get a `"keyup"` event. Despite its name, `"keydown"` fires not only when the key is physically pushed down. When a key is pressed and held, the event fires again every time the key _repeats_.

For special keys such as `ENTER`, it holds a string that names the key (`"Enter"`, in this case). Modifier keys such as `SHIFT`, `CONTROL`, `ALT`, and `META` (`COMMAND` on Mac) generate key events just like normal keys. But when looking for key combinations, you can also find out whether these keys are held down by looking at the `shiftKey`, `ctrlKey`, `altKey`, and `metaKey` properties of keyboard and mouse events.

```html
<p>Press CTRL+Space to continue.</p>

<script>
  window.addEventListener("keydown", (event) => {
    if (event.key == " " && event.ctrlKey) {
      console.log("Continuing!");
    }
  });
</script>
```

The DOM node where a key event originates depends on the element that has focus when the key is pressed. Most nodes cannot have focus unless you give them a tabindex attribute, but things like links, buttons, and form fields can. When nothing in particular has focus, `document.body` acts as the target node of key events.

When the user is typing text, using key events to figure out what is being typed is problematic. Some platforms, most notably the virtual keyboard on Android phones, don’t fire key events.

To notice when something was typed, elements that you can type into, such as the `<input>` and `<textarea>` tags, fire `"input"` events whenever the user changes their content. To get the actual content that was typed, it is best to directly read it from the focused field.

## Pointer Events

There are currently two widely used ways to point at things on a screen: mice and touchscreens. These produce different kinds of events.

### Mouse Clicks

The `"mousedown"` and `"mouseup"` events are similar to `"keydown"` and `"keyup"` and fire when the button is pressed and released. These happen on the DOM nodes that are immediately below the mouse pointer when the event occurs.

After the `"mouseup"` event, a `"click"` event fires on the most specific node that contained both the press and the release of the button. For example, if I press down the mouse button on one paragraph and then move the pointer to another paragraph and release the button, the "click" event will happen on the element that contains both those paragraphs.

If two clicks happen close together, a `"dblclick"` (double-click) event also fires, after the second click event.

To get precise information about the place where a mouse event happened, you can look at its `clientX` and `clientY` properties, which contain the event’s coordinates (in pixels) relative to the top-left corner of the window, or `pageX` and `pageY`, which are relative to the top-left corner of the whole document (which may be different when the window has been scrolled).

```html
<style>
  body {
    height: 200px;
    background: beige;
  }
  .dot {
    height: 8px;
    width: 8px;
    border-radius: 4px;
    background: blue;
    position: absolute;
  }
</style>

<script>
  // Every time you click the document, a dot is added under the mouse pointer
  window.addEventListener("click", (event) => {
    let dot = document.createElement("div");
    dot.className = "dot";
    dot.style.left = event.pageX - 4 + "px";
    dot.style.top = event.pageY - 4 + "px";
    document.body.appendChild(dot);
  });
</script>
```

### Mouse Motion

Every time the mouse pointer moves, a `"mousemove"` event is fired.

```html
<p>Drag the bar to change its width:</p>
<div style="background: orange; width: 60px; height: 20px"></div>

<script>
  // Displays a bar and sets up event handlers so that dragging to the left or right on this bar makes it narrower or wider
  let lastX;
  let bar = document.querySelector("div");
  bar.addEventListener("mousedown", (event) => {
    if (event.button == 0) {
      lastX = event.clientX;
      window.addEventListener("mousemove", moved);
      event.preventDefault();
    }
  });

  function moved(event) {
    if (event.buttons == 0) {
      window.removeEventListener("mousemove", moved);
    } else {
      let dist = event.clientX - lastX;
      let newWidth = Math.max(10, bar.offsetWidth + dist);
      bar.style.width = newWidth + "px";
      lastX = event.clientX;
    }
  }
</script>
```

### Touch Events

When a finger starts touching the screen, you get a `"touchstart"` event. When it is moved while touching, `"touchmove"` events fire. Finally, when it stops touching the screen, you’ll see a `"touchend"` event.

Because many touchscreens can detect multiple fingers at the same time, these events don’t have a single set of coordinates associated with them. Rather, their event objects have a `touches` property, which holds an array-like object of points, each of which has its own `clientX`, `clientY`, `pageX`, and `pageY` properties.

```html
<style>
  dot {
    position: absolute;
    display: block;
    border: 2px solid red;
    border-radius: 50px;
    height: 100px;
    width: 100px;
  }
</style>
<p>Touch this page</p>

<script>
  // Show red circles around every touching finger
  function update(event) {
    for (let dot; (dot = document.querySelector("dot")); ) {
      dot.remove();
    }
    for (let i = 0; i < event.touches.length; i++) {
      let { pageX, pageY } = event.touches[i];
      let dot = document.createElement("dot");
      dot.style.left = pageX - 50 + "px";
      dot.style.top = pageY - 50 + "px";
      document.body.appendChild(dot);
    }
  }
  window.addEventListener("touchstart", update);
  window.addEventListener("touchmove", update);
  window.addEventListener("touchend", update);
</script>
```

## Scroll Events

Whenever an element is scrolled, a `"scroll"` event is fired on it.

```html
<style>
  #progress {
    border-bottom: 2px solid blue;
    width: 0;
    position: fixed;
    top: 0;
    left: 0;
  }
</style>

<div id="progress"></div>

<script>
  // Draws a progress bar above the document and updates it to fill up as you scroll down

  // Create some content
  document.body.appendChild(
    document.createTextNode("supercalifragilisticexpialidocious ".repeat(1000))
  );

  let bar = document.querySelector("#progress");

  // The global innerHeight binding gives us the height of the window, which we have to subtract from the total scrollable height—you can’t keep scrolling when you hit the bottom of the document. There’s also an innerWidth for the window width. By dividing pageYOffset, the current scroll position, by the maximum scroll position and multiplying by 100, we get the percentage for the progress bar.
  window.addEventListener("scroll", () => {
    let max = document.body.scrollHeight - innerHeight;
    bar.style.width = `${(pageYOffset / max) * 100}%`;
  });
</script>
```

## Focus Events

When an element gains focus, the browser fires a `"focus"` event on it. When it loses focus, the element gets a `"blur"` event.

Unlike the events discussed earlier, these two events do not propagate. A handler on a parent element is not notified when a child element gains or loses focus.

```html
<p>Name: <input type="text" data-help="Your full name" /></p>
<p>Age: <input type="text" data-help="Your age in years" /></p>
<p id="help"></p>

<script>
  let help = document.querySelector("#help");
  let fields = document.querySelectorAll("input");
  for (let field of Array.from(fields)) {
    field.addEventListener("focus", (event) => {
      let text = event.target.getAttribute("data-help");
      help.textContent = text;
    });
    field.addEventListener("blur", (event) => {
      help.textContent = "";
    });
  }
</script>
```

The window object will receive `"focus"` and `"blur"` events when the user moves from or to the browser tab or window in which the document is shown.

## Load Events

When a page finishes loading, the `"load"` event fires on the window and the document body objects. This is often used to schedule initialization actions that require the whole document to have been built. Remember that the content of `<script>` tags is run immediately when the tag is encountered.

Elements such as images and script tags that load an external file also have a `"load"` event that indicates the files they reference were loaded. Like the focus-related events, loading events do not propagate.

When a page is closed or navigated away from (for example, by following a link), a `"beforeunload"` event fires. The main use of this event is to prevent the user from accidentally losing work by closing a document. If you prevent the default behavior on this event _and_ set the `returnValue` property on the event object to a string, the browser will show the user a dialog asking if they really want to leave the page.

## Events and the Event Loop

In the context of the event loop, browser event handlers behave like other asynchronous notifications. They are scheduled when the event occurs but must wait for other scripts that are running to finish before they get a chance to run.

The fact that events can be processed only when nothing else is running means that, if the event loop is tied up with other work, any interaction with the page (which happens through events) will be delayed until there’s time to process it. So if you schedule too much work, either with long-running event handlers or with lots of short-running ones, the page will become slow and cumbersome to use.

For cases where you really do want to do some time-consuming thing in the background without freezing the page, browsers provide something called _web workers_. A worker is a JavaScript process that runs alongside the main script, on its own timeline.

To avoid the problems of having multiple threads touching the same data, workers do not share their global scope or any other data with the main script’s environment. Instead, you have to communicate with them by sending messages back and forth.

```js
// code/squareworker.js
// Computes a square and sends a message back
addEventListener("message", (event) => {
  postMessage(event.data * event.data);
});
```

```js
let squareWorker = new Worker("code/squareworker.js");
squareWorker.addEventListener("message", (event) => {
  console.log("The worker responded:", event.data);
});
squareWorker.postMessage(10);
squareWorker.postMessage(24);
```

The `postMessage` function sends a message, which will cause a `"message"` event to fire in the receiver. The script that created the worker sends and receives messages through the `Worker` object, whereas the worker talks to the script that created it by sending and listening directly on its global scope. Only values that can be represented as JSON can be sent as messages—the other side will receive a _copy_ of them, rather than the value itself.

## Timers

Sometimes you need to cancel a function you have scheduled. This is done by storing the value returned by `setTimeout` and calling `clearTimeout` on it.

```js
let bombTimer = setTimeout(() => {
  console.log("BOOM!");
}, 500);

if (Math.random() < 0.5) {
  console.log("Defused.");
  clearTimeout(bombTimer);
}
```

The `cancelAnimationFrame` function works in the same way as `clearTimeout` — calling it on a value returned by `requestAnimationFrame` will cancel that frame (assuming it hasn’t already been called).

A similar set of functions, `setInterval` and `clearInterval`, are used to set timers that should _repeat_ every X milliseconds.

```js
let ticks = 0;
let clock = setInterval(() => {
  console.log("tick", ticks++);
  if (ticks == 10) {
    clearInterval(clock);
    console.log("stop.");
  }
}, 200);
```

## Debouncing

Some types of events have the potential to fire rapidly, many times in a row (the `"mousemove"` and `"scroll"` events, for example). When handling such events, you must be careful not to do anything too time-consuming or your handler will take up so much time that interaction with the document starts to feel slow.

If you do need to do something nontrivial in such a handler, you can use `setTimeout` to make sure you are not doing it too often. This is usually called _debouncing_ the event.

```html
<textarea>Type something here...</textarea>

<script>
  // We want to react when the user has typed something, but we don’t want to do it immediately for every input event. When they are typing quickly, we just want to wait until a pause occurs. Instead of immediately performing an action in the event handler, we set a timeout. We also clear the previous timeout (if any) so that when events occur close together (closer than our timeout delay), the timeout from the previous event will be canceled.
  let textarea = document.querySelector("textarea");
  let timeout;
  textarea.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => console.log("Typed!"), 500);
  });
</script>
```

Giving an undefined value to `clearTimeout` or calling it on a timeout that has already fired has no effect.

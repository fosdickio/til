# React Hooks

## Introduction

Hooks are a new addition in React 16.8 that allow you to use state and other React features without writing a class. They provide a more direct API to the React concepts like props, state, context, refs, and lifecycle. In essence, they are just functions that let you "hook into" React state and lifecycle features from function components.

## Rules of Hooks

Hooks are JavaScript functions, but they impose two additional rules:

1. Only call hooks **at the top level**. Don't call hooks inside loops, conditions, or nested functions.
2. Only call hooks **from React function components**. Don't call hooks from regular JavaScript functions (unless it's your own custom hook).

## State Hook

The `useState` hook is called inside a function component to add some local state to it. React will preserve this state between re-renders. The only argument to `useState` is the initial state. `useState` returns a pair: the current state value and a function that lets you update it. You can call this function from an event handler or somewhere else.

```javascript
import React, { useState } from "react";

function Example() {
  [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

## Effect Hook

Operations like data fetching, subscriptions, or manually changing the DOM from React components are called "side effects" (or "effects" for short). They can affect other components and can't be done during rendering.

The `useEffect` hook adds the ability to perform side effects from a function component. It serves the same purpose as `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount` in React classes, but unified into a single API.

When you call `useEffect`, you're telling React to run your "effect" function after flushing changes to the DOM. Effects are declared inside the component so they have access to its props and state. By default, React runs the effects after every render — including the first render.

Effects may also optionally specify how to "clean up" after them by returning a function. Just like with `useState`, you can use more than a single effect in a component

```javascript
import React, { useState, useEffect } from "react";

function FriendStatusWithCounter(props) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    document.title = `You clicked ${count} times`;
  });

  const [isOnline, setIsOnline] = useState(null);
  useEffect(() => {
    ChatAPI.subscribeToFriendStatus(props.friend.id, handleStatusChange);
    return () => {
      ChatAPI.unsubscribeFromFriendStatus(props.friend.id, handleStatusChange);
    };
  });

  function handleStatusChange(status) {
    setIsOnline(status.isOnline);
  }

  if (isOnline === null) {
    return "Loading...";
  }

  return isOnline ? "Online" : "Offline";
}
```

## Context Hook

The `useContext` hook accepts a context object (the value returned from `React.createContext`) and returns the current context value for that context. The current context value is determined by the value prop of the nearest `<MyContext.Provider>` above the calling component in the tree.

```javascript
const value = useContext(MyContext);
```

When the nearest `<MyContext.Provider>` above the component updates, this hook will trigger a rerender with the latest context value passed to that `MyContext` provider. A component calling `useContext` will always re-render when the context value changes.

```javascript
const themes = {
  light: {
    foreground: "#000000",
    background: "#eeeeee",
  },
  dark: {
    foreground: "#ffffff",
    background: "#222222",
  },
};

const ThemeContext = React.createContext(themes.light);

function App() {
  return (
    <ThemeContext.Provider value={themes.dark}>
      <ThemedButton />
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  const theme = useContext(ThemeContext);

  return (
    <button style={{ background: theme.background, color: theme.foreground }}>
      Themed Button
    </button>
  );
}
```

## Reducer Hook

The `useReducer` hook is an alternative to `useState`. It accepts a reducer of type `(state, action) => newState`, and returns the current state paired with a `dispatch` method.

`useReducer` is usually preferable to `useState` when you have complex state logic that involves multiple sub-values or when the next state depends on the previous one. `useReducer` also lets you optimize performance for components that trigger deep updates because you can pass dispatch down instead of callbacks.

```javascript
const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    default:
      throw new Error();
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: "decrement" })}>-</button>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
    </>
  );
}
```

## Ref Hook

`useRef` returns a mutable ref object whose `.current` property is initialized to the passed argument (`initialValue`). The returned object will persist for the full lifetime of the component.

Essentially, `useRef` is like a "box" that can hold a mutable value in its `.current` property. A common use case is to access a child imperatively.

```javascript
function TextInputWithFocusButton() {
  const inputEl = useRef(null);
  const onButtonClick = () => {
    // `current` points to the mounted text input element
    inputEl.current.focus();
  };

  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  );
}
```

Refs can serve as a way to access the DOM. If you pass a ref object to React with `<div ref={myRef} />`, React will set its `.current` property to the corresponding DOM node whenever that node changes.

However, `useRef()` is useful for more than the ref attribute. It's handy for keeping any mutable value around similar to how you'd use instance fields in classes.

This works because `useRef()` creates a plain JavaScript object. The only difference between `useRef()` and creating a `{current: ...}` object yourself is that `useRef` will give you the same ref object on every render.

Keep in mind that `useRef` doesn’t notify you when its content changes. Mutating the `.current` property doesn’t cause a re-render. If you want to run some code when React attaches or detaches a ref to a DOM node,then a [callback ref](https://reactjs.org/docs/hooks-faq.html#how-can-i-measure-a-dom-node) might be a better choice.

## Building Custom Hooks

Sometimes, we want to reuse some stateful logic between components. Traditionally, there were two popular solutions to this problem: _higher-order components_ and _render props_. Custom hooks let you do this, but without adding more components to your tree.

```javascript
import React, { useState, useEffect } from "react";

// Custom hook
function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);

  function handleStatusChange(status) {
    setIsOnline(status.isOnline);
  }

  useEffect(() => {
    ChatAPI.subscribeToFriendStatus(friendID, handleStatusChange);
    return () => {
      ChatAPI.unsubscribeFromFriendStatus(friendID, handleStatusChange);
    };
  });

  return isOnline;
}

// Custom hook used in component
function FriendStatus(props) {
  const isOnline = useFriendStatus(props.friend.id);
  if (isOnline === null) {
    return "Loading...";
  }
  return isOnline ? "Online" : "Offline";
}
```

The state of each component is completely independent. Hooks are a way to reuse stateful logic, not state itself. In fact, each _call_ to a hook has a completely isolated state — so you can even use the same custom Hook twice in one component.

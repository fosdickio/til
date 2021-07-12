# Redux Notes

## What is Redux?

Redux is a pattern and library for managing and updating application state, using events called "actions." It serves as a centralized store for state that needs to be used across your entire application, with rules ensuring that the state can only be updated in a predictable fashion.

## Why Redux?

The patterns and tools provided by Redux make it easier to understand when, where, why, and how the state in your application is being updated, and how your application logic will behave when those changes occur.

## Redux Libraries and Tools

Redux is a small standalone JS library. However, it is commonly used with several other packages:

### React-Redux

Redux can integrate with any UI framework and is most frequently used with React. [**React-Redux**](https://react-redux.js.org/) is our official package that lets your React components interact with a Redux store by reading pieces of state and dispatching actions to update the store.

### Redux Toolkit

[**Redux Toolkit**](https://redux-toolkit.js.org) is our recommended approach for writing Redux logic. It contains packages and functions that we think are essential for building a Redux app. Redux Toolkit builds on our suggested best practices, simplifies most Redux tasks, prevents common mistakes, and makes it easier to write Redux applications.

### Redux DevTools Extension

The [**Redux DevTools Extension**](https://github.com/zalmoxisus/redux-devtools-extension) shows a history of the changes to the state in your Redux store over time. This allows you to debug your applications effectively, including using powerful techniques like "time-travel debugging".

## Terminology

### Actions

An **action** is a plain JavaScript object that has a `type` field. **You can think of an action as an event that describes something that happened in the application**.

The `type` field should be a string that gives this action a descriptive name, like `"todos/todoAdded"`. The type string is usually written in the form `"domain/eventName"`, where the first part is the feature or category that this action belongs to and the second part is the specific event that happened.

An action object can have other fields with additional information about what happened. By convention, we put that information in a field called `payload`.

```js
const addTodoAction = {
  type: "todos/todoAdded",
  payload: "Buy milk",
};
```

#### Action Creators

An **action creator** is a function that creates and returns an action object. They are typically used so that we don't have to write the action object by hand every time.

```js
const addTodo = (text) => {
  return {
    type: "todos/todoAdded",
    payload: text,
  };
};
```

#### Reducers

A **reducer** is a function that receives the current `state` and an `action` object, decides how to update the state if necessary, and returns the new state (`(state, action) => newState`). **You can think of a reducer as an event listener which handles events based on the received action (event) type.**

Reducers must _always_ abide by the following rules:

- They should only calculate the new state value based on the `state` and `action` arguments.
- They are not allowed to modify the existing `state`. Instead, they must make _immutable updates_, by copying the existing `state` and making changes to the copied values.
- They must not do any asynchronous logic, calculate random values, or cause other "side effects."

```js
const actions = [
  { type: "counter/increment" },
  { type: "counter/decrement" },
  { type: "counter/reset" },
];

const initialState = { value: 0 };

function counterReducer(state = initialState, action) {
  // Check to see if the reducer cares about this action
  if (action.type === "counter/increment") {
    // If so, make a copy of `state`
    return {
      ...state,
      // Update the copy with the new value
      value: state.value + 1,
    };
  }
  // Returns the existing `state` if unchanged
  return state;
}

const finalResult = actions.reduce(counterReducer, initialState);
console.log(finalResult);
// {value: 3}
```

#### Store

The current Redux application state lives in an object called the **store**.

The store is created by passing in a reducer and has a method called `getState` that returns the current state value.

```js
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({ reducer: counterReducer });

console.log(store.getState());
// {value: 0}
```

#### Dispatch

The Redux store has a method called `dispatch`. **The only way to update the state is to call `store.dispatch()` and pass in an action object**. The store will run its reducer function and save the new state value inside. We can then call `getState()` to retrieve the updated value.

```js
store.dispatch({ type: "counter/increment" });

console.log(store.getState());
// {value: 1}
```

**You can think of dispatching actions as "triggering an event"** in the application. It means that an event happened and we want the store to know about it. Reducers act like event listeners and update the state when they hear about an action they are interested in.

It is common practice to call action creators to dispatch the right action.

```js
const increment = () => {
  return {
    type: "counter/increment",
  };
};

store.dispatch(increment());

console.log(store.getState());
// {value: 2}
```

#### Selectors

**Selectors** are functions that know how to extract specific pieces of information from a store state value. As an application grows bigger, this can help avoid repeating logic since different parts of the app need to read the same data.

```js
const selectCounterValue = (state) => state.value;

const currentValue = selectCounterValue(store.getState());
console.log(currentValue);
// 2
```

### Redux Application Data Flow

Earlier, we talked about "one-way data flow", which describes this sequence of steps to update the app. These steps are:

1. State describes the condition of the app at a specific point in time.
2. The UI is rendered based on that state.
3. When something happens (such as a user clicking a button), the state is updated (based on what occurred).
4. The UI re-renders based on the new state.

For Redux specifically, we can break these steps out into more detail:
**Initial Setup**

1. A Redux store is created using a root reducer function.
2. The store calls the root reducer once and saves the return value as its initial `state`.

**Updates**

1. When something happens in the app (such as a user clicking a button), the app code dispatches an action to the Redux store (like `dispatch({type: 'counter/increment'})`).
2. The store runs the reducer function again with the previous `state` and the current `action`. It then saves the return value as the new `state`.
3. The store notifies all subscribed parts of the UI that the store has been updated.
4. Each UI component that needs data from the store checks to see if the parts of the state they need have changed.
5. Each component that sees its data has changed forces a re-render with the new data, so that it can update what's shown on the screen.

Here's what that data flow looks like visually:

![Redux Data Flow Diagram](img/redux-data-flow-diagram.gif)

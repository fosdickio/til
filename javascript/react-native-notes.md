# React Native Notes

## Overview
- A framework that relies on React core
- Allows us build mobile apps using only JavaScript
- Supports iOS and Android

## How does React Native work?
- JavaScript is bundled (transpiled and minified)
- Separate threads for UI, layout, and JavaScript
- Communicate asynchronously through a "bridge"
  - JavaScript thread will request UI elements to be shown
  - JavaScript thread can be blocked and UI will still work

## Differences between React Native and Web
- Base components
- Style
- No browser APIs
  - CSS animations, Canvas, SVG, etc.
  - Some have been polyfilled (fetch, timers, console, etc.)
- Navigation

## React Native Components
- Not globally in scope like React web components
  - Import from `react-native`
- `div` → `View`
- `span` → `Text`
  - All text must be wrapped by a `<Text />` tag
- `button` → `Button`
- `ScrollView`

## Style
- React Native uses JavaScript objects for styling
- Object keys are based on CSS properties
- Flexbox layout
  - Defaults to column layout
- Lengths are in unitless numbers
- `style` prop can take an array of styles
- `StyleSheet.create()`
  - Functionally the same as creating objects for style
  - Additional optimization: only sends IDs over the bridge

## Event Handling
- Unlike web, not every component has every interaction
- Only a few "touchable" components
  - `Button`
  - `TouchableOpacity`, `TouchableHighlight`, `TouchableWithoutFeedback`
  - `TouchableNativeFeedback` (Android only)
- Web handlers will receive the event as an argument, but React Native handlers often receive different arguments

## Todo App Example
```javascript
import React from 'react';
import {View, Button, Text, ScrollView, StyleSheet, Switch} from 'react-native'
import {Constants} from 'expo'

let id = 0

const styles = StyleSheet.create({
  todoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  appContainer: {
    paddingTop: Constants.statusBarHeight,
  },
  fill: {
    flex: 1,
  }
})

const Todo = props => (
  <View style={styles.todoContainer}>
    <Switch value={props.todo.checked} onValueChange={props.onToggle} />
    <Button onPress={props.onDelete} title="Delete" />
    <Text>{props.todo.text}</Text>
  </View>
)

export default class App extends React.Component {
  constructor() {
    super()
    this.state = {
      todos: [],
    }
  }

  addTodo() {
    id++
    const text = `Todo #${id}`
    this.setState({
      todos: [
        ...this.state.todos,
        {id: id, text: text, checked: false},
      ], 
    })
  }

  removeTodo(id) {
    this.setState({
      todos: this.state.todos.filter(todo => todo.id !== id)
    })
  }

  toggleTodo(id) {
    this.setState({
      todos: this.state.todos.map(todo => {
        if (todo.id !== id) return todo
        return {
          id: todo.id,
          text: todo.text,
          checked: !todo.checked,
        }
      })
    })
  }

  render() {
    return (
      <View style={[styles.appContainer, styles.fill]}>
        <Text>Todo count: {this.state.todos.length}</Text>
        <Text>Unchecked todo count: {this.state.todos.filter(todo => !todo.checked).length}</Text>
        <Button onPress={() => this.addTodo()} title="Add Todo" />
        <ScrollView style={styles.fill}>
          {this.state.todos.map(todo => (
            <Todo
              onToggle={() => this.toggleTodo(todo.id)}
              onDelete={() => this.removeTodo(todo.id)}
              todo={todo}
            />
          ))}
        </ScrollView>
      </View>
    )
  }
}
```

## Components
- Return a node (something that can be rendered)
- Represent a discrete piece of the UI
- "All React components must act like pure functions with respect to their props."
- Two types:
  - Stateless Functional Component (SFC) aka Pure Functional Component
  - `React.Component`

## Stateless Functional Component (SFC)
- Simplest component: use when you don’t need state
- A function that takes props and returns a node
  - Should be "pure" (it should not have any side effects like setting values, updating arrays, etc.)
- Any change in props will cause the function to be re-invoked

## `React.Component`
- An abstract class that can be extended to behave however you want
- These have additional features that SFCs don’t
  - Have instances
  - Maintain their own state
  - Have lifecycle methods (similar to hooks or event handlers) that are automatically invoked
- Rendering now becomes a function of props and class properties

## Mount
- `constructor(props)`
  - Initialize state or other class properties (bound methods, etc.)
- `render()`
  - The meat of a component
  - Returns a node
- `componentDidMount()`
  - Do anything that isn’t needed for UI (async actions, timers, etc.)
  - Setting state here will cause a re-render before updating the UI

## Update
- `componentWillReceiveProps(nextProps)`
  - Update any state fields that rely on props
- `shouldComponentUpdate(nextProps, nextState)`
  - Compare changed values, return true if the component should re-render
    - If returned false, the update cycle terminates
  - Almost always a premature optimization
- `render()`
- `componentDidUpdate(prevProps, prevState)`
  - Do anything that isn’t needed for UI (network requests, etc.)

## Unmount
- `componentWillUnmount()`
  - Clean up
    - Remove event listeners
    - Invalidate network requests
    - Clear timeouts/intervals

## Expo
- "The fastest way to build an app"
- Suite of tools to accelerate the React Native development process
  - Snack - runs React Native in the browser
  - XDE - a GUI to serve, share, and publish your Expo projects
  - CLI - a command-line interface to serve, share, and publish projects
  - Client - runs your projects on your phone while developing
  - SDK - bundles and exposes cross-platform libraries and APIs

## Import/Export
- Components are great for simplifying code
- We can split components into their own files
  - Helps organize the project
  - Can export the component from the file
- Import the component before using it in a file
- Default vs. named import/export

## PropTypes
- React can validate the types of component props at runtime
- Development tool that allows developers to ensure they’re passing correct props
- Helps document your components' APIs
- Only runs in development mode

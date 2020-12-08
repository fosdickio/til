# GraphQL Notes

## Background
- GraphQL is a new API standard.
- It was developed and open-sourced by Facebook and is now maintained by a large community.
- An API defines how a client can load data from a server.

## Introduction
- GraphQL enables declarative data fetching where a client can specify exactly what data it needs from an API.
- Instead of multiple endpoints that return fixed data structures, a GraphQL server only exposes a single endpoint and responds with precisely the data a client asked for.
- GraphQL is a query language for APIs - not databases.
  - It’s database agnostic and effectively can be used in any context where an API is used.

## Data Fetching
With a REST API, you would typically gather the data by accessing multiple endpoints.

![REST Data Fetching](img/rest-data-fetching.png)

In GraphQL on the other hand, you’d simply send a single query to the GraphQL server that includes the concrete data requirements.  The server then responds with a JSON object where these requirements are fulfilled.

![GraphQL Data Fetching](img/graphql-data-fetching.png)

## Schema and Type System
- GraphQL uses a strong type system to define the capabilities of an API.
- All the types that are exposed in an API are written down in a schema using the GraphQL Schema Definition Language (SDL).
- This schema serves as the contract between the client and the server to define how a client can access the data.

### The Schema Definition Language (SDL)
Here is an example of how we can use the SDL to define a simple type called `Person`:

```
type Person {
  name: String!
  age: Int!
}
```

It’s also possible to express relationships between types.  In the example of a blogging application, a `Person` could be associated with a `Post`:

```
type Post {
  title: String!
  author: Person!
}
```

Conversely, the other end of the relationship needs to be placed on the `Person` type:

```
type Person {
  name: String!
  age: Int!
  posts: [Post!]!
}
```

This just created a one-to-many-relationship between `Person` and `Post` since the posts field on `Person` is actually an array of posts.

### Defining a Schema
Generally, a schema is simply a collection of GraphQL types. However, when writing the schema for an API, there are some special root types:

```
type Query { ... }
type Mutation { ... }
type Subscription { ... }
```

The `Query`, `Mutation`, and `Subscription` types are the entry points for the requests sent by the client.

Here is an example of a full schema:

```
type Query {
  allPersons(last: Int): [Person!]!
}

type Mutation {
  createPerson(name: String!, age: Int!): Person!
}

type Subscription {
  newPerson: Person!
}

type Person {
  name: String!
  age: Int!
  posts: [Post!]!
}

type Post {
  title: String!
  author: Person!
}
```

## Error Handling
A successful GraphQL query is supposed to return a JSON object with a root field called `data`. If the request fails or partially fails, a second root field called `errors` is added to the response:

```
{
  "data": { ... },
  "errors": [ ... ]
}
```

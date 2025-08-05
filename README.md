# Bloggu

Bloggu is a simple blogging platform API built with FastAPI, SQLAlchemy, and Strawberry GraphQL. It supports user authentication, comment posting, and comment history tracking, with group-based access control.

## Features

- User sign up, login, and JWT-based authentication
- Group-based user management
- Comment creation, update, and deletion
- Comment history tracking
- REST endpoints for authentication
- GraphQL API for all CRUD operations

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

### Setup

1. Clone the repository and navigate to the project directory.

2. Copy `.example.env` and adjust values if needed (default values are provided).

3. Build and start the services:

```sh
docker compose up --build
```

This will start the FastAPI app on [http://localhost:8000/graphql](http://localhost:8000/graphql) and a PostgreSQL database.

## Usage

### 1. Sign Up

```sh
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "123", "group": "B"}'
```

### 2. Login

```sh
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=123"
```

Copy the `access_token` from the response.

### 3. Use GraphQL Playground

Go to [http://localhost:8000/graphql](http://localhost:8000/graphql) in your browser.

In the "Headers" section, add:

```json
{
  "Authorization": "Bearer <your_bearer_token>"
}
```

Replace `<your_bearer_token>` with the token from the login step.

---

## Example GraphQL Queries & Mutations

### User

**Update User**

```graphql
mutation {
  updateUser(username: "bob-renamed", group: "admin") {
    id
    username
    group
  }
}
```

**Delete User**

```graphql
mutation {
  deleteUser
}
```

**Get All Users**

```graphql
query {
  allUsers {
    id
    username
    group
  }
}
```

**Get User by ID**

```graphql
query {
  userById(userId: 1) {
    id
    username
    group
  }
}
```

### Comment

**Create Comment**

```graphql
mutation {
  createComment(content: "Hello world!") {
    id
    content
    userId
  }
}
```

**Update Comment**

```graphql
mutation {
  updateComment(commentId: 1, newContent: "Updated content") {
    id
    content
    userId
  }
}
```

**Delete Comment**

```graphql
mutation {
  deleteComment(commentId: 1)
}
```

**Get All Comments**

```graphql
query {
  allComments {
    id
    content
    userId
  }
}
```

**Get Comment by ID**

```graphql
query {
  commentById(commentId: 1) {
    id
    content
    userId
  }
}
```

### Comment History

**Get All Comment Histories**

```graphql
query {
  allCommentHistories {
    id
    commentId
    timestamp
    oldValue
    newValue
  }
}
```

**Get Comment History by ID**

```graphql
query {
  commentHistoryById(historyId: 1) {
    id
    commentId
    timestamp
    oldValue
    newValue
  }
}
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE)

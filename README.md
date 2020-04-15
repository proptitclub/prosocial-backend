# How the APIs works

## Posts, reactions, comments

- Get all Posts

  - Post
  - Reaction count
  - Comment count

- Get Posts with Id

  - Post
  - Reaction
  - Comment

- Post Post

  - Auth with user-group-role
  - Save Post

- Config Post

  - Save Post

- Delete Post

  - Delete all Reaction by Post Id
  - Delete all Comment by Post Id
  - Delete Post

- Post Reaction with Post Id
- Post Comment with Post Id
- Config, Delete Reaction
- Config, Delete Comment

## How the authentication work
- how to get token: POST request to "/api-auth/token/obtain/" with a header contain "Content-Type: application/json",
POST request body include "username" and "password"
- returned token include 2 token: "access" token exist in 5 minutes, "refresh" token exist in 1 day
- when access token is expried, POST request to "/api-auth/token/refresh/" with header contain "Content-Type: application/json", POST request body include "refresh" token, it gonna return "access" token back
- when request to url with authentication, put "Authorization: Bearer {}".format(access_token) to the request header
# How the APIs works

## Posts, reactions, comments

- Get all Posts(Done)

  - Post(Done)
  - Reaction count(Done)
  - Comment count(Done)

- Get Posts with Id (Done)

  - Post(Done)
  - Reaction(Done)
  - Comment(Done)

- Post Post(Done)

  - Auth with user-group-role (Done)
  - Save Post (Done)

- Config Post (Done)

  - Save Post(Done)

- Delete Post (Done)

  - Delete all Reaction by Post Id
  - Delete all Comment by Post Id
  - Delete Post

- Post Reaction with Post Id(Done)
- Post Comment with Post Id(Done)
- Config, Delete Reaction(Done)
- Config, Delete Comment(Done)

## How the authentication work
- how to get token: POST request to "/auth/jwt/create/" with a header contain "Content-Type: application/json",
POST request body include "username" and "password"
- returned token include 2 token: "access" token exist in 5 minutes, "refresh" token exist in 1 day
- when access token is expried, POST request to "auth/jwt/refresh/" with header contain "Content-Type: application/json", POST request body include "refresh" token, it gonna return "access" token back
- when request to url with authentication, put "Authorization: Bearer {}".format(access_token) to the request header
- get auth user:
    - access "auth/users/me/" for auth user information

## Update Authenticated User
- PATCH -> /auth/users/me/ : update non-sercured infomation, include avatar, url, id, username, display_name, phone_number, facebook, role, date_of_birth, description, email, user_gender, cover

- POST -> /auth/users/set_password/ : update pass word, body: new_password, re_new_password, current_password
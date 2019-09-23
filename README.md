
### Introduction

A starter API services (Skeleton) using Python Flask and Authentication using Basic Authentication & JSON Web Tokens (JWT) approach.
This code deployable to Cloud Foundry.

### Instructions

Do `git clone` this repository, you should have `cf-flask-auth` folder.

##### Cloud Foundry

Login to your Cloud Foundry account.

> $ cd cf-flask-auth

> $ cf push

Navigate to CF App Route to access the APIs.


##### Local Machine

Do `git clone` this repository, you should have `cf-flask-auth` folder.

> $ cd cf-flask-auth

> $ python run.py


API endpoints:

```
http://localhost:5000/ -- no authentication
http://localhost:5000/v1/ba/welcome  -- requires basic authentication to access
http://localhost:5000/v1/jwt/user -- requires user json payload register
http://localhost:5000/v1/jwt/welcome  -- requires JWT to access
http://localhost:5000/v1/jwt/refresh -- requires JWT to access
```








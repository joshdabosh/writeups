# No-Signature,-No-Problem
Web, 200

> We're using the latest tech to authenticate you to this site: https://8efc5a73607de8.codecupchallenge.com/

Again, we are tasked with logging in as admin.

When we submit a sample password, we notice that a JWT gets sent in the URL as the `token` parameter.

Taking from the title, we reason that it's a alg:none attack.

[JWT.io](https://jwt.io) is a great resource to use.

We base64 decode, and change our JWT's header to `{"alg":"none","typ":"JWT"}`.

Then, we change our JWT body's `isAdmin` attribute to `true`.

We ignore the signature, and don't include in the final token since we don't need it at all.

Our final token will be something like
`eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpc0FkbWluIjp0cnVlLCJpYXQiOjE1ODU3ODU0MjR9.`

Note the periods separating the head, body, and signature.

Even though there is no signature, we need to include the `.` at the end in order for the parsing to work.

Accessing the page again with our crafted token gives the flag.

Flag: `car-twelve`

# Snickerdoodle
Web, 100

> https://0e1a313d7a6d3.codecupchallenge.com/

We are presented with a password field, and we reason that when we authenticate we'll get the flag.

Submitting a sample password, we notice that an `is_admin=0` cookie gets added to our session.

Let's change that to `is_admin=1`.

We visit the home page again, and we get the flag.

Flag: `regular-crowd`

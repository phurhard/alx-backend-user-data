# User data
- This repository contains tasks from ALX SE Backend specialization.

## Directories

- The directories included in this repo are

* [0x00-personal_data](0x00-personal_data)
    This folder contains tasks and lessons on how user personal details can be protected
    this is crucial as a backend developer because the details of users are higly sensitive date that must not be toyed with.
    There are specific laws guiding what is regarded as PII and what is not
* [0x01-Basic_authentication](0x01-Basic_authentication)
    This folder contains a basic authentication implementation
    
    ```Never implement your own authentication system, it's advisable to make use of industry and well known strong authentication services, like Flask-User```
* [0x02-Session_authentication](0x02-Session_authentication)
    This is a continuation of users authentication
    This section focuses on session, which the server uses to keep track of the active user
* [0x03-user_authentication_service](0x03-user_authentication_service)
    This is a grand cover of the user authentication system.
    In this directory, i created a user model, a db model, and a flask app. 
    Also i wrote a test to confirm all enmdpoints are working as required. The user authentication service is an implementation of how to ensure the user is authenticated before being given permissions to the site, and keeping track of the users session.
    This incorporates the session authentication parts of user authentication services.
- * Do not authenticate users yourself, use industry best practices and well known tools

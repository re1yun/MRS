MRS v2 Manual
=============

Registration
-------------
1. Add user
>curl -X POST 'http://localhost:8080/v2/customers/{customer id}'
2. Add user name
>curl -X PUT 'http://localhost:8080/v2/customers/{customer id}?name={name}'
3. Add user listen history
>curl -X PUT 'http://localhost:8080/v2/customers/{customer id}/listened/{song id}'

Get Information
---------------
1. User
>curl -X GET 'http://localhost:8080/v2/customers/{customer id}'
2. User listen history
>curl -X GET 'http://localhost:8080/v2/customers/{customer id}/listened'
3. Song
>curl -X GET 'http://localhost:8080/v2/songs/{song id}'

Delete
------
1. User
>curl -X DELETE 'http://localhost:8080/v2/customers/{customer id}'
2. User listen history
>curl -X DELETE 'http://localhost:8080/v2/customers/{customer id}/listened/{song id}'

Suggestion
----------
1. User
>curl -X GET 'http://localhost:8080/v2/customers/{customer id}/suggestion'

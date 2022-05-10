
### Requirements 📌
* Docker 🐳
* docker-compose 🐳
* Python 3.6 

### Run FastAPI Docker ⚡ Local Development
1. git clone https://github.com/meriem-s/user-service.git
2. `docker pull postgres:14`
3. `docker build .`
4. `docker-compose up`
5. That's just all, api server listens to http://localhost:8000/ now

# REST API DEFINITION

The REST API to the user service app is described below.


### Create user data in the database

`POST /create-user`

```
curl -X 'POST' \
  'http://localhost:8000/create-user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
      
"firstname" : "meriem",
"lastname": "said",
"mail": "saidmeriem96@gmail.com",
"phoneNumber" : "004912345678"
}'
```

#### Response

`Status: 200 OK`
```
{
  "id": 1,
  "firstname": "meriem",
  "lastname": "said",
  "emails": [
    {
      "mail": "saidmeriem96@gmail.com",
      "id": 1
    }
  ],
  "phonenumbers": [
    {
      "id": 1,
      "number": "004912345678"
    }
  ]
}
```
```
 content-length: 149 
 content-type: application/json 
 date: Mon,09 May 2022 22:48:26 GMT 
 server: uvicorn 
```
### Get User by Id or by Name
#### Requests

`GET /users?name={name}`

`GET /users?user_id={user_id}`

#### Response
`Status: 200 OK`

```
{
  "id": 1,
  "firstname": "meriem",
  "lastname": "said",
  "emails": [
    {
      "mail": "saidmeriem96@gmail.com",
      "id": 1
    }
  ],
  "phonenumbers": [
    {
      "id": 1,
      "number": "004912345678"
    }
  ]
}
```
```
 content-length: 149 
 content-type: application/json 
 date: Mon,09 May 2022 22:49:55 GMT 
 server: uvicorn 
```

### Add user data (phone number /email )

#### Request
`PUT /add-data/{user_id}`


```
curl -X 'PUT' \
  'http://localhost:8000/add-data/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
{
  "mail": "saidmeriem96@yahoo.com",
  "number": "0021612345678"
}'
```
#### Response
`Status: 200 OK`

```
{
  "id": 1,
  "firstname": "meriem",
  "lastname": "said",
  "emails": [
    {
      "mail": "saidmeriem96@gmail.com",
      "id": 1
    },
    {
      "mail": "saidmeriem96@yahoo.com",
      "id": 2
    }
  ],
  "phonenumbers": [
    {
      "id": 1,
      "number": "004912345678"
    },
    {
      "id": 2,
      "number": "0021612345678"
    }
  ]
}

```

```
 content-length: 47 
 content-type: application/json 
 date: Mon,09 May 2022 22:51:37 GMT 
 server: uvicorn
``` 

### Update user data in the database
#### Request

`PUT /update-user{user_id}`

```
curl -X 'PUT' \
  'http://localhost:8000/update/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "old_mail": "saidmeriem96@yahoo.com",
  "new_mail":"new_maisl@gmail.com" ,
  "old_number": "004912345678",
  "new_number": "0049122221234567"
}'
```
#### Response
`Status: 200 OK`

```
{
  "msg": "Update Sucessful"
}
```
```
 content-length: 26 
 content-type: application/json 
 date: Mon,09 May 2022 23:05:00 GMT 
 server: uvicorn 
```

### Delete user data from the database
#### Request

`DELETE /delete-user/{user_id}`

```
curl -X 'DELETE' \
  'http://localhost:8000/delete-user/1' \
  -H 'accept: application/json'
```
#### Reponse
`Status: 200 OK`


### Testing  🚨
under the main directory run: 
```
pytest
```
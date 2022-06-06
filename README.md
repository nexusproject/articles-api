# Articles API Server
This is a fully asynchronous API server, that realizes headless (no UI) CMS for managing articles (CRUD).

Technologies: Python 3.9, FastAPI, MySQL Percona Server 8, SQLAlchemy

Made for fun :-)

## Running
##### Using Docker Compose:
`make run_docker`
or
`docker compose up --abort-on-container-exit`

##### Run server with local installed MySQL:
`DATABASE_URL=mysql://root:@127.0.0.1:3306/articles make run`

## Access to API
The server responds on port 8000.

For methods to create, delete, update requires authorization by HTTP field with a constant token.

`Authorization: some_hardcoded_token`

##### Access from console (examples)
###### Creating article
```
curl -X POST http://localhost:8000/api/v1/create \
  -H 'Authorization: some_hardcoded_token' \
  -H 'Content-Type: application/json' \
  -d '{"topic":"Marge Simpson story", "text": "text text text"}'
```
###### Updating article
```
curl -X PATCH http://localhost:8000/api/v1/article/1 \
  -H 'Authorization: some_hardcoded_token' \
  -H 'Content-Type: application/json' \
  -d '{"topic":"Other topic", "text": "some text"}'
```
###### Deleting article
```
curl -X DELETE http://localhost:8000/api/v1/article/1 
  -H 'Authorization: some_hardcoded_token'
```
###### Get one article by id
```
curl -X GET http://localhost:8000/api/v1/article/1
```
###### Get list of articles
```
curl -X GET http://localhost:8000/api/v1/list?from_date=2022-06-02T15:40:00\&sort_order=desc\&sort_by=updated\&page_size=30\&page=1
```
All query options are optional

##### Access from WEB, docs and openapi schema
[Link to Docs](http://localhost:8000/docs)

[Link to openapi schema](http://localhost:8000/openapi.json)


## Running Tests
##### With Docker Compose:
`make test_docker`
or
`docker compose -f docker-compose.testing.yml up --abort-on-container-exit --force-recreate`
##### Without Docker, with local installed MySQL:
`TEST_DATABASE_URL=mysql://root:@127.0.0.1:3306/__articles_test make test`

Be careful! the test database will be deleted after passing the tests!

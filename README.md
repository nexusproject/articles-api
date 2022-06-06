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

## Running Tests
##### With Docker Compose:
`make test_docker`
or
`docker compose -f docker-compose.testing.yml up --abort-on-container-exit --force-recreate`
##### Without Docker, with local installed MySQL:
`TEST_DATABASE_URL=mysql://root:@127.0.0.1:3306/__articles_test make test`

Be careful! the test database will be deleted after passing the tests!

TAG = ghcr.io/nexusproject/xx/articles-api:latest

build:
	docker build --tag $(TAG) .

push: build
    docker push $(TAG)

test: export DATABASE_URL=$(TEST_DATABASE_URL)
test:
	dbmate up
	env PYTHONPATH=. poetry run pytest --flake8
	dbmate drop

test_docker:
	docker compose -f docker-compose.testing.yml up --abort-on-container-exit --force-recreate

migrate:
	dbmate up

run: migrate
	poetry run uvicorn articles.api:app --host 0.0.0.0 --port 8000 --reload

run_docker:
	docker compose up --abort-on-container-exit

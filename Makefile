run:
	poetry run uvicorn articles.api:app --host 0.0.0.0 --port 8000 --reload
test:
	env PYTHONPATH=. poetry run pytest --flake8

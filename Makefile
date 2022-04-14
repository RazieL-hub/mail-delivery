start:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

mkm:
	docker exec -it mail_web alembic revision --autogenerate

m:
	docker exec -it mail_web alembic upgrade head

md:
	docker exec -it mail_web alembic downgrade base

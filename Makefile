setup:
	pip install -r requirements.txt

	docker-compose up -d

	alembic upgrade head
part1:
	python3 part1.py
part2:
	python3 part2.py
part3:
	python3 part3.py

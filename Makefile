.PHONY: build
build:
	mkdir site || :
	python main.py

format:
	ruff main.py --fix
	black main.py

lint:
	black --check main.py
	ruff main.py

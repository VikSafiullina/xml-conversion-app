compile-deps:
	@echo "Compiling production dependencies..."
	@pip install pip-tools
	@pip-compile requirements.in > requirements.txt
	@pip wheel --wheel-dir=./wheels -r requirements.txt
	@echo "Production dependencies compiled!"

run-app-locally:
	@echo "Running app..."
	@uvicorn app.main:app --reload --port 8000

prepare-env:
	@echo "Preparing environment..."
	@python3 -m venv venv
	@echo "Activating virtual environment and installing all dependencies..."
	@. venv/bin/activate && pip install --upgrade pip && pip install pip-tools && pip-compile requirements.in && pip install --use-pep517 -r requirements.txt && pip install --upgrade graphene-sqlalchemy==3.0.0rc1 graphene==v3.3.0 && pip install "strawberry-graphql[debug-server]"
	@echo "Done!"
.PHONY: run test format clean venv

# Run the main program
run:
	python3 src/main.py

# Run unit tests
test:
	PYTHONPATH=src pytest tests/

# Format code with Black
format:
	black src tests

# Clean cache and logs
clean:
	find . -type d -name "__pycache__" -exec rm -r {} \;
	rm -f logs.txt

# Set up and activate virtual environment
venv:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

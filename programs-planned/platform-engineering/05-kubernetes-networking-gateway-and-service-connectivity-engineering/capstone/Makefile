PYTHON ?= python3
.PHONY: test tour clean

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

tour:
	PYTHONPATH=. $(PYTHON) scripts/capstone_tour.py

clean:
	PYTHONPATH=. $(PYTHON) scripts/clean.py

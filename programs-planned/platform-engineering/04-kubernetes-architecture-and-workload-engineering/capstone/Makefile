PYTHON ?= python3
export PYTHONPATH := $(CURDIR)
.PHONY: test tour go-test

test:
	$(PYTHON) -m pytest -q tests

tour:
	cd .. && $(PYTHON) scripts/capstone_tour.py

go-test:
	cd controller-go && go test ./...

SRC = $(PWD)/src
AWS_PROFILE = tudev
PYTHON = python3
CHALICE = chalice --project-dir $(SRC)
STAGE = dev

.PHONY: unit test coverage

deps: .deps
.deps: requirements.txt
	pip3 install -r requirements.txt
	touch .deps

run: deps
	$(CHALICE) local

unit test: deps $(TOOLS)
	cd $(SRC);\
	$(PYTHON) -m pytest ../tests

coverage: deps $(TOOLS)
	cd $(SRC);\
	$(PYTHON) -m pytest ../tests --cov $(SRC) --cov-report=term-missing ../tests

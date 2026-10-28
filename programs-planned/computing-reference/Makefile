.PHONY: test validate validate-blueprint

test:
	python3 -m unittest discover -s tests/course_validation

validate: test validate-blueprint

validate-blueprint:
	python3 tools/validate_blueprint.py

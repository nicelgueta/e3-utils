
.PHONY: clean-env new-env reset-env
clean-env:
	rm -rf venv
new-env:
	python -m venv venv
	pip install -r requirements.txt
reset-env: clean-env new-env

.PHONY: add-pkg rm-pkg
add-pkg:
	pip install $(filter-out $@, $(MAKECMDGOALS))
	pip freeze > requirements.txt
rm-pkg:
	pip uninstall $(filter-out $@, $(MAKECMDGOALS))
	pip freeze > requirements.txt
%:
	@true
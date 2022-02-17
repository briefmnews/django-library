clean:
	rm -rf *.egg-info .pytest_cache
	rm -rf htmlcov
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

coverage:
	pytest --cov=django_library tests

report:
	pytest --cov=django_library --cov-report=html tests

install:
	pip install -r test_requirements.txt

release:
	git tag -a $(shell python -c "from django_library import __version__; print(__version__)") -m "$(m)"
	git push origin --tags
PYTHON = python


clean:
	@echo "Cleaning up..."
	rm -rf ./metar_taf_parser_mivek.egg-info/
	rm -rf ./build/
	rm -rf ./dist/
	rm -rf ./htmlcov/
	rm -rf ./.coverage
	rm -rf ./coverage.json
	rm -rf ./coverage.xml

test:
	@echo "Launching test"
	${PYTHON} -m pipenv run coverage run -m unittest

report: test
	${PYTHON} -m pipenv run coverage html
	${PYTHON} -m pipenv run coverage xml
	${PYTHON} -m pipenv run coverage json

lock:
	${PYTHON} -m pipenv lock

install:
	@echo "Install dependencies"
	${PYTHON} -m pip install flake8 pipenv
	${PYTHON} -m pipenv install -d
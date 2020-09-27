PYTHON=python3.8

# ========== Linux (Debian) ==========


# ----- Install -----

install:
	$(if $(shell apt-cache search $(PYTHON)), , \
		sudo add-apt-repository -y ppa:fkrull/deadsnakes && apt-get update)
	sudo apt-get install -y build-essential
	sudo apt-get install -y $(PYTHON) $(PYTHON)-dev $(PYTHON)-venv cython


# ----- Virtualenv -----

venv-init:
	if [ ! -e "venv/bin/activate" ]; then $(PYTHON) -m venv venv ; fi;
	bash -c "source venv/bin/activate && \
		pip install --upgrade wheel pip setuptools && \
		pip install --upgrade --requirement requirements.txt"


# ----- Update -----

update: venv-init

update-dev: venv-init
	bash -c "source venv/bin/activate && \
		pip install --upgrade --requirement requirements-dev.txt"


# ----- Setup -----

setup: install venv-init

setup-dev: install update-dev


# ----- Clean -----

clean:
	-@rm -rf build/
	-@find . \( \
		-name "__pycache__" -o \
		-name "*.pyc" -o \
		-name ".pytest_cache" -o \
		-name ".cache" \) \
		-prune \
		-exec rm -rf {} \;
	@rm -f .coverage
	@rm -rf .cov_html


# ----- Tests -----

test: update-dev
	bash -c "source venv/bin/activate && \
		python -m pytest ./tests -vv ./tests ./funi --flake8 \
		--cov ./funi --cov-fail-under=80"

test-cov: update-dev
	bash -c "source venv/bin/activate && \
		python -m pytest --cov ./funi --cov-report html:.cov_html \
		--cov-report term ./tests/ -vv ./tests ./funi --flake8 && \
		python -m webbrowser -t 'file://`pwd`/.cov_html/index.html'"


# ----- Code analysis -----

pylint-check: update-dev
	bash -c "source venv/bin/activate && \
		python -m pylint funi/ tests/"

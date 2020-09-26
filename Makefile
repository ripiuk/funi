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


# ----- Setup -----

setup: install venv-init


# ----- Tests -----

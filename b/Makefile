NAME := krpsim

.PHONY: install clean

install:
	@python3 -m pip install -r requirements.txt
	@python3 -m pip install --user -e .

clean:
	@python3 setup.py clean
	@rm -rf sources/$(NAME)/__pycache__/	2> /dev/null || true
	@rm -rf sources/$(NAME).egg-info/ 		2> /dev/null || true

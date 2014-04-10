# Simple Makefile for some common tasks. This will get
# fleshed out with time to make things easier on developer
# and tester types.
.PHONY: test clean

test:
	py.test -x --tb=short tests

clean:
	find . -name "*.pyc" | xargs rm || true

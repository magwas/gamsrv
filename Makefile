all: tests

clean:
	rm -rf html xml; find -name '*.pyc'|xargs rm

docs:
	doxygen Doxyfile

tests:
	python -m unittest discover -p "*.py" -v

all: tests

clean:
	rm -rf html xml

docs:
	doxygen Doxyfile

tests:
	python -m unittest discover -p "*.py" -v

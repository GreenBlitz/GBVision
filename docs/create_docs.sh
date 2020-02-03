#DONT REMOVE __INITS__ FROM SUBMODULES AS IT COULD BREAK DOCS.

sphinx-apidoc -o sources/ ../gbvision
make clean html

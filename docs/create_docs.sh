#DONT REMOVE __INITS__ FROM SUBMODULES AS IT COULD BREAK DOCS.

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"/docs || (mkdir "$PROJECT_ROOT"/docs/ && (cd "$PROJECT_ROOT"/docs || exit 1))
sphinx-apidoc -o sources/ "$PROJECT_ROOT"/gbvision
make clean html

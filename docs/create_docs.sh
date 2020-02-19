#DONT REMOVE __INITS__ FROM SUBMODULES AS IT COULD BREAK DOCS.

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"/docs || (mkdir "$PROJECT_ROOT"/docs/ && (cd "$PROJECT_ROOT"/docs || exit 1))
rm source/*.rst
cp "$PROJECT_ROOT"/docs/cache/index.rst "$PROJECT_ROOT"/docs/source/index.rst
if [ -n "$(command -v py)" ]; then
  alias py=py
else
  alias py=python3
fi
if [ -n "$(command -v sphinx-apidoc)" ]; then
  sphinx-apidoc -o source/ "$PROJECT_ROOT"/gbvision || exit 1
else
  py -m sphinx -o source/ "$PROJECT_ROOT"/gbvision || exit 1
fi
exit 0

#DONT REMOVE __INITS__ FROM SUBMODULES AS IT COULD BREAK DOCS.

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"/docs || (mkdir "$PROJECT_ROOT"/docs/ && (cd "$PROJECT_ROOT"/docs || exit 1))
rm source/*.rst
if [ -n "$(command -v py)" ]; then
  alias py=py
else
  alias py=python3
fi
if [ -n "$(command -v sphinx-apidoc)" ]; then
  alias sphinx=sphinx-apidoc
else
  alias sphinx="py -m sphinx"
fi
sphinx -o source/ "$PROJECT_ROOT"/gbvision || exit 1
exit 0

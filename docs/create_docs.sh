#DONT REMOVE __INITS__ FROM SUBMODULES AS IT COULD BREAK DOCS.

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"/docs || (mkdir "$PROJECT_ROOT"/docs/ && (cd "$PROJECT_ROOT"/docs || exit 1))
sphinx-apidoc -o sources/ "$PROJECT_ROOT"/gbvision || exit 1
if [ -n "$(command -v make)" ]; then
  make clean html || exit 1
else
  cmd "/C make.bat clean html" || exit 1
fi
exit 0
# ln -s -f ../../deploy/pre-commit.sh .git/hooks/pre-commit
poetry run isort -c . && \
poetry run flake8 --config=$PWD/linting.ini . && \
poetry run mypy --config-file=$PWD/linting.ini .

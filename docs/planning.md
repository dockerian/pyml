# Project Planning

> Agile stories for the project.

<br/><a name="contents"></a>
## Contents

* [Stories](#stories)


<br/><a name="stories"></a>
## Stories

### Story: Create a Python3 project

  * Estimate: 3d
  * Acceptance Criteria:
    - Language: Python
    - Initialize with `.gitignore`, GPL LICENSE and README.md
    - Should have `.dockerignore`, `.gitattributes`, and `.pylintrc`
    - Should have Dockerfile
    - Should have Makefile with targets:
      `clean`, `clean-all`, `docker`, `test`, `test-all`
    - Should have `setup.cfg`, and `setup.py`
    - Should have a "docs" folder
    - Should have a project folder, e.g. "`ml`"
    - Should have a library folder, e.g. "`ml/utils`"
    - Should include necessary tools in `tools` folder
    - Should have `ml/config.py`, `ml/logging.yaml`, `ml/utils/logger*.py` with unit tests
    - Should run `pytest` with linter, flake8, and pep8 to generate coverage report
    - Should run all tests in python venv (virtual env)
    - Should have travis ci integrated

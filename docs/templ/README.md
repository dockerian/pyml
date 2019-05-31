# Build a New Python Project

> How to initialize a new python project with venv, CI, and test coverage.
>
> Note:
> - Based on general practice, the process may not be the best solution.
> - Limited support to Python playbook, environment, IDE, CI, and frameworks.
> - A code generator is available [here](../../tools/make_newpy.sh).


<br/><a name="contents"></a>
## Contents

* [Directory](#tree)
* [Python project creator](#creator)
* [Config and Logging](#config-and-logging)
* [Testing framework](#testing)
* [Github Badges](#badges)
* [Travis CI](#travis-ci)


<br/><a name="tree"></a>
## Directory

  The project directory structure can be initialized as the following:

  ```
  /
  ├── .dockerignore
  ├── .pylintrc
  ├── Dockerfile
  ├── docs
  │   └── templ
  │       ├── README.md             # this documentation
  │       ├── _*.templ              # all templates here with
  │       ├── ...                   # prefix `_` and `.templ` extension
  │       └── _setup.py.templ
  ├── LICENSE
  ├── Makefile                      # repository root Makefile
  ├── README.md
  │
  ├── {{__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__}}
  │   ├── __init__.py
  │   ├── api                       # api service
  │   ├── common                    # common/shared library
  │   │   └── __init__.py
  │   ├── utils                     # utilities library
  │   │   ├── __init__.py
  │   │   ├── extension.py
  │   │   ├── logger_formatter.py
  │   │   └── logger.py
  │   │
  │   ├── Makefile                  # project-level Makefile
  │   ├── README.md
  │   ├── app.py                    # api service entry point
  │   ├── config.py                 # config module
  │   ├── config.yaml
  │   ├── logging.conf              # logging config
  │   ├── logging.yaml
  │   ├── main.py                   # main entrance
  │   ├── requirements-dev.txt
  │   ├── requirements.txt
  │   └── ...
  ├── setup.cfg
  ├── setup.py
  │
  ├── tests
  │   ├── test_config.py
  │   ├── test_utils_extension.py
  │   ├── test_utils_get_hash.json
  │   └── test_utils_logger.py
  └── tools
      ├── make_venv.sh
      └── run.sh
  ```


<br/><a name="creator"></a>
## Python project creator

  Based on a full [CI](https://en.wikipedia.org/wiki/Continuous_integration)-integrated
  Python[3](https://www.python.org/) project [template](./templ), the bash
  script [`tools/make_newpy.sh`](../../tools/make_newpy.sh) provides a code
  generator in CLI mode to allow developer creating a new Python project with
  pre-built `Dockerfile`, `Makefile`, `setup.py`, `config`, `logger`,
  as well as linter, pep8, flake8, etc., and testing frameworks.

  The `make_newpy.sh` supports a couple handy command line argument options:

  `--help` - print usage

  `--install` - add a link to system path (e.g. `/user/local/bin`):

  ```
  tools/make_newpy.sh --install /usr/local/bin/make_newpy  # default to `newpy`
  ```

  `--uninstall` - remove installed link:

  ```
  make_newpy --uninstall  # optional $2 to provide the link
  ```


<br/><a name="config-and-logging"></a>
## Config and Logging

  Here is the instructions on how to use the template manually.

  * At the repository root, choose and create a project folder, which could be
    the same as or an alias of the repository name. This would also be the top
    python module (`{{__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__}}`).
  * Add `requirements.txt` (including dependencies for production only)
    and `requirements-dev.txt` (dependencies for dev and testing).
    See example in [docs/templ](../../docs/templ/example).
  * For `Makefile`, `README.md`, and `setup.py`, find templates in `docs/templ/example`
    folder and replace any (`{{__PLACE_HOLDER__}}`) with proper text.
  * Add `setup.cfg` (and set test coverage threshold)
  * Add `utils/logging*.py`, `logging.conf` and `logging.yaml` to the project
    folder and replace any (`{{__PLACE_HOLDER__}}`) with proper text.
  * Add `config.py` with `tests/test_config.py`
  * Add `.dockerignore`, `.gitattributes`, `.gitignore`, and `.pylintrc`
  * Fix import names

  **Note**:
  * Use [regex](https://regex101.com/) ([regular expression](https://regexr.com/)) `\{\{__[A-Z_]+?__\}\}` to find all place holders.
  * Use `{{__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__}}` with "`.`",
    e.g. `ml\.` (regex) to find imports in all python files (`*.py`).
  * Docker container may not need to run with python venv:
    - uncomment lines after `# Don't need venv insider docker` in Makefile
    - uncomment lines of `pip install -r requirements*.txt` in Dockerfile



<br/><a name="testing"></a>
## Testing Frameworks

  This project is designed to use either Python 3 (by default, `USE_PYTHON3=1`)
  or Python 2.7 (`USE_PYTHON3=false`), with venv (virtual env) on a docker host
  or inside docker container (existing `/.dockerenv`).

  All the following testing frameworks are supported thru `Makefile` scripts:
  * [nose2](https://nose2.readthedocs.io/en/latest/index.html)

    ```
    make nosetest  # or `nose2`
    ```

  * [pytest](https://docs.pytest.org/en/latest/)

    ```
    make pytest    # or `pytest`
    ```

  * [unittest](https://docs.python.org/3/library/unittest.html)

    ```
    make unittest  # or `python -m unittest discover`
    ```

  Also support to use `setup.py`:

  * [tox](http://tox.readthedocs.org/en/latest/examples.html)
    - see `docs/templ/example/.tox.ini.templ`.

  * [setup.py](https://docs.python.org/3/distutils/setupscript.html)

    ```
    python setup.py test
    ```

  See
  * https://docs.python-guide.org/writing/tests/
  * https://www.fullstackpython.com/unit-testing.html
  * https://wiki.python.org/moin/PythonTestingToolsTaxonomy


<br/><a name="badges"></a>
## Github Badges

  * [Shields.io badges builder](https://shields.io/#/)
  * [Markdown code for Github badges](https://github.com/Naereen/badges)
  * [Badges as a service](https://github.com/badges)
  * Other links
    - https://github.com/dwyl/repo-badges
    - https://medium.freecodecamp.org/how-to-use-badges-to-stop-feeling-like-a-noob-d4e6600d37d2
    - https://nitratine.net/blog/post/github-badges/
    - http://thomas-cokelaer.info/blog/2014/08/1013/
    - https://pypi.org/project/coverage-badge/


<br/><a name="travis-ci"></a>
## Travis CI

  * Install `codecov`

    ```
    python3 -m pip install codecov
    ```
  * Sign in http://codecov.io/ with Github account.
  * Add repository to codecov.io and get a token for specific repository.
  * Add a [travis-ci](https://docs.travis-ci.com/user/languages/python/)
    config file "`.travis.yml`" at repository root:

    ```
    language: python
    python:
      - {{__PYTHON_VERSION__}}
    install:
      - make dev-setup
    script:
      - make test
    after_success:
      - export CODECOV_TOKEN={{__CODECOV_TOKEN__}}
      - bash <(curl -s https://codecov.io/bash) -t {{__CODECOV_TOKEN__}}
    ```
  * Another [example](http://thomas-cokelaer.info/blog/2014/08/1013/):

    ```
    language: python
    python:
      - "3.3"
      - "2.7"
      - "2.6"
    before_install:
      - "export DISPLAY=:99.0"
      - "sh -e /etc/init.d/xvfb start"
    # command to install dependencies
    # e.g. pip install -r requirements.txt --use-mirrors
    install:
      - pip install
      - pip install nose coverage
      - pip install coveralls
    # command to run tests, e.g. python setup.py test
    script:
      - python setup.py nosetests --with-coverage --cover-package pypiview
    after_sucess:
      - coveralls
    ```

  See also
  - https://github.com/codecov/codecov-python
  - https://realpython.com/python-continuous-integration/
  - https://docs.travis-ci.com/user/languages/python/
  - https://docs.codecov.io/docs




<div><br/>
&raquo; Back to <a href="#contents">Contents</a> | <a href="../README.md">Home</a> &laquo;
<a href="https://github.com/dockerian" style="text-decoration:none;"><img src="https://avatars3.githubusercontent.com/u/22064108?s=400&v=4" style="border:0;height:50;width:50px;vertical-align:middle" height="50" alt="Dockerian" border="0" title="Dockerian" align="right" valign="middle" /></a>
</div>

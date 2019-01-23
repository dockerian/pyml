# PyML

> Python Machine Learning Practice

[![Code Coverage](https://codecov.io/gh/dockerian/pyml/branch/master/graph/badge.svg)](https://codecov.io/gh/dockerian/pyml)
[![Build Status](https://travis-ci.org/dockerian/pyml.svg?branch=master)](https://travis-ci.org/dockerian/pyml)


<br/><a name="contents"></a>
## Contents

* [Design](ml/README.md)
* [Dev Setup](#dev-setup)
* [Testing](#testing)



<br/><a name="dev-setup"></a>
## Dev Setup

  Running a `dev-setup` script to install the project and libraries.

  ```
  make clean dev-setup  # this will create a python virtualenv
  ```



<br/><a name="testing"></a>
## Testing

  After running `make dev-setup`, the project and libraries are installed (in python virtual environment). Now it is able to run tests.

  ```
  make test  # also available to run `make unittest` or `make nosetest`
  ```
  or to start a clean test (highly recommended before committing changes) -

  ```
  make clean test-all
  ```
  and open test coverage report

  ```
  make show  # must be on docker host
  ```


<p><br/></p>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Contributors](https://img.shields.io/github/contributors/dockerian/pyml.svg)](https://github.com/dockerian/pyml/graphs/contributors)
[![Code Coverage](https://codecov.io/gh/dockerian/pyml/branch/master/graph/badge.svg)](https://codecov.io/gh/dockerian/pyml)
[![Build Status](https://travis-ci.org/dockerian/pyml.svg?branch=master)](https://travis-ci.org/dockerian/pyml)

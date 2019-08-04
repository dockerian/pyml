# BDD Cucumber Guide

> Software Development Guide for Cumcumber BDD Testing


## Contents

  * [Cucumber Overview](#bdd-overview)
    * [Installation](#bdd-install)
    * [Workflow](#bdd-workflow)
  * [Features and Steps](#features-and-steps)
    * [Features](#features)
      - Overview
      - Scenario Outline
      - Input Data Table
    * [Steps](#steps)
      - Overview
      - Scenario Outline
      - Input Data Table
  * [Cucumber in a Python project](#cucumber-in-project)
    * [Overview](#cucumber-overview)
    * [Cucumber Tests](#cucumber-tests)
    * [Known Issues](#known-issues)
  * [References](#references)


**Author(s)**

  |Name        |Email            |
  |:-----------|:----------------|
  |Harrison Lee|leeh@infoblox.com|

**Revision History**

  |Revision|Date      |Description   |
  |:-------|:---------|:-------------|
  |0.1     |07/01/2019|Initial Draft |


<br/><a name="bdd-overview"></a>
## BDD Cucumber Overview

  To begin, [Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development) (TDD) is a development process where tests are written before the functional code. This turns code into an instruction manual for itself. Initially, the tests fail and the developer writes the minimum amount of code to pass and finally refactors the new code to acceptable standards.

  Similar to TDD, [Behavior Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development) (BDD) is a testing process that takes a collaborative approach to software development and attempts to bridge the communication gap between business and engineers. Specifically, [Cucumber](https://en.wikipedia.org/wiki/Cucumber_(software)) is a BDD Framework that is centered around the idea of using its plain language parser called [Gherkin](https://docs.behat.org/en/v2.5/guides/1.gherkin.html). Gherkin allows expected software behaviors to be specified in a logical cause-and-effect language non-engineers can better interpret.

  When comparing TDD to BDD, both share similarities in the development process by starting with tests. The difference is that TDD is more focused on function interfaces. Where as BDD does not mind the input/output of each individual function as long as the result of process is correct under the `GIVEN` conditions (likely from acceptance criteria of an Agile story).

  Furthermore, this guide will assume `Python3(>=3.7.3)` as a software engineer’s expected programming language.

<a id="bdd-install"></a>
### Installation

  Getting started in Python3 to use [Cucumber](https://www.guru99.com/introduction-to-cucumber.html), `behave` (>=1.2.6) will be required.

  * Recommended to have `behave` library in the requirements file.

  In order to install `behave`, open terminal, activate `venv` and execute

  ```
  (.venv)
  $ pip install behave
  ```

  The `behave` command requires all dependencies to be installed within the same virtual environment it exists in. To update an already installed behave, use

  ```
  (.venv)
  $ pip install -U behave
  ```


<a id="bdd-workflow"></a>
### Workflow

  1. First, in the desired directory where the tests reside, create a directory called `features`.
  2. Within the `features` directory, create a new directory called `steps`. Capitalizations and spelling is very important so please double check.
  3. The `features` directory is where the `.feature` files will live, which are similar to user stories and written in Gherkin.
  4. Lastly, within the `steps` directory is where the Python3 files to test the `feature` files will live. More will be explained about the `feature` and `step` files [later](#features).

  Example of a working environment below.

  ```
  .
  └── features
      ├── some_features.feature
      └── steps
          └── some_steps.py

  ```

  To use behave, navigate to the directory that the `features` directory lives in and in terminal execute...

  ```
  (.venv)
  $ behave
  ```

  This is optional, but it is also possible to create a `behave.ini` which is a configuration file for `behave`. An advantage of this configuration file is that the `paths` keyword makes it possible to define the location of the `features` directory making it more flexible. This allows `behave` to be called outside of the `features` directory as long as the `paths` is set to where the features directory is.

  An example of a working environment with the `behave.ini` file is shown below.

  ```
  (base)
  ├── tests
  │   └── features
  │       ├── some_features.feature
  │       └── steps
  │           └── some_steps.py
  └── behave.ini

  ```

  An example of the `behave.ini` configuration file below.

  ```
  [behave]
  paths = tests/features
  ```

  Another advantage of this configuration file is that, `behave` by default does not capture `stdout`, so it is not possible to print and see the behavior of the tests (different from test results which are displayed, writing explicit print statements will not be shown). Therefore using some command-line arguments in the configuration file, it is possible to tune `behave` to capture output. More information about the command-line arguments can be found on the `behave` [documentation page](https://behave.readthedocs.io/en/latest/behave.html).

  An example of the `behave.ini` configuration file to capture output below.

  ```
  [behave]
  paths = tests/features
  stdout_capture = true
  stderr_capture = false
  log_capture = false
  ```


  <a id="aws-setup"></a>
  Also it is important to have a runtime environment (e.g. AWS setup as and external dependency for the tests when Cucumber serves as functional testing framework). Here is an example of setting AWS environment:

  1. Install [AWS Command Line Interface](https://aws.amazon.com/cli/) by executing...

  ```
  pip install awscli
  ```

  2. Sign in to the AWS Management Console at  https://console.aws.amazon.com/iam/.
  3. On the navigation pane, choose `Users`.
  4. Choose the name of the user whose access keys are to be created and then choose `Security credentials` tab.
  5. In the `Access keys` section, choose `Create access key`.
  6. To view the new access key pair, choose `Show`. There will not be access to the secret access to the secret access key after the dialog box closes.
  7. Download the key pair and choose `Download .csv file`. Store the keys in a secure location.
  8. After the .csv file is downlaoded, choose `Close`. The key pair should be active by default and the key pair can be used right away.
  9. Open terminal and execute...

  ```
  aws configure
  ```

  10. Fill in the necessary fields using the key access pair and necessary credentials.

  An example of `aws configure` below.

  ```
  AWS Access Key ID [None]: ABCDEFGHIJKLMNOPQRST
  AWS Secret Access Key [None]: abCdEfGhiJKLM/KlMnOpQ/rStUvWxYz012345678
  Default region name [None]: us-east-1
  Default output format [None]: json
  ```


<br/><a name="features-and-steps"></a>
## Features and Steps

<a id="features"></a>
### Features

#### _Overview_

  `Feature` files are files written in Gherkin that define a `feature` and `scenario` to be tested. These files are also found within the `features` directory and can be called anything as long as file has the `.feature` extension. The main components of a `feature` file requires a defined `given`, `when`, and `then`, which are also referred to as `steps`. This reflects the idea of cause-and-effect.

  `Feature` file example below.

  ```
  Feature: When should a ninja fight

  Scenario: Stronger Opponent
      Given the ninja has a third level black-belt
      When attacked by Chuck Norris
      Then the ninja should run for his life

  ```

  * The `Feature` should be a broad overview of what is being tested
  * The `Scenario` should be the case(s) to test
  * `Given` is what is being given to the test
  * `When` is a specific condition for the test
  * `Then` is the result, so how the function behaved, given a condition when another condition is set

  Important to note there are `And` and `But` keywords, which act as conditions after `steps`.

  An example of the `And` and `But` keyword below.

  ```
  Given the integer 1
  And the string "Hello"
  When both are concatenated
  Then the outcome is "Hello1"
  But the outcome is not an integer

  ```

#### _Scenario Outline_

  Scenarios can test a defined `given`, but when wanting to test multiple `given` variables it is suggested to use a `Scenario Outline`. `Scenario Outlines` are `Scenarios` that can take variables defined by the developer.

  Scenario Outline example below.

  ```
  Scenario Outline: Blenders
    Given I put <thing> in a blender,
    When I switch the blender on
    Then it should transform into <other thing>

  Examples: Amphibians # Name for the table, not required
    | thing   | other thing |
    | frog    | mush        |

  ```

  * In this particular example, we can notice `thing` being an input and `other thing` being the expected output, which is the idea of cause and effect once again.
  * In Gherkin, the | symbol denotes a data table. Therefore, after defining Examples: (name of data table), the header of the data table is used to match variable names (spelling and capitalization must be the exact same) and the values below the headers are passed as parameters to function calls.

#### _Input Data Table_

  Furthermore, it is possible to include a table of data.
  Input Data Table example below.

  ```
  Scenario: some scenario
    Given a set of specific users
      | name      | department  |
      | Pudey     | Silly Walks |
      | Two-Lumps | Silly Walks |

    When we count the number of people in each department
    Then we will find two people in "Silly Walks"  

  ```

  * This has useful applications which can be better explained and demonstrated in the `steps` portion of this guide.


<a id="steps"></a>
### Steps

#### _Overview_

  `Step` files do the tests defined in the `features` and `scenarios` found in the `feature` files. `Step` files are found within the `steps` directory which is located within the `features` directory and can be called anything as long as the files have the .py extension.

  * An important part of the `steps` file is to make sure the functions that are to be tested are imported from the necessary files. Also that `given`, `when`, and `then` are imported from `behave` as well.

  The `step` files rely on hooks. This means is that annotation is very important. Standalone `step` files are hard to explain without `feature` files because both files go together.

  This is an example of a `feature` and `step` file together below.

  ```
  ## features/some.feature
  Feature: showing off behave

    Scenario: run a simple test
      Given we have behave installed
      When we implement a test
      Then behave will test it for us!

  ## features/steps/some_steps.py
  from behave import given, when, then

  @given('we have behave installed')
  def step_impl(context):
    pass

  @when('we implement a test')
  def step_impl(context):
  assert True is not False  

  @then('behave will test it for us')
  def step_impl(context):
    assert context.failed is False
  ```

  * Notice how the annotation for each `step` in the `step` file, the `given`, `when`, and `then` match the `feature` file exactly. This is very important as `behave` relies on hooks in the `step` file to match each `feature` `step` to. Capitalization and spelling must be precise.
  * A `Context` object is also given by default as a way to store information.
  * Usually `given` is a good place to initialize variables or states that will be necessary for testing, then using `when` to call the function that is being tested, and finally using `then` to assert and check if the result is intended (or unintended).

#### _Scenario Outline_

  Here is another example of the `steps` file, except the `feature` file using variable input with a data table…

  ```
  ## features/dealer.features
  Scenario Outline: Get hand total
    Given a <hand>
    When the dealer sums the cards
    Then the <total> is correct

    Examples: Hands # Name for the table not required
    | hand  | total |
    | 5,7   | 12    |
    | 5,Q   | 15    |
    | Q,Q,A | 21    |
    | Q,A   | 21    |
    | A,A,A | 13    |

  ## features/steps/steps.py
  @given('a {hand}')
  def step_impl(context, hand):
    context.dealer = Dealer()
    context.dealer.hand = hand.split(',')

  @when('the dealer sums the cards')
  def step_impl(context):
    context.dealer_total = context.dealer.get_hand_total()

  @then('the {total:d} is correct')
  def step_impl(context, total):
    assert (context.dealer_total == total)

  ```

  * Notice how the annotation of the `steps` still match the `feature scenario` with variable input.
  * Also notice how in the actual `step` functions the variable is passed as a parameter.

#### _Input Data Table_

  Finally, an example of how a `step` function uses a data table as input from the `feature` file…

  ```
  ## features/user.feature
  Scenario: some scenario
    Given a set of specific users
      | name      | department  |
      | Pudey     | Silly Walks |
      | Two-Lumps | Silly Walks |

    When we count the number of people in each department
    Then we will find two people in "Silly Walks"

  ## features/steps/user_steps.py
  @given ('a set of specific users')
  def step_impl(context):
    for row in context.table:
      model.add_user(name=row['name'],
            department=row['department'])

  ```

  * The columns of the data table can be selected by calling the column header. This is similar to the Python Pandas library with the dataframes.


<br/><a name="cucumber-in-project"></a>
## Cucumber in Python project

<a id="cucumber-overview"></a>
### Overview

  This is an experimentation of Cucumber to see how it would work on an existing project. Make sure that [AWS is setup](#aws-setup), `behave` is installed in the virtual environment with all dependencies, and have Python3 (Version 3.7.3).

  Work enviornment example below.

  ```
  .
  └── project
      ├── tests
      │   └── features
      │       └── steps
      └── <top_module_name>
          └── process
              └── module.py

  ```

  Some files and directories not included.

  ```
  PYTHONPATH=. behave tests/features
  ```

  In the Makefile, there is a command to run this line and can be run:

  ```
  make bdd
  ```

  This will activate the virtual environment which includes `behave` and all its dependencies then deactivate after the test.


<a id="cucumber-tests"></a>
### Cucumber Tests

  _TBD_


<a id="known-issues"></a>
### Known Issues

  When using `behave` and there are directory issues. A possible solution is to navigate to the root directory and execute the line below with the file path to the `features` directory.

  ```
  PYTHONPATH=. behave */features
  ```
  or

  ```
  PYTHONPATH=. behave tests/features
  ```


<br/><a name="references"></a>
## References

  * 10 Minute [Cucumber tutorial](https://cucumber.io/docs/guides/10-minute-tutorial/) in Java, JS, Ruby, and Kotlin

  * Behave tutorial from the official [Behave documentation](https://behave.readthedocs.io/en/latest/tutorial.html)

  * Behave [tutorial](https://semaphoreci.com/community/tutorials/getting-started-with-behavior-testing-in-python-with-behave), starting from scratch to make a game of twenty-one

  * Comparing the pros and cons of [different BDD’s](https://dzone.com/articles/brief-comparison-bdd)

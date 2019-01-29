# Project Planning



> Agile stories for the project.

<br/><a name="contents"></a>
## Contents

* [Project Initiation](#epic-init)
* Digit Recognizer
  * [Trainning Epic](#epic-drt)
  * [Preiction Epic](#epic-drp)



<br/><a name="epic-init"></a>
## Project Initiation

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


<br/><a name="epic-drt"></a>
## Digit-recognizer Trainning Epic

> This epic is to create a digit recognizer that can classifiy hand written digits. The project is to use deep learning algorithms to train an model and to predict digits in training set.

### Story: Collect and modify data set

* Estimation: 1d
* Acceptance criteria:
  - Data should be downloaded from Kaggle digit recognizer competetion to datasets folder
  - Data set should be in the form of a matrix as each collumn being each image, and each row being each pixel. load label set in a 1:m matrix
  - Should create functions: load_data, load_dataset in digit-recognizer/dataSvc.py
  - Should nomalize data sets

### Story: Create math extensions

* Estimation: 2d
* Acceptance criteria:
  - Should be common/mathEx.py
  - Should include basic activation functions: relu, leaky_relu, and sigmoid, with the backward version of them
  - Should include functions of forward and backward activation: l_model_forward, l_model_backward_with_l2, linear_activation_backward_with_l2, linear_activation_forward, linear_backward_with_l2, linear_forward,
  - Should include function: compute_cost
  - Should include initialiation function with "He initialization": initialize_parameters_deep_he
  - Should include function: change_to_multi_class
  - Should include function for gradient descent: update_parameters

### Story: build deep training model

* Estimation: 1d
* Acceptance criteria:
  - Should needed load data from files to normalized training set
  - Should define hyper-parameters: Layer dementsions, learning rate alpha, regularization parameter lambda, number of iterations
  - Should be able to print costs
  - Should go through forward and backward propagation in each iteration
  - Should save parameters to numpy file after training


<br/><a name="epic-drp"></a>
## Digit-recognizer Prediction Epic

### Story: Predict on certain set

* Estimation: 1d
* Acceptance criteria:
  - Should load datas from files to noramlized traning set and test set
  - Should load parameters from numpy files
  - Should go through one iteration of forward propagation
  - Should calculate and print accuracy

## Recognizer Epic

### Story: Predict on certain hand written image

* Estimation: 1d
* Acceptance criteria:
  - Should load jpg images from files to normalized vectors
  - Should tell the recognizer if the image is white based or black based
  - Should go through one iteration of forward iteration
  - Should print loaded image to system
  - Should print predicted answer and actual answer to system


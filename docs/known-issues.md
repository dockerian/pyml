# Known Issues

> Troubleshooting notes in use of this project.

<br/><a name="contents"></a>
## Contents

  * [ImportError](#import-error)



<br/><a name="import-error"></a>
## ImportError

  * Error ([example](https://github.com/openai/spinningup/issues/1))

    ```
    ImportError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information.
    ```
  * Fix options ([see](https://github.com/scikit-optimize/scikit-optimize/issues/637))
    - re-install or remove [Conda](https://docs.conda.io/en/latest/) (package, dependency and environment management)

      ```
      conda install matplotlib
      # or
      conda install anaconda-clean
      anaconda-clean --yes
      ```
    -  force `matplotlib` to use TCL/TK and reinstalling python with tcl. This solved the problem both when running in a virtual env and in the native python environment.

      ```
      echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
      brew uninstall python3
      brew install python3 --with-tcl-tk
      ```
  * Recommendation
    - don't usually have `matplotlib` as a direct dependency:
      it is very platform dependent and it is usually not essential for what these libraries are trying to accomplish.
    - install the libraries as part of an extra, i.e. `pip install skopt[plotting]`

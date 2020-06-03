# Digital islands

> Using a boolean 2D matrix to represent islands. Any connected "\*"s form an island. For example:

  ```python
  matrix = [
    [*, *, _, _, _, *, _],
    [_, *, *, _, _, _, _],
    [_, _, _, _, *, _, _],
    [_, _, *, _, _, _, *],
    [*, _, *, *, _, _, *],
    [_, *, *, _, _, _, _],
    [_, _, _, _, _, _, _],
    [_, _, *, _, *, *, *],
  ]
  ```
> Above has 6 islands, and the largest island size is 7.

> See https://repl.it/@jason_zhuyx/digiIslands

The `DigiIslands` class scans an input matrix and builds a list of island slices, with visited history info, to achieve `O(2*n)` in space and `O(n)` for runtime execution, where "`n`" is number of items of the input matrix.

```python
from ml.digiIslands.di import DigiIslands
from tests.constant import DATA

import ml.common.extension as utils


def main():
    """
    The main routine.
    """
    # import sys
    # print('command args', sys.argv)
    # return sys.argv
    data = DATA[3]
    print("- input matrix: {}".format(utils.str_matrix(data)))
    grid = DigiIslands(data)
    grid.print_islands()


if __name__ == "__main__":
    import os
    os.system('python3 -m unittest -v tests/test_di.py')
    # run_all()
    main()
```

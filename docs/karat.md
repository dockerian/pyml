# Karat Questions

> Collection of Karat interview process and questions


## Content

* [Karat Technical Categories](#categories)
* [Karat Coding Questions](#coding)


<br /><a name="categories"></a>
## Karat Tech Categories

* General Programming
  - Fundamental concepts underlying the design of well-structured code.
  - Questions
    * What software principle to solve complexity of models?
    * Why in favor of composition than inheritance?

* Web / API Concepts
  - Interactions between web servers and clients.
  - Questions
    * What is the same-origin policy with respect to browser-based JavaScript behavior?
      How can it be overcome, for example when an API is hosted on a separate domain?

    * Versioning of REST APIs becominges critical in the real -world.
      How would you implement versioning of a REST API and why do you believe it is the best method?

    * How does a browser get a cookie from a website?
      How does the website get the cookie from the browser?

* Networking and Security
  - Safe remote interactions between multiple systems.

* Databases
  - Design of complex data storage systems.

* Performance
  - Identifying and troubleshooting issues with real services.

* Testing
  * What is race condition and how it happens?


<br /><a name="coding"></a>
## Karat Coding

### Connect-Four Board State Checker

  The program or function must take in a Connect 4 board and return true if the board is valid and false if it is not. It is okay to assume whatever board representation you like (e.g. Array of Arrays).

  The Rules For Connect 4:
  * Players R and Y take in turns to drop tiles of their colour into columns of a 7x6 grid. When a player drops a tile into the column, it falls down to occupy the lowest unfilled position in that column. If a player manages to get a horizontal, vertical or diagonal run of four tiles of their colour on the board, then they win and the game ends immediately.

  For example (with R starting), the following are an impossible Connect 4 position.

  ```
  | | | | | | | |
  | | | | | | | |
  | | | | | | | |
  | | |R| | | | |
  | | |Y| | | | |
  |R| |Y| | | | |

  | | | | | | | |
  | | | | | | | |
  | | | | | | | |
  | | | | | | | |
  | |Y|Y|Y|Y| | |
  | |R|R|R|R| | |
  ```
  And some possible states:

  ```
  | | | | | | | |
  | | | | | | | |
  | | | | | | | |
  | | |R| | | | |
  | | |Y| | | | |
  |R|R|Y| | | | |

  | | | | | | | |
  | | |Y| | | | |
  | | |R| | | | |
  | | |Y| | | | |
  | | |R| | | | |
  | |Y|R| | | | |
  ```

### Schedule ranges

  Imagine that you're at a large company, and you're tasked with analyzing schedules to see when we've overbooked our schedule.

  Each Worker object contains information about a person's shift. This data includes:
    1. name
    2. startTime (as an integer, 0 to 23 inclusive)
    3. endTime (as an integer, 0 to 23 inclusive)

  Problem: Given a list of Worker objects, find the list of ranges that has the most workers booked

  ```python
  """
  For works as the following -
    name    startTime   endTime
    A         1           3
    B         4           7
    C         2           6

    ----|----|----|----|----|----|----|---- time
        1    2    3    4    5    6    7

        |< ---A-->|
                       |<-----B------>|
             |<--------C-------->|
  """
  class Worker:
      def __init__(self, name, startTime, endTime):
          self.name = name
          self.startTime = startTime
          self.endTime = endTime

  def getMostBookedRanges(workers: list) -> list:
      times = [0 for x in range(24)]
      for w in workers:
          for h in range(w.startTime, w.endTime):
              times[h] += 1
      ranges = []
      prev_count, start = -1, -1
      max_count = max(times)
      # print(max_count, times)
      for h, count in enumerate(times):
          if count != prev_count:
              if prev_count == max_count:
                  ranges.append((start, h))
              prev_count = count
              start = h
      return ranges

  ranges = getMostBookedRanges(workers)
  # expecting [(2, 3), (4, 6)]
  ```

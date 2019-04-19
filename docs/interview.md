# Interview Questions

> Collective interview questions on data structure and algorithms

## Contents
  * [Data Structure](#ds)
    - [Array/List](#ds-array)
    - [Linked List](#ds-linkedlist)
    - [Queue and Stack](#ds-queue-and-stack)
    - [Tree and Trie](#ds-tree)
    - [Graph](#ds-graph)
  * [Design questions](#design)
  * [Mathematics problems](#math)
  * [Sorting Algorithms](#sorting)
    - [Big O Notation](#sorting-big-o)
    - [Bubble sort](#sorting-bubblesort)
    - [Insertion sort](#sorting-insertionsort)
    - [Merge sort](#sorting-mergesort)
    - [Quick sort](#sorting-quicksort)
  * [Quiz, IQ, and Brain Teaser](#quiz)
  * [Testing](#testing)
  * [Networking](#networking)
  * [Non-technical](#non-tech)
  * [Reading](#reading)


<br/><a name="ds"></a>
## Data Structure

<a name="ds-array"></a>
### Array/List

  * Check if two strings are anagrams of each other.
  * Check if a string or a sentence is palindrome char by char, or word by word.
  * Check if one string contains all characters in another string.
  * Find all permutations of a String.
  * Find the duplicate number in a given integer list.
  * Find the largest and smallest in a given unsorted integer list.
  * Find the missing number in a given unsorted integer list, e.g. from 1~100.
  * Find all pairs, in an integer list, whose sum is equal to a given number.
  * Reverse order of words in a sentence.

<a name="ds-linkedlist"></a>
### Linked List

  * Find the middle element in a singly linked list (in one pass).
  * Check if a linked list contains a cycle. Find the starting node of the cycle.
  * Reverse a linked list.

<a name="ds-queue-and-stack"></a>
### Queue and Stack

  * How to implement a queue using a stack?
  * Implement a `quick_sort` function without recursion.


<a name="ds-tree"></a>
### Tree and Trie

  * Find if one B-tree contains another B-tree.
  * Perform in-order traversal without recursion.
  * Perform pos-torder traversal without recursion.
  * Perform pre-order traversal in a given binary tree.

<a name="ds-graph"></a>
### Graph

  * Detect a cycle in a graph.



<br/><a name="design"></a>
## Design questions

### OOP

  * Designing a simple card game.
    - How to store the order of all the players (data structures)
    - How to break it up into classes (card, game, player, etc)
    - Create properties/fields and functions/methods.

### Resources:

  * Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four, 1994)
  * Head First Design Patterns (2nd Edition, 2008)

  * The [System Design Primer](https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question)
  * [Scalability for Dummies](http://www.lecloud.net/search/scalability+for+dummies)
  * Design a [Collaborative Editor](http://blog.gainlo.co/index.php/2016/03/22/system-design-interview-question-how-to-design-google-docs/)
  * Design a [URL Shortener](http://blog.gainlo.co/index.php/2016/03/08/system-design-interview-question-create-tinyurl-system/)



<br/><a name="math"></a>
## Mathematics

### Big prime number

  * https://langui.sh/2009/03/07/generating-very-large-primes/
  * https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb

### Resources

  * https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-fall-2010/assignments/



<br/><a name="sorting"></a>
## Sorting

<a name="sorting-big-o"></a>
### Big-O notation

  | Algorithm      | Best     | Average  | Worst    | Space    |
  | -------------- |:--------:|:--------:|:--------:|:--------:|
  | Bubble-sort    | n        | n^2      | n^2      | 1        |
  | Bucket-sort    | n+k      | n+k      | n^2      | n        |
  | Cube-sort      | n        | n log(n) | n log(n) | n        |
  | Heap-sort      | n log(n) | n log(n) | n log(n) | 1        |
  | Insertion-sort | n        | n^2      | n^2      | 1        |
  | Merge-sort     | n log(n) | n log(n) | n log(n) | n        |
  | Quick-sort     | n log(n) | n log(n) | n^2      | log(n)   |
  | Radix-sort     | n\*k     | n\*k     | n\*k     | n+k      |
  | Selection-sort | n^2      | n^2      | n^2      | 1        |
  | Shell-sort     | n log(n) |n log(n)^2|n log(n)^2| 1        |
  | Tree-sort      | n log(n) | n log(n) | n^2      | n        |


<br/><a name="sorting-bubblesort"></a>
### Bubble Sort

  ```python
  def bubble_sort(arr, reversed_order=False):
      x_range = range(len(arr)) if reversed_order else range(len(arr)-1, 0, -1)
      for num in x_range:
          for i in range(num):
              if arr[i] > arr[i+1]:
                  arr[i], arr[i+1] = arr[i+1], arr[i]
  ```

<br/><a name="sorting-insertionsort"></a>
### Insertion Sort

  ```python
  def insertion_sort(arr):
     for ndx in range(1, len(arr)):
       pos = ndx
       val = arr[ndx]
       while pos > 0 and arr[pos-1] > val:
           arr[pos] = arr[pos-1]
           pos = pos-1
       arr[pos] = val
  ```

<br/><a name="sorting-mergesort"></a>
### Selection Sort

  ```python
  def selection_sort(arr):
      x_range = range(len(arr)-1, 0, -1)
      for num in x_range:
          pos = 0
          for ndx in range(1, num+1):
              if arr[ndx] > arr[pos]:
                  pos = ndx
          arr[num], arr[pos] = arr[pos], arr[num]
  ```

<br/><a name="sorting-mergesort"></a>
### Merge Sort

  ```python
  def merge_sort(arr):
      if not isinstance(arr, list) or len(arr) <= 1:
          return
      mid = len(arr) // 2
      hal, har = arr[:mid], arr[mid:]  # copy to new slices

      merge_sort(hal)  # sorting the left half
      merge_sort(har)  # sorting the right half

      i = j = k = 0
      # copy data to new slices `hal` and `har`
      while i < len(hal) and j < len(har):
          if hal[i] < har[j]:
              arr[k], i = hal[i], i+1
          else:
              arr[k], j = har[j], j+1
          k += 1
      # checking if any element was left
      while i < len(hal):
          arr[k], k, i = hal[i], k+1, i+1
      while j < len(har):
          arr[k], k, j = har[j], k+1, j+1
  ```

<br/><a name="sorting-quicksort"></a>
### Quick Sort

  ```python
  def _check_median_pivot(arr, li, hi):
      mi = (li + hi) / 2
      lv, lv_is_num = _get_num(arr[li])
      mv, mv_is_num = _get_num(arr[mi])
      hv, hv_is_num = _get_num(arr[hi])
      if mv_is_num and (not lv_is_num or mv < lv):
          arr[li], arr[mi] = arr[mi], arr[li]
      if hv_is_num and (not lv_is_num or hv < lv):
          arr[li], arr[hi] = arr[hi], arr[li]
      if mv_is_num and (not hv_is_num or mv < hv):
          arr[mi], arr[hi] = arr[hi], arr[mi]

  def _get_num(v):
      try:
          v = float(v)
          v = int(v)
      except Exception:
          pass
      return v, isinstance(v, (int, float))

  def _get_pivot(arr, li, hi, median_pivot=False):
      if median_pivot:
          _check_median_pivot(arr, li, hi)
      si = li  # index of smaller element, starting at lower index
      pivot, pivot_is_number = _get_num(arr[hi])  # initial pivot
      for xi in range(li, hi):
          v, v_is_number = _get_num(arr[xi])
          # moving non-number to higher position
          if v_is_number and (not pivot_is_number or v < pivot):
              arr[si], arr[xi] = arr[xi], arr[si]
              si = si + 1
      arr[si], arr[hi] = arr[hi], arr[si]
      return si

  def quick_sort(arr, li=0, hi=None, level=0):
      if not arr or not isinstance(arr, list):
          return
      sz = len(arr)
      li = li if isinstance(li, int) and 0 <= li and li < sz else 0
      hi = hi if isinstance(hi, int) and 0 <= hi and hi < sz else sz-1
      if li < hi:
          pivot = _get_pivot(arr, li, hi)
          # print('sorting {}, pivot {} from {} to {}'.format(arr, pivot, li, hi))
          quick_sort(arr, li, pivot-1, level+1)
          quick_sort(arr, pivot+1, hi, level+1)
  ```



<br/><a name="quiz"></a>
### Quiz, IQ, and Brain Teaser

  * Calculate the angle at any specific clock time.
  * From 10 boxes of balls, with one box contains 9g balls and other contain 10g balls.
    How to weigh one time and find the 9g-ball box?
  * From 12 identical looking balls, use a simple mechanical balance 3 times,
    how to find the only-one fake ball (which could be lighter or heavier)?
  * Four people, sharing 1 torch, need to cross a bridge can only support maximum 2 persons.
    Each speed at 1m, 2m, 5m, and 8m, can all pass in 15-minute?
  * Only 2 cuts allowed, paying one gold bar to a worker in 7 days (1 week).
  * Use 3 gallon jug and 5 gallon jug, measure out exactly 4 gallons.

  * https://blog.codinghorror.com/classic-computer-science-puzzles/



<br/><a name="testing"></a>
## Software Testing

  Test categories:
  * spec test
    - positive test
    - negative test
  * edge test cases, including out-of-range
  * type check
  * branch check
  * exception check
  * run time error

  Advanced:
  * usability test
     - user interface and UX (user experience) - (consumer) product
     - UI and readability (easy to read/understand)
     - spec/doc, or user manual/guide
  * performance test (load test / stress test)
  * security test: (password exposure, input and logging, wired clear text, data loss, data integrity)
  * risk test
  * localizations: (non-ascii, unicode, different language documentation, user interface)
  * integration
    - installation and setup
    - environment (os system/platform, cloud platform)
    - ad hoc / smoke test / acceptance test / alpha / beta
    - accessibility test, compatibility test
    - work with other services/products



<br/><a name="networking"></a>
## Networking

#### Data Transfer and Latency

  |Computer Event| Speed  | Avg Latency | Normalized Scale |
  |:-------------|-------:|------------:|-----------------:|
  |3 GHz CPU     |        |      0.3 ns |               1s |
  |Cache (L1)    | 3.5GB/s|      0.9 ns |               3s |
  |Cache (L2)    |   3GB/s|      2.8 ns |               9s |
  |Cache (L3)    |        |     12.9 ns |              43s |
  |RAM           |   2GB/s|     ~100 ns |               4m |
  |SSD           | 200MB/s|   25~150 μs |         1~4 days |
  |Hard Drive    | 150MB/s|     1~10 ms |       1~9 months |
  |Internet SF-NYC      ||        65 ms |          5 years |
  |Internet SF-Hong Kong||       141 ms |         11 years |

#### Online network tools

  * http://www.all-nettools.com/toolbox/
  * https://hackertarget.com/ip-tools/
  * https://mxtoolbox.com/NetworkTools.aspx
  * https://www.tamos.com/products/nettools/
  * https://network-tools.com/

#### Downloadable tools

  * https://angryip.org/
  * https://www.wireshark.org/
  * https://nmap.org/
  * https://www.ntop.org/
  * https://www.ssh.com/ssh/putty/mac/ | * http://www.rbrowser.com/ | https://www.emtec.com/zoc/
  * http://pandorafms.org/features/free-download-monitoring-software/
  * https://www.putty.org/

#### Resources

  * https://dev.to/ben/explain-tcp-like-im-five &#9734;&#9734;&#9734;
  * http://bpastudio.csudh.edu/fac/lpress/471/hout/netech/postofficelayers.htm (analogy)
  * http://xahlee.info/linux/computer_networking_index.html &#9733;&#9733;&#9734;&#9734;&#9734;
  * https://www.geeksforgeeks.org/computer-network-tutorials/ &#9733;&#9733;&#9734;&#9734;&#9734;
  * https://www.geeksforgeeks.org/computer-network-tcpip-model/ &#9734;&#9734;&#9734;
  * https://www.garykessler.net/library/tcpip.html &#9733;&#9733;
  * https://edu.gcfglobal.org/en/internetbasics/ &#9734;&#9734;
  * https://www.inetdaemon.com/tutorials/index.shtml &#9733;&#9733;&#9733;
  * https://www.lantronix.com/resources/networking-tutorials/ &#9733;&#9733;&#9734;&#9734;&#9734;
  * http://www.omnisecu.com/tcpip/ &#9733;&#9733;&#9733;
  * https://stackoverflow.com/questions/176264/what-is-the-difference-between-a-uri-a-url-and-a-urn
  * https://en.wikipedia.org/wiki/List_of_information_technology_initialisms (acronyms)
  * https://quizlet.com/113657279/common-networking-acronyms-flash-cards/ (acronyms)
  * http://www.ibexsystems.com/NetworkAcronyms.htm (acronyms)
  * https://nordicapis.com/defining-stateful-vs-stateless-web-services/

#### Free/public APIs

* https://any-api.com (collection)
* https://www.computersciencezone.org/50-most-useful-apis-for-developers (collection for dev)
* https://fakejson.com
* https://github.com/toddmotto/public-apis (collection)
* https://developer.here.com
* https://my-json-server.typicode.com/ (fake API server)
* https://httpstat.us (mocking status code in testing)
* https://rapidapi.com (collection)
* https://reqres.in | https://resttesttest.com | https://api.nasa.gov (AJAX)
* https://swapi.co (The Star Wars)



<br/><a name="non-tech"></a>
### Non-technical

  * [Psychological Tricks](https://github.com/yangshun/tech-interview-handbook/blob/master/non-technical/psychological-tricks.md)
  * [Questions to ask](https://github.com/yangshun/tech-interview-handbook/blob/master/non-technical/questions-to-ask.md)
  * [Negotiation](https://github.com/yangshun/tech-interview-handbook/blob/master/non-technical/negotiation.md)


<br/><a name="reading"></a>
### Reading

* Books/Collection:
  * [Computer Science in JavaScript](https://github.com/humanwhocodes/computer-science-in-javascript)
  * [Mock Interview Generator](https://docs.google.com/spreadsheets/d/1t_228bDllazltWrq7WrLaKCs3dHXlGHBybWz9nnRvSc/edit?usp=sharing)
  * [Tech Interview Handbook](https://github.com/yangshun/tech-interview-handbook)

* Others:
  * https://www.facebook.com/codingpill/
  * https://careersidekick.com/5-things-every-hiring-manager-wants/
  * https://careersidekick.com/brain-teaser-job-interview-questions-facebook-google-apple/
  * http://interactivepython.org/courselib/static/pythonds/index.html
  * https://javarevisited.blogspot.com/2011/06/top-programming-interview-questions.html
  * https://www.geeksforgeeks.org/
  * https://www.geeksforgeeks.org/must-do-coding-questions-for-companies-like-amazon-microsoft-adobe/
  * https://www.geeksforgeeks.org/top-10-algorithms-in-interview-questions/
  * https://medium.freecodecamp.org/the-ultimate-guide-to-preparing-for-the-coding-interview-183251ee36c9
  * https://www.interviewcake.com/google-interview-questions
  * http://overthewire.org/wargames/



<div><br/>
&raquo; Back to <a href="#contents">Contents</a> | <a href="../README.md">Home</a> &laquo;
<a href="https://github.com/dockerian" style="text-decoration:none;"><img src="https://avatars3.githubusercontent.com/u/22064108?s=400&v=4" style="border:0;height:50;width:50px;vertical-align:middle" height="50" alt="Dockerian" border="0" title="Dockerian" align="right" valign="middle" /></a>
</div>

# Interview Questions

> Collective interview questions on data structure and algorithms

## Contents

  * [Languages](#lang)
  * [Data Structure](#ds)
    - [Array/List](#ds-array)
    - [Linked List](#ds-linkedlist)
    - [Queue and Stack](#ds-queue-and-stack)
    - [Tree and Trie](#ds-tree)
    - [Graph](#ds-graph)
  * [Design questions](#design)
    - [OOP](#oop)
    - [System Design](#design-system)
    - [Database](#design-db)
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



<br/><a name="lang"></a>
## Languages

### Error Handling

  * [Deal with exceptions in Python](https://www.pythonforthelab.com/blog/learning-not-to-handle-exceptions/)
  * [Use try/except in Python](https://www.techbeamers.com/use-try-except-python/)

  * Catch all exceptions (NOT recommended)

    ```python
    try:
        do_some_func()
    except BaseException as ex:  # catch *all* exceptions; same as bare `except:`
        # will catch all including `SystemExit`, `KeyboardInterrupt`, or `GeneratorExit`.
        pass  # potential causing to hang
    ```

  * Find out the exception name
    ```python
    try:
        do_some_func()
        raise IndexError # as test error
    except Exception as ex:
        # won't catch `SystemExit`, `KeyboardInterrupt`, or `GeneratorExit`.
        print(type(ex).__name__) # print the name of the exception
    ```

  * Print traceback

    ```python
    import traceback
    try:
        sqrt = 0**-1
    except Exception as ex:
        print(ex)
        print(traceback.print_exc())
    ```

### Multi-threading

  * Mutex vs Semaphores (C/C++)
    - [Part 1: Semapores](https://blog.feabhas.com/2009/09/mutex-vs-semaphores-%e2%80%93-part-1-semaphores/)
    - [Part 2: The Mutex](https://blog.feabhas.com/2009/09/mutex-vs-semaphores-%e2%80%93-part-2-the-mutex/) (MUTual EXclusion)
    - [Part 3: Mutual Exclusion Problems](https://blog.feabhas.com/2009/10/mutex-vs-semaphores-%e2%80%93-part-3-final-part-mutual-exclusion-problems/)

### Code Online

  * [CodePen](http://codepen.io/)
  * [CodeShare](https://codeshare.io)
  * [CollabEdit](http://collabedit.com)
  * [CodeAnywhere](https://codeanywhere.com) - IDE
  * [JSFiddle](https://jsfiddle.net/) - HTML, CSS and JavaScript |
    see [list](https://www.sitepoint.com/7-code-playgrounds/)
  * [OnlineGDB](https://www.onlinegdb.com/online_python_compiler) - Java, Python, Haskell, Swift, etc.
  * [SoloLearn](https://code.sololearn.com) - C/C++, C#, HTML/CSS/JS, Java, Python3, PHP, Ruby
  * [Repl.it](https://repl.it) -
    [Python](https://repl.it/languages/python3) and [more](https://repl.it/languages/)
  * [Awesome Online IDE](https://github.com/styfle/awesome-online-ide)
  * [Go Playground](https://play.golang.org/)
  * [Rust](https://play.rust-lang.org/)

### Others

  * [50 Shades of Go](http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/)
  * [Go error vs try...catch/except](https://opencredo.com/blogs/why-i-dont-like-error-handling-in-go/)
  * [Rust Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)



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

  Binary Tree
  - A binary tree is a tree data structure in which each parent node can have at most two children.

  Full Binary Tree
  - A full Binary tree is a special type of binary tree in which every parent node has either two or no children.

  Complete Binary tree
  - Every level must be completely filled
  - All the leaf elements must lean towards the left.
  - The last leaf element might not have a right sibling i.e. a complete binary tree doesn't have to be a full binary tree.

  Heap
  - A special tree-based data structure.
  - A complete binary tree.
  - All nodes in the tree follow the property that they are greater than their children i.e. the largest element is at the root and both its children and smaller than the root and so on. Such a heap is called a max-heap. If instead all nodes are smaller than their children, it is called a min-heap.

  Problems:
  * Find if one B-tree contains another B-tree.
  * Perform in-order traversal without recursion.
  * Perform pos-torder traversal without recursion.
  * Perform pre-order traversal in a given binary tree.


<a name="ds-graph"></a>
### Graph

  * Detect a cycle in a graph.



<br/><a name="design"></a>
## Design questions

<a name="oop"></a>
### OOP

  * Designing a simple card game.
    - How to store the order of all the players (data structures)
    - How to break it up into classes (card, game, player, etc)
    - Create properties/fields and functions/methods.


<a name="design-db"></a>
### Database Design

#### Concepts

  * ACID
    - **Atomicity**: Transactions are often composed of multiple statements. Atomicity guarantees that each transaction is treated as a single "unit", which either succeeds completely, or fails completely: if any of the statements constituting a transaction fails to complete, the entire transaction fails and the database is left unchanged. An atomic system must guarantee atomicity in each and every situation, including power failures, errors and crashes.

    - **Consistency**: ensures that a transaction can only bring the database from one valid state to another, maintaining database invariants: any data written to the database must be valid according to all defined rules, including constraints, cascades, triggers, and any combination thereof. This prevents database corruption by an illegal transaction, but does not guarantee that a transaction is correct. Referential integrity guarantees the primary key - foreign key relationship.

    - **Isolation**: Transactions are often executed concurrently (e.g., multiple transactions reading and writing to a table at the same time). Isolation ensures that concurrent execution of transactions leaves the database in the same state that would have been obtained if the transactions were executed sequentially. Isolation is the main goal of concurrency control; depending on the method used, the effects of an incomplete transaction might not even be visible to other transactions.

    - **Durability**: guarantees that once a transaction has been committed, it will remain committed even in the case of a system failure (e.g., power outage or crash). This usually means that completed transactions (or their effects) are recorded in non-volatile memory.

#### SQL Query

  * For DB tables:

    ```sql
    -- containers(id, name);
    CREATE TABLE IF NOT EXISTS containers (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK for containers',
      `name` VARCHAR(45) NULL COMMENT 'container name',
      PRIMARY KEY (`id`)
    );

    -- items(id, type);
    CREATE TABLE IF NOT EXISTS items (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK for items',
      `type` VARCHAR(45) NULL COMMENT 'Item type',
      PRIMARY KEY (`id`)
    );

    -- containeritem(container_id, item_id);
    CREATE TABLE IF NOT EXISTS containeritem (
      `container_id` INT NOT NULL COMMENT 'Composite PK: FK to containers.id',
      `item_id` INT NOT NULL COMMENT 'Composite PK: FK to items.id',
      CONSTRAINT `FK__containeritem_container_id`
        FOREIGN KEY (`container_id`)
        REFERENCES `containers` (`id`),
      CONSTRAINT `FK__containeritem_item_id`
        FOREIGN KEY (`item_id`)
        REFERENCES `items` (`id`)
    );
    ```
    Write a SQL query to list all container names, item types, and count of types (including zero) for each container.

    ```sql
    SELECT d.name, d.type,
      CASE WHEN ci.item_id IS NULL THEN 0 ELSE count(ci.item_id) END as 'count'
      FROM (
      SELECT c.id as 'c_id', c.name, i.id as 'i_id', i.type
        FROM containers c
       CROSS JOIN items i
      ) d  -- optionally to use CTE
     LEFT OUTER JOIN containeritem ci ON d.i_id = ci.item_id
      AND d.c_id = ci.container_id
     GROUP BY d.name, d.type
     ORDER BY d.name, d.type
    ;
    ```
    See http://sqlfiddle.com/#!9/20fa2b/52


<a name="design-system"></a>
### System Design

#### Checklist

  * A.B.C.D.
    - **_A_**sk questions (what features? how much to scale? ...)
    - Don't use **_b_**uzzword
    - **_C_**lear and organized thinking
    - **_D_**rive discussion `:_**)`

  * Questions to ask
    - Features (scope)
    - Define APIs (who's calling the interface and how)
    - Availability (host/site down)
    - Latency performance (faster with cache for customer-facing service)
    - Scalability (from hundreds of users to thousands, millions, ...)
    - Durability (secured without data loss nor being compromised)
    - Class diagram
    - Security and privacy
    - Cost effective
    - Usability

  * Design philosophy

    * Scalability
      - vertical (more cpu, mem, storage on the same host, has limitation)
      - horizontal (adding more hosts)

    * CAP theorem
      A distributed database system can only have 2 of the 3:

      - **Consistency**: every read receives a recent write or an error. (note difference in [ACID](https://en.wikipedia.org/wiki/ACID))
      - **Availability**: every request receives a (non-error) response - without guarantee that it contains the most recent write.
      - **Partition tolerance**: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.
        <br/><u>__2 options__</u> on partition failure:
        * Cancel the operation to decrease the availability but ensure consistency.
        * Proceed with the operation and thus provide availability but risk inconsistency.
        * Note: such trade-off only apply on network partition or failure.

    * ACID vs BASE
      - BASE (Basically Available, Soft state, Eventual consistency), a consistency model used in distributed computing to achieve high availability, with (weak) guarantees that, if no new updates are made to a given data item, eventually all accesses to that item will return the last updated value.

    * Strong vs eventual consistency
      - Database systems designed with traditional ACID guarantees in mind such as RDBMS choose consistency over availability, whereas systems designed around the BASE philosophy, common in the NoSQL movement for example, choose availability over consistency.

    * Relational database vs NoSQL
      - RDMS
      - NoSQL types:
        * key/value pairs
        * wide column
        * document based
        * graph based

    * Partitioning/sharding data
      - Partitioning performs division of a logical database or its constituent elements into distinct independent parts.
      - Sharding, a horizontal partitioning, is the act of taking a data set and splitting it across multiple machines.
      - Consitent Hashing is a method/algorithm to determine which machine any particular piece of data goes to.

    * Optimistic vs passimistic locking

    * Cache policy

    * Datacenter, racks, hosts

    * CPU, memory, hard drive, and network bandwidth (limited resources)

    * Random vs sequential read/write on disk

  * Concepts in IT

    * http vs http2 vs websockets
    * tcp/ip model (vs osi 7 layers), tcp (document) vs udp (stream/video)
    * ipv4 (32-bit) vs ipv6 (128-bit)
    * dns lookup
    * https, TLS, public key infrastructure and certificate authority (CA)
    * symmetric (e.g. AES) vs asymmetric (public/private key) encryption
    * load balancer: L4 () or L7
    * edges server (e.g. CDN)
    * space-efficient probabilistic data structure
      - [Bloom filters](https://en.wikipedia.org/wiki/Bloom_filter)
      - [Count-Min sketch](https://bravenewgeek.com/tag/count-min-sketch/)
      - [HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog) - [HLL](http://www.yoonper.com/post.php?id=79)
      - see [Js code](https://github.com/Callidon/bloom-filters)
    * consensus over distributed hosts ([Paxos](https://medium.com/coinmonks/paxos-made-simple-3b83c05aac37))
    * design patterns and object oriented design
    * virtual machine and containers
    * publisher-subscriber over queue (pub-sub architecture)
    * multithreading, locks, synchronization, CAS (compare and swap)
    * map reduce

  * Technologies

    * Cassandra (wide column, high scalability)
    * MongoDB / Couchbase
    * Memcached, Redis (distributed cache)
    * Zookeeper (centralized configuration management, all in mem, scale for reads, but not for writes)
    * Kaffa (fault tolerant high available queue, deliver message once, keep in order)
    * HAProxy


#### Example: Find the peakest time

  From a long list of trip time (with Start and End time, sorted by Started), e.g. within a whole month, find the peakest trip time.¶

  ```go
  type Trip struct {
    Start time
    End time
  }

  // assuming the list (e.g. a whole month/year) is sorted by start time
  func countPeakTrips(a []Trip) int {

  }
  ```


#### Example: Design a stock data system

  * requirements
    - get real time price
    - get historic trend
  * data schema and database
  * misc consideration


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
      x_range = range(len(arr)-1, 0, -1)
      for num in x_range:
          for i in range(num):
              is_upper = not reversed_order and arr[i] > arr[i+1]
              is_lower = reversed_order and arr[i] < arr[i+1]
              if is_lower or is_upper:
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
## Non-technical

  * [Psychological Tricks](https://github.com/yangshun/tech-interview-handbook/blob/master/non-technical/psychological-tricks.md)
  * [Questions to ask](https://github.com/yangshun/tech-interview-handbook/blob/master/non-technical/questions-to-ask.md)
  * [Negotiation](https://github.com/yangshun/tech-interview-handbook/blob/master/non-technical/negotiation.md)
  * [STAR](http://www.rightattitudes.com/2008/07/15/star-technique-answer-interview-questions/)


<br/><a name="reading"></a>
## Reading

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
  * https://javarevisited.blogspot.com/2017/07/top-50-java-programs-from-coding-Interviews.html
  * https://www.geeksforgeeks.org/
  * https://www.geeksforgeeks.org/must-do-coding-questions-for-companies-like-amazon-microsoft-adobe/
  * https://www.geeksforgeeks.org/top-10-algorithms-in-interview-questions/
  * https://medium.com/basecs (basics of computer science)
  * https://medium.freecodecamp.org/the-ultimate-guide-to-preparing-for-the-coding-interview-183251ee36c9
  * https://www.interviewcake.com/google-interview-questions
  * http://overthewire.org/wargames/



<div><br/>
&raquo; Back to <a href="#contents">Contents</a> | <a href="../README.md">Home</a> &laquo;
<a href="https://github.com/dockerian" style="text-decoration:none;"><img src="https://avatars3.githubusercontent.com/u/22064108?s=400&v=4" style="border:0;height:50;width:50px;vertical-align:middle" height="50" alt="Dockerian" border="0" title="Dockerian" align="right" valign="middle" /></a>
</div>

# Python Study Notes

> Learning Python with `import this` and etc.

## Contents

  * [Concurrency](#concurrency)
  * [Date/Time](#datetime)



<br/><a name="concurrency"></a>
## Concurrency

### Multithreading

> For UI, I/O or Network usage.

  * Using `threading` and `queue`

    ```python
    import threading
    from queue import Queue

    a_lock = threading.Lock()
    results = []  # a list of processed results
    data = []  # a list of items

    def process(data_item):
        with a_lock:
            # process data_item, append result to results
            pass

    def threader():
      while True:
        # get the job from the front of the queue
        process(q.get())
        q.task_done()

    q = Queue()
    max_threads = 5
    for x in range(max_threads):
        thread = threading.Thread(target = threader)
        # set daemon to ensure the thread will die when the main thread dies;
        # otherwise, set to False to keep it running.
        t.daemon = True
        t.start()

    for data_item in data:
        q.put(data_item)  # producer
    ```

  * Creating a `ThreadPool`

    ```python
    from queue import Queue
    from threading import Thread

    class Worker(Thread):
        """ Thread executing tasks from a given tasks queue """
        def __init__(self, tasks):
            Thread.__init__(self)
            self.tasks = tasks
            self.daemon = True
            self.start()

        def run(self):
            while True:
                func, args, kargs = self.tasks.get()
                try:
                    func(*args, **kargs)
                except Exception as e:
                    # An exception happened in this thread
                    print(e)
                finally:
                    # Mark this task as done, whether an exception happened or not
                    self.tasks.task_done()

    class ThreadPool:
        """ Pool of threads consuming tasks from a queue """
        def __init__(self, num_threads):
            self.tasks = Queue(num_threads)
            for _ in range(num_threads):
                Worker(self.tasks)

        def add_task(self, func, *args, **kargs):
            """ Add a task to the queue """
            self.tasks.put((func, args, kargs))

        def map(self, func, args_list):
            """ Add a list of tasks to the queue """
            for args in args_list:
                self.add_task(func, args)

        def wait_completion(self):
            """ Wait for completion of all the tasks in the queue """
            self.tasks.join()
    ```

  * Using `ThreadPoolExecutor`


### Parallel

> For CPU-bound calculation.

  * Using `Pool.apply()`

    ```python
    # Parallelizing using Pool.apply()
    import multiprocessing as mp

    # Step 1: Initialize multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())
    # Step 2: Use `pool.apply` a function `a_func` with (tuple) args
    results = [pool.apply(a_func, args=(row, other, args)) for row in data]
    # Step 3: Must close
    pool.close()

    print(results)
    ```

  * Using `Pool.map()`

    ```python
    # Parallelizing using Pool.map()
    import multiprocessing as mp

    # Step 1: Initialize multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())
    # Step 2: Use `Pool.map()` accepts only one iterable as argument
    results = pool.map(a_func, [row for row in data])
    # Step 3: Must close
    pool.close()
    ```

  * Using `Pool.starmap()`

    ```python
    # Parallelizing with Pool.starmap()
    import multiprocessing as mp

    pool = mp.Pool(mp.cpu_count())
    # note: a_func(row, other, args) must return a result
    results = pool.starmap(a_func, [(row, other, args) for row in data])
    pool.close()
    ```

### Parallel (Asynchronously)

  * Using `Pool.apply_async()`

    ```python
    import multiprocessing as mp

    pool = mp.Pool(mp.cpu_count())

    for i, row in enumerate(data):
      # note: a_func(i, row, other, args) must return (i, result)
      pool.apply_async(a_func, args=(i, row, other, args))
    pool.close()
    pool.join()
    # optionally results could be got by a `callback` function from apply_async.
    apply_results = pool.ApplyResult.get()
    apply_results.sort(key=lambda x: x[0])  # sorting by original index
    results = [r for i, r in apply_results]
    ```
    or calling `apply_async` without `callback` nor `ApplyResult`:

    ```python
    async_results = [
      # note: a_func(i, row, other, args) must return (i, result)
      pool.apply_async(a_func, args=(i, row, other, args)) for i, row in enumerate(data)
    ]
    pool.close()
    pool.join()
    results = [r.get()[1] for r in async_results]
    ```

  * Using `Pool.starmap_async()`

    ```python
    import multiprocessing as mp

    pool = mp.Pool(mp.cpu_count())
    # a_func(i, row, other, args) returns a result without index
    results = pool.starmap_async(a_func, [
      (i, row, other, args) for i, row in enumerate(data)
    ]).get()
    pool.close()
    ```

  * Using `Pool.map_async()`

    ```python
    import multiprocessing as mp

    pool = mp.Pool(mp.cpu_count())
    # a_func(row) returns a result without index
    results = pool.map_async(a_func, [
      row for i, row in enumerate(data)
    ]).get()
    pool.close()
    ```


### Reference

  - https://www.metachris.com/2016/04/python-threadpool/
  - https://www.pythonsheets.com/notes/python-concurrency.html
  - https://www.machinelearningplus.com/python/parallel-processing-python/
  - https://sebastianraschka.com/Articles/2014_multiprocessing.html



<br/><a name="datetime"></a>
## Date/Time

> Default `datetime` objects are "naïve" without the time zone information.

### From `datetime` object

  * Local (PDT) to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):

    ```
    import datetime
    datetime.datetime.now().isoformat()
    > '2019-06-03T10:58:47.723650'
    ```

  * Local (PDT) to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) without microsecond:

    ```
    import datetime
    datetime.datetime.now().replace(microsecond=0).isoformat()
    > '2019-06-03T10:58:47'
    ```

  * Local (PDT) to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) with time zone:

    ```
    import datetime, time
    # calculate the offset, taking into account of daylight saving time
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    dtz = datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset))
    dtz.isoformat()
    > '2019-06-03T10:58:47.723650-07:00'
    ```

  * Local (PDT) to RFC 5322 / 2282 / 1123

    ```
    import datetime, time
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    dtz = datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset))
    dtz.strftime("%a, %d %b %Y %H:%M:%S %z")
    > 'Mon, 03 Jun 2019 10:58:47 -0700'
    ```

  * UTC to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):

    ```
    import datetime
    datetime.datetime.utcnow().isoformat()
    > '2019-06-03T18:58:47.723650'
    ```

  * UTC to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) with time zone ([RFC 3399](https://tools.ietf.org/html/rfc3339) compatible):

    ```
    import datetime
    datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    > '2019-06-03T18:58:47.723650+00:00'
    ```
    Notes:
    - Method `datetime.replace` returns a new `datetime` object without modifying the original.
    - Same to replace `datetime.timezone.utc` with `pytz.utc` if `pytz` is imported.

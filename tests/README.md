# Python Testing

> Everything about testing.


<br/><a name="contents"></a>
## Contents

* [Online Tutorials](#tutorials)
* [Free APIs](#free-api)




<br/><a name="tutorials"></a>
## Online Tutorials

  * [Real Python Testing](https://realpython.com/python-testing/)
  * [Understanding GIL](http://www.dabeaz.com/python/UnderstandingGIL.pdf)
    - Parallel execution is forbidden
    - GIL ("global interpreter lock") ensures that only one thread runs in
the interpreter at once
    - Default "check" (can be changed by `sys.setcheckinterval()`) occurs every 100 "ticks" (not time-based but loosely map to interpreter instructions)
    - Python has no thread scheduling (which is left to the host os)
      * GIL thread signaling is the source of big overhead. And far worse on multi-core.
      * the interpreter has no control over scheduling so it just attempts to thread switch as fast as possible with the hope that main will run.
      * the main thread is often blocked on an uninterruptible thread-join or lock.
    - Currently running thread
      * Resets the tick counter
      * Runs signal handlers if the main thread (has any pending)
      * Releases the GIL
      * Reacquires the GIL


<br/><a name="free-api"></a>
## Free API endpoints

  * [Any API](https://any-api.com/)
  * [Collective API List](https://apilist.fun/)
  * [Hosted REST-API ready to respond AJAX requests](https://reqres.in/)
  * [JSON Placeholder](https://jsonplaceholder.typicode.com/)
  * [Public APIs](https://github.com/toddmotto/public-apis)
  * [Rapid API](https://rapidapi.com/)




<div><br/>
<a href="https://github.com/dockerian" style="text-decoration:none;"><img src="https://avatars3.githubusercontent.com/u/22064108?s=400&v=4" style="border:0;height:50;width:50px;" height="50" alt="Dockerian" border="0" title="Dockerian" align="right" valign="top" /></a>
</div>

&raquo; Back to <a href="#contents">Contents</a> | <a href="../README.md">Home</a> &laquo;

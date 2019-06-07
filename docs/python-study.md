# Python Study Notes

> Learning Python with `import this` and etc.

## Contents

  * [Date/Time](#datetime)



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

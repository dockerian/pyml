# API Study

> This page is the note taken from studying RESTful API.



## Content

* [Intro](#intro)
* [RESTful API Concepts](#rest)
  - [Definitions](#rest-def)
  - [Applications and Services](#rest-app)
  - [API Versions](#rest-ver)
  - [Resources & Collections](#rest-res)
  - [REST Idempotency](#rest-idempotency)
  - [Operations](#rest-op)
* [HTTP Headers](#http-headers)
* [Design Flow](#design)



<br /><a name="intro"></a>
## Introduction

### What is API

* It is a interface that is not for users (opposite with UI), but machines (apps, servers)
* consumer: developers that use API to coorperate with the their application; the app may outsource requirements for data or functionality through API by "calling" that API
* provider: people who put API on to the internet, so that developer can use it (eg. Google Maps API)


### API Driven Organizations

* Every part of program is put on an API layer
* And every part serves as a micro API service (likely in cloud computing)
* Having providers and consumers of API within the organization
* Services oriented infrastructure or services oriented architecture
* Example: Amazon is a full API driven organization
* More easily maintain or upgrade



<br/><a name="rest"></a>
## RESTful API Concepts
<a name="rest-def"></a>
### Definitions

* Representational State Transfer Application Programming Interface

* Representational
  - Representation of resources: resource can be anything that can be named on the internet (eg. list of name, article, video)
  - HTTP is: client sends a request and tothe web server, and the web server responses with a resource (but actually a representation of resource)
  - URL: Uniform Resource Locator
  - Request example: https://api.foobar.com/employees?name=John
    - protocol: "https"
    - host: "api.foobar.com"
    - resource/entity: "employees"
    - query: "?name=John"
  - State: application state that has the resources

<a name="rest-app"></a>
### Applications and Services

  An application is a collection of related services.

  * A service (or microservice) defines a set of resources and operations on those resources. A service is referenced by a service name.
  * A service name is a combination of host (site URL), the root path to service, and the service version. The root path may have slash-separated components.
  * URI BNF description:

    ```
    <service-name> = <scheme>"//"<site-url>"/"<root-path>"/"<version>
    <scheme> = "https:"
    <root-path> = <name> [ "/" <name> ]*
    <version> = "v"<version-number>
    <version-number> = <digit>
    ```
  * Example:
    - https://translation.googleapi.com/language/translate/v2

<a name="rest-ver"></a>
### API Versions

  * Services are versioned using [semantic versioning](https://semver.org) scheme with `<MAJOR>.<MINOR>.<PATCH>` version numbers.
    - `<MAJOR>` version makes incompatible API changes
    - `<MINOR>` version adds functionality in a backwards-compatible manner
    - `<PATCH>` version makes backwards-compatible bug fixes
  * Incompatible (breaking) changes include:
    - Changing behavior for an existing API
    - Removing or renaming APIs or API parameters
    - Changing Error Codes and Fault Contracts
    - Anything violates the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment)
  * Different versions of a service may co-exist to allow clients to migrate to new service versions. Release policy determines how many versions of a service can exist and when old versions are retired.

<a name="rest-res"></a>
### Resources & Collections (Nouns)

A resource is an entity or object that can be referenced by the RESTful API.
A resource-oriented API is generally modeled as a resource hierarchy, where each node is either a simple resource or a collection resource. For convenience, they are often called as a resource and a collection, respectively.

  * A collection contains a list of resources of the same type. For example, a user has a collection of contacts.
  * A resource has some state and zero or more sub-resources. Each sub-resource can be either a simple resource or a collection resource.
  * Each resource has a unique resource name. A resource name consists of a service name, a simple resource name, or a collection resource name and an ID if appropriate. If the resource is in a hierarchy of objects, then parent resources are specified before the child resource.
    - **Convention**: *Collection resource names should be unabbreviated and in plural form.*
  * A non-singleton collection name specified without an `{id}` refers to all the items in the collection. When a non-singleton collection name is specified as the parent of a resource, all its items can be referenced by using "`-`" as the ID. This notation references all the child resources of all the parent resources.
    - Resource ID's can be arbitrary text, e.g., numbers or strings.
  * A *singleton resource* can be used when only a single instance of a resource exists within its parent resource (or within the API, if it has no parent).
    - The standard Create and Delete methods **must be omitted** for singleton resources; the singleton is implicitly created or deleted when its parent is created or deleted (and implicitly exists if it has no parent). The resource must be accessed using the standard Get and Update methods.
    - Singleton example: `/configuration` or `/users/settings`
  * URI BNF description:

    ```
    <resource> = <scheme>"//"<service-name>["/"<resource-name>["/"<id>]]*
    <resource-name> = <simple-resource-name> | <collection-resource-name>
    <simple-resource-name> = <name-singular>
    <collection-resource-name> = <name-plural>["/"<id>]
    <id> = <arbitrary-string> | "-"
    ```

<a name="rest-idempotency"></a>
### REST Idempotency

| Standard      | HTTP Method  | Request Body | Response Body   |Idempotent|Safe|
|:--------------|:-------------|:-------------|:----------------|:--------:|:--:|
| List          | GET          | N/A          | Resource list   | Yes      | Y  |
| Get/fetch     | GET          | N/A          | Single resource | Yes      | Y  |
| Create        | POST         | Resource     | New resource    | No       | N  |
| Update/Change | PUT or PATCH | Resource *   | Resource        | Yes/No * | N  |
| Delete        | DELETE       | N/A          | N/A             | Yes      | N  |

  * Form parameters (`POST`) may be used in place of URL query parameters (`GET`), following the same REST-style mapping rule for mapping request fields to query parameters. The supported Content-Type is `application/x-www-form-urlencoded`.

  * An idempotent HTTP method is an operation that will produced the same result if executed once or multiple times (that can be called many times without different outcomes). No matter how many times it is called, the result should be the same.
    - `PUT` is required to use a complete entity instance as payload to "replace" (or "create" if not exist) a resource.
    - `PATCH` can be used to update partial entity, which may not guarantee "**idempotency**".
      `PATCH` operation might also indicate to do "move", "create", or "delete".
    - **Idempotency** is important in building a fault-tolerant API.

  * Non-safe (and non-idempotent) methods should never be cached by any middleware proxies.

<a name="rest-op"></a>
### Operations

  * REQUEST: the actions that defines what kind of request of type of HTTP request were sending to the web server
    - `GET`, `PUT`, `PATCH`, `POST`, `DELETE` (CRUD)
    - `HEAD`, `OPTIONS`, `CONNECT`, `TRACE`

  * RESPONSE: representation of resource, easy to read and implemented into applications, e.g. REST XML-RPC SOAP JSON Serialized PHP

  * API is like a bunch of useful methods or functions, parameters is like the parameters we can pass on to these methods

  * A standard method could return a long-running operation for requests that do not complete within the time-span of the single API call.

  * Collection operators:
    - Filtering: `_filter`
    - Field selection: `_fields`
    - Pagination: `_offset`, `_limit`, `_size`
    - Sorting: `_order_by`


<br/><a name="http-headers"></a>
## HTTP Headers

### HTTP Request Headers

| Header           | Type        |Description  |
|:-----------------|:------------|:------------|
| Authorization    |String       |Use "Token" or "Bearer" format.|
| Date             |RFC 5322 Date|GMT/UTC timestamp of the request.|
| Accept           |Content type |(Hint of) the requested content type for the response, e.g. `application/json` or `text/javascript` (for JSONP).|
| Accept-encoding  |gzip, deflate|REST endpoints SHOULD support GZIP and DEFLATE encoding, when applicable. For very large resources, services MAY ignore and return uncompressed data.|
| If-Match         ||Only if the request matches one of listed `ETags`.|
| If-Modified-Since||Response 304 w/o body if no change; otherwise 200 w/ latest.|
| Prefer           ||return=minimal,<br/>return=representation|

### HTTP Response Headers

| Header            | Required |Description  |
|:------------------|:---------|:------------|
| Date              | All      |RFC 5322 GMT/UTC timestamp the response was processed.|
| Content-Type      | All      ||
| Content-Encoding  | All      |GZIP or DEFLATE, as appropriate|
| Preference-Applied| If specified in request||
| Location          | If the operation creates a resource||

  * Timestamp uses unixtime (integer) or ISO 8601 date in UTC.
  * Content type uses JSON defined by RFC 4627.

### Status Code

  * `1xx` (Informational)
    - `100 Continue`
  * `2xx` (Success)
    * `201 CREATED` for `POST`
    * `200 OK` or `204 No Content` for `PUT` method success
    * `200 OK` for other methods success
    - `202 Accepted` (long-running operation, with `Location` in header)
    - `203 Non-Authoritative Information`
    - `205 Reset Content`
    - `206 Partial Content`
  * `3xx` (Redirection)
    - `300 Multiple Choices`
    - `301 Moved Permanently`
    - `302 Found`
    - `303 See Other`
    * `304 Modified`
    - `305 Use Proxy`
    - `307 Temporary Redirect`
  * `4xx` (Client Error)
    * `400 Bad Request`
    * `401 Unauthorized` (authN, unauthenticated / not authenticated)
    * `403 Forbidden` (authZ, no sufficient permission)
    * `404 Not Found`
    * `405 Method Not Allowed`
    * `406 Not Acceptable`
    * `408 Request Timeout`
    * `409 Conflict` (Concurrency conflict, e.g. read-modify-write conflict)
    - `499 Client Closed Request` (cancelled by client)
  * `5xx` (Server Error)
    * `500 Internal Server Error` (server corruption, possible data loss)
    - `501 Not Implemented`
    * `502 Bad Gateway`
    - `503 Service Unavailable`
    - `504 Gateway Timeout`


<br/><a name="design"></a>
## Design Flow

  * Define the service provided by the API.
  * Determine what types of resources the service provides.
  * Determine the relationships between resources.
  * Decide the resource name schemes based on types and relationships.
  * Decide the resource (entity) schemas.
  * Add methods to resources.

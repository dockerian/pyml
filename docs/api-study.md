# API Study

> This page is the note taken from studying RESTful API.



## Content

* [Intro](#intro)
* [RESTful API Concepts](#rest)
  - [Definitions](#rest-def)
  - [Resource types](#rest-res-types)
  - [Applications and Services](#rest-app)
  - [API Versions](#rest-ver)
  - [Resources & Collections](#rest-res)
  - [REST Idempotency](#rest-idempotency)
  - [Operations](#rest-op)
* [HTTP Headers](#http-headers)
* [Design Flow](#design)
* [Microservices vs SOA](#msa-vs-soa)
* [CORS](#cors)



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


<a name="rest-res-types"></a>
### Resource Types

* **Document**: a singular concept that is akin to an object instance or database record. e.g.: http://api.soccer.restapi.org/leagues/seattle/teams/trebuchet

* **Collection**: a server-managed directory of resources. Clients may propose new resources to be added to a collection. However, it is up to the collection to choose to create a new resource, or not. Example: http://api.soccer.restapi.org/leagues/seattle/teams

* **Store**: a client-managed resource repository. A store resource lets an API client put resources in, get them back out, and decide when to delete them. On their own, stores do not create new resources; therefore a store never generates new URIs. Instead, each stored resource has a URI that was chosen by a client when it was initially put into the store. Example: `PUT /users/1234/favorites/alonso`.

* **Controller**: models a procedural concept.
  - Controller resources are like executable functions, with parameters and return values; inputs and outputs. Like a traditional web application's use of HTML forms, a REST API relies on controller resources to perform application-specific actions that cannot be logically mapped to one of the standard methods (create, retrieve, update, and delete, also known as CRUD).
  - Controller names typically appear as the last segment in a URI path, with no child resources to follow them in the hierarchy.
  - **Note**: Controller resource remains argument about "resource must be a noun, instead of a verb".
  - Example: `POST /alerts/245743/resend`


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

  * Usages:
    - Checking whether a resource has changed. This is useful when maintaining a cached version of a resource (`HEAD`).
    - Checking whether a resource exists and is accessible (`HEAD`, `OPTIONS`). For example, validating user-submitted links in an application.
    - Retrieving metadata about the resource, e.g. its media type or its size, before making a possibly costly retrieval (`HEAD`).
    - Identifying which HTTP methods a resource supports (`OPTIONS`).

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
| Allow            ||List of allowed methods a resource supports, thru `OPTIONS` request, e.g. `Allow: GET,HEAD,POST,OPTIONS,TRACE`.|
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
    - `203 Non-Authoritative Information` (enclosed payload has been modified from that of the origin server's 200 OK response by a transforming proxy)
    - `204 No Content` (success but additional content in the response payload body)
    - `205 Reset Content` (desires the user agent to reset the "document view")
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
      (the client has a request with header `Accept-*` that the server is unable to fulfill)
    * `408 Request Timeout`
      (server decided to close the connection rather than continue waiting request message to complete within certain time)
    * `409 Conflict` (Concurrency conflict, e.g. read-modify-write conflict)
    - `499 Client Closed Request` (cancelled by client)
  * `5xx` (Server Error)
    * `500 Internal Server Error` (server corruption, possible data loss)
    - `501 Not Implemented`
    * `502 Bad Gateway`
      (service temporarily overloaded, temporary error, or proxy server received an invalid response from an upstream server)
    - `503 Service Unavailable`
      (simply refuse, or may with `Retry-After` header on temporary overloaded or scheduled maintenance)
    - `504 Gateway Timeout`
  * See
    - [httpstatuses](https://httpstatuses.com/)
    - [more](https://www.restapitutorial.com/httpstatuscodes.html)


<br/><a name="design"></a>
## Design Flow

  * Define the service provided by the API.
  * Determine what types of resources the service provides.
  * Determine the relationships between resources.
  * Decide the resource name schemes based on types and relationships.
  * Decide the resource (entity) schemas.
  * Add methods to resources.



<br/><a name="msa-vs-soa"></a>
## Microservice vs SOA

### 3 types of architectures

  * Monolithic is similar to a big container (single unit) wherein all the software components of an application are assembled together and tightly packaged.
  * SOA (Service-Oriented Architecture) is essentially a collection of services (coarse-grained). These services communicate with each other. The communication can involve either simple data passing or it could involve two or more services coordinating some activity.
    - Functional Service (business users)
    - Enterprise Service (shared services team)
    - Application Service (application development team)
    - Infrastructure Service (infrastructure services team)
  * Microservices, aka Microservice Architecture, is an architectural style that structures an application as a collection of small autonomous services, modeled around a business domain. (fine-grained)
    - Functional Service and Infrastructure Service by application development teams
    - Limited service taxonomy
    - Minimal coordination

### Microservices vs SOA

  * **Service Granularity**
    - Service components within a microservices architecture are generally single-purpose services that do one thing really well.
    - With SOA, service components can range in size anywhere from small application services to very large enterprise services. It is common to have a service component within SOA represented by a large product or even a subsystem.
  * **Component Sharing**
    - Component sharing is one of the core tenets of SOA. As a matter of fact, component sharing is what enterprise services are all about. SOA enhances component sharing, whereas MSA tries to minimize on sharing through "bounded context".
    - A bounded context refers to the coupling of a component and its data as a single unit with minimal dependencies. As SOA relies on multiple services to fulfill a business request, systems built on SOA are likely to be slower than MSA.
  * **Middleware vs API layer**
    - The microservices architecture pattern typically has what is known as an API layer, whereas SOA has a messaging middleware component.
    - The messaging middleware in SOA offers a host of additional capabilities not found in MSA, including mediation and routing, message enhancement, message, and protocol transformation.
    - MSA has an API layer between services and service consumers.
  * **Remote services**
    - SOA architectures rely on messaging (AMQP, MSMQ) and SOAP as primary remote access protocols. Most MSAs rely on two protocols -- REST and simple messaging (JMS, MSMQ), and the protocol found in MSA is usually homogeneous.
  * **Heterogeneous interoperability**
    - SOA promotes the propagation of multiple heterogeneous protocols through its messaging middleware component. SOA should be used to integrate several systems using different protocols in a heterogeneous environment.
    - MSA attempts to simplify the architecture pattern by reducing the number of choices for integration. MSA is a better option if all services could be exposed and accessed through the same remote access protocol.

### Comparison chart

  |SOA|MSA|
  |:--|:--|
  |share-as-much-as-possible|share-as-little-as-possible|
  |importance is on business functionality reuse|importance is on the concept of "bounded context"|
  |have common governance and standards|people collaboration and freedom of other options|
  |use Enterprise Service bus (ESB) for communication|use Simple messaging system|
  |multiple message protocols|lightweight protocols such as HTTP/REST etc.|
  |multi-threaded with more overheads to handle I/O|single-threaded usually with the use of Event Loop features for non-locking I/O handling|
  |maximizes application service reusability|focuses on decoupling|
  |use traditional relational database|use modern relational database|
  |systematic change requires modifying the monolith|systematic change is to create a new service|
  |devOps and CD popular, but not yet mainstream|strong focus on devOps and CD|



<br/><a name="cors"></a>
## CORS

> Cross-Origin Resource Sharing (CORS) is a mechanism that uses additional HTTP
  headers to tell a browser to let a web application running at one origin (domain)
  have permission to access selected resources from a server at a different origin.
> A web application executes a **cross-origin HTTP request** when it requests
  a resource that has a different origin (domain, protocol, and port)
  than its own origin.

### Preflight mechanism

> To protect resources against cross-origin requests that could not originate
  from certain user agents before this specification existed a preflight request
  is made to ensure that the resource is aware of this specification.

  Preflight requests were introduced so that a browser could be sure it was
  dealing with a CORS-aware server before sending certain requests.
  Those requests were defined to be those that were both potentially
  dangerous (state-changing) and new (not possible before CORS due to
  the [Same Origin Policy](https://en.wikipedia.org/wiki/Same-origin_policy)).
  Using preflight requests means that servers must opt-in (by responding
  properly to the preflight) to the new, potentially dangerous types of
  request that CORS makes possible.

### CORS and Preflight Example

  A browser user is logged into a.com. When the user navigates to a malicious
  b.com, where a page includes some JavaScript that tries to send a `DELETE`
  request to a.com/api/resource.
  Since the user is logged into a.com, that request, if sent, would include
  cookies that identify the user.

  Before CORS, the browser's [Same Origin Policy](https://en.wikipedia.org/wiki/Same-origin_policy)
  would have blocked it from sending such request - a.com might have assumed that
  it could never receive such a request, and thus it might have never been hardened
  against such an attack.

  To protect such non-CORS-aware servers, then, the protocol requires
  the browser to first send a preflight request. This new kind of request is
  something that only CORS-aware servers can respond to properly, allowing
  the browser to know whether or not it's safe to send the actual `DELETE`.

  Preflight requests were created so as to reduce (but not fully protect from)
  the attack form on site b.com can `POST` to a.com with the user's cookies -
  a.k.a CSRF ([Cross-Site Request Forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery))
  attack surface for non-CORS-aware servers.


### Reference

  * https://www.codecademy.com/articles/what-is-cors
  * https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
  * https://stackoverflow.com/questions/15381105/cors-what-is-the-motivation-behind-introducing-preflight-requests
  * https://auth0.com/blog/cors-tutorial-a-guide-to-cross-origin-resource-sharing/

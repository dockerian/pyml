# API Study

> This page is the note taken from studying RESTful API.



## Content

* [Intruodction](#intro)
* [Rest API](#rest)



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
## RESTful API

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


### Functions

* REQUEST: the actions that defines what kind of request of type of HTTP request were sending to the web server
  - POST, GET, PUT, DELETE (CRUD)
  - HEAD, OPTIONS

* RESPONSE: representation of resource, easy to read and implemented into applications, eg. REST XML-RPC SOAP JSON Serialized PHP

* API is like a bunch of useful methods or functions, parameters is like the parameters we can pass on to these methods

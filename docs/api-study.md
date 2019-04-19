# API Study
> This page is the note taken from studying API



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
* every part of program is put on an API layer
* The every part serves as an API service
* so they have providers and consumers of API within the organization
* services oriented infrasturacture or services oriented architecture
* can more easily maintain or upgrade
* Amazon if full API driven oranization, now Amazon if the biggest API provider on the planet



<br/><a name="rest"></a>
## Rest API


### Definitions
* Representational State Transfer Application Programming interface
* Representational
  - representation of resources: resource can be anything that can be named on the internet (eg. list of name, article, video)
  - HTTP is: client sends a request and tothe web server, and the web server responses with a resource (but actually a representation of resource)
  - URL: Runiform Resource Locator
  - request example: https://clevertechie.com/img/flowers/lily.jpg(https is protocal. clevertechie.com is the host, rest of request is the resource)
  - state: application state that has the resources


### Rest

#### REQUEST
* verb + URL: eg. GET, POST, PUT, DELETE, the acations that defines what kind of request of type of HTTP request were sending to the web server


### Rest API

#### REQUEST
* REST API end point URL + API method + parameters
* example: (REST API endpoint URL)https://api.flickr.com/services/rest/(method)?method=flickr.photo.sgetinfo&(parameters)photo_id=2079357948
* RESPONSE: representation of resource, easy to read and implemented into applications, eg. REST XML-RPC SOAP JSON Serialized PHP
* API is like a bunch of useful methods or functions, parameters is like the parameters we can pass on to these method
* apigee.com/console/
* json.parser.onlinne.fr
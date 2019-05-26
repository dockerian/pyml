# API Design Notes

> RESTful API Services high level design and dev notes.

<br/><a name="contents"></a>
## Contents

* [Flask API](#flask-api)
* [WSGI Servers](#wsgi-servers)
* [Swagger](#swagger)



<br/><a name="flask-api"></a>
## Flask API

### Comparison

  * https://fastapi.tiangolo.com/alternatives/
  * https://github.com/the-benchmarker/web-frameworks
    - [hug](http://www.hug.rest/) | [github](https://github.com/hugapi/hug)
    - [vibora](https://vibora.io/) | [github](https://github.com/vibora-io/vibora)
    - [falcon](http://falconframework.org/) | [github](https://github.com/falconry/falcon)
    - [fastapi](http://fastapi.tiangolo.com/) | [github](https://github.com/tiangolo/fastapi)
    - [japronto](https://github.com/squeaky-pl/japronto)
    - [bottle](http://bottlepy.org/docs/dev/) | [github]()


### Code-first approach

  * [Blueprint, Flask-RESTPlus, and Swagger](http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/) |
    [source](https://github.com/postrational/rest_api_demo/tree/master/rest_api_demo)
  * [Designing well-structed REST APIs with Flask-RestPlus](https://medium.com/ki-labs-engineering/designing-well-structured-rest-apis-with-flask-restplus-part-1-7e96f2da8850)
  * [Flask REST API with Swagger UI](https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f)
  * [Flask and Flask-RESTPlus](https://nikgrozev.com/2018/10/12/python-api-with-flask-and-flask-restplus/)
  * Requirements:
    - flask
    - flask-restplus
    - fastapi (`pip install fastapi[all]`)
      * fastapi==0.26.0
      * aiofiles-0.4.0
      * aniso8601-3.0.2
      * dnspython-1.16.0
      * email-validator-1.0.4
      * graphene-2.1.3
      * graphql-core-2.1
      * graphql-relay-0.4.5
      * h11-0.8.1
      * httptools-0.0.13
      * promise-2.2.1
      * pydantic==0.26 (`pip install fastapi`)
      * python-multipart-0.0.5
      * rx-1.6.1 ujson-1.35
      * starlette==0.12.0 (`pip install fastapi`)
      * uvicorn-0.7.1
      * uvloop-0.12.2
      * websockets-7.0
    - flasgger (optional)
      * aniso8601==6.0.0
      * flasgger==0.9.2 (15M)
      * Flask-RESTful==0.3.7 (`pip install flask-restful`)
      * mistune==0.8.4 (with flasgger)
  * Example:

    ```python
    from flask import Flask
    from flask_restplus import Api, Resource

    app = Flask(__name__)
    api = Api(app = app)

    ns = api.namespace('main', description='Main APIs')

    @ns.route('/hello')               # Optional using namespace
    @api.route('/hello')              # Create a URL route to this resource
    class HelloWorld(Resource):       # Create a RESTful resource
        def get(self):                # Create GET endpoint
            return {'hello': 'world'}

    if __name__ == '__main__':
      app.run(debug=True)  
    ```
  * See
    - [Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/)
    - [Flasgger](https://github.com/rochacbruno/flasgger/)
    - [Eve](https://docs.python-eve.org/en/stable/)

### Spec-first

  * [Connexion Documentation](https://buildmedia.readthedocs.org/media/pdf/connexion/latest/connexion.pdf)
  * [Using connexion](https://realpython.com/flask-connexion-rest-api/#using-connexion-to-add-a-rest-api-endpoint)

  * Requirements:
    - flask
      * Click==7.0
      * Flask==1.0.3
      * itsdangerous==1.1.0
      * Jinja2==2.10.1
      * MarkupSafe==1.1.1
      * Werkzeug==0.15.4
    - flasgger (optional)
      * aniso8601==6.0.0
      * flasgger==0.9.2
      * Flask-RESTful==0.3.7 (pip install flask-restful)
      * mistune==0.8.4 (with flasgger)
    - connexion
      * certifi==2019.3.9
      * chardet==3.0.4
      * clickclick==1.2.2
      * connexion==2.2.0 (4.2M)
      * idna==2.8
      * inflection==0.3.1
      * jsonschema==2.6.0
      * openapi-spec-validator==0.2.6
      * pathlib==1.0.1
      * PyYAML==5.1
      * requests==2.22.0
      * six==1.12.0
      * urllib3==1.25.2
    - connexion[swagger-ui]
      * flask
      * connexion
      * swagger-ui-bundle
    - pyopenssl
      * asn1crypto==0.24.0
      * cffi==1.12.3
      * cryptography==2.6.1
      * pyOpenSSL==19.0.0
      * pycparser==2.19

  * Example:

    ```python
    import connexion

    app = connexion.App(__name__, specification_dir='./apidoc')
    app.add_api('swagger.yml')  # read from above specification_dir

    @app.route('/')
    def main():
        return {'hello': 'world'}

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8081, debug=True)
    ```


<br/><a name="wsgi-servers"></a>
## WSGI Servers

  * [A Detailed Study of WSGI](https://www.cabotsolutions.com/2017/11/a-detailed-study-of-wsgi-web-server-gateway-interface-of-python)
  * An Introduction to Python WSGI Servers
    - [Part 1](https://www.appdynamics.com/blog/engineering/an-introduction-to-python-wsgi-servers-part-1/)
    - [Part 2](https://www.appdynamics.com/blog/engineering/a-performance-analysis-of-python-wsgi-servers-part-2/)
  * [Choosing a Fast Python API Framework](https://fgimian.github.io/blog/2018/05/17/choosing-a-fast-python-api-framework/)
  * [Gunicorn Documentation](https://buildmedia.readthedocs.org/media/pdf/gunicorn-docs/stable/gunicorn-docs.pdf)
  * [Python WSGI Server Benchmark](https://github.com/kubeup/python-wsgi-benchmark)
  * [WSGI Servers](https://www.fullstackpython.com/wsgi-servers.html)



<br/><a name="swagger"></a>
## Swagger

  The API specifications is designed in [swagger-editor](https://editor.swagger.io/).
  On a dev box with docker installed, `Makefile` provides a script to run a swagger-editor locally (in docker container):

  ```
  make swagger-editor  # this will open swagger-editor on http://localhost:8881
  # or with specific port
  SWAGGER_PORT=9980 make swagger-editor
  ```
  **Note**:
  - The swagger-editor is a distributed web app with embedded "Petstore" spec
  - Open or drag-and-drop [swagger.yaml](../apidoc/v1)

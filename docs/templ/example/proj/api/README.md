# API Design Notes

> RESTful API Services high level design and dev notes.

<br/><a name="contents"></a>
## Contents

* [Flask API](#flask-api)
* [Swagger](#swagger)



<br/><a name="flask-api"></a>
## Flask API

### Code-first approach

  * [Blueprint, Flask-RESTPlus, and Swagger](http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/) |
    [source](https://github.com/postrational/rest_api_demo/tree/master/rest_api_demo)
  * [Flask REST API with Swagger UI](https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f)
  * Requirements:
    - flask
    - flask-restplus
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
    - connexion
      * certifi==2019.3.9
      * chardet==3.0.4
      * clickclick==1.2.2
      * connexion==2.2.0
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

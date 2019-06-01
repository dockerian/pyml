"""
api/__models.py

see https://pydantic-docs.helpmanual.io/
"""
from pydantic import BaseModel, Schema


class ApiSchema(BaseModel):
    name: str = Schema(
        ..., description='Name of the API service.')
    description: str = Schema(
        None, description='Description of the API service.')
    endpointURL: str = Schema(
        ..., title='Endpoint URL',
        description='Deployment endpoint URL of the API service.')
    environment: str = Schema(
        ...,
        description='Deployment environment for the API service.',
        **{"example": "dev"})
    redocsUrl: str = Schema(
        None, description='Open API documentation.')
    swaggerFile: str = Schema(
        None, description='Swagger specification file of the API service.')
    swaggerUi: str = Schema(
        None, description='Swagger documentation URL.')
    version: str = Schema(
        None, description='API service version.',
        **{"example": "1.0.0"})

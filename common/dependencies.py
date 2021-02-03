import secrets

import fastapi.openapi.utils as fu
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

BASIC_AUTH_USER = "admin"
BASIC_AUTH_PASSWORD = "admin"

fu.validation_error_definition = {
    "title": "ValidationError",
    "type": "object",
    "properties": {
        "error-field": {"title": "Error Message", "type": "string"},
    },
    "required": ["error-field"],
}

fu.validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "errors": {
            "title": "details",
            "type": "object",
            "properties": {"error-field": {"title": "Error Message", "type": "string"}},
            "required": ["error-field"],
        }
    },
}

security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, BASIC_AUTH_USER)
    correct_password = secrets.compare_digest(credentials.password, BASIC_AUTH_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

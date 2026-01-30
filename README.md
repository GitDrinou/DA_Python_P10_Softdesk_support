# SoftDesk Support

## Version
1.0.0

## Overview
This project consists of building a secure RESTful API, provides a robust 
system of managing projects, issues and comments in collaborative 
environment. It is designed for SoftDesk Support and enables users to track, 
create, and manage ressources efficiently.

The API has been developed using Django REST Framework, following:
- OWASP security best practices
- GDPR compliance rules
- Green code principles
- Secure authentication using JWT
- Fine-gained permission management per user

## Prerequisites
Before starting, make sure you have installed:
- Python ≥ 3.10
- Git
- Pipenv (to install it if needed `pip install pipenv`)

## Installation
1. Clone the project with the command:`git clone https://github.com/GitDrinou/DA_Python_P10_Softdesk_support.git`
2. Install dependencies with pipenv: `pipenv install`. This command will 
   create a virtual environment and install all dependencies listed in 
   **Pipfile**
3. Activate the virtual environment: `pipenv shell`
4. Apply database migrations: `python manage.py migrate`

## Running the API
Start the server: `python manage.py runserver`

The API will be available at: http://127.0.0.1:8000/
## Running test
To run all unit tests: `python manage.py test`

## Authentication
The API uses JWT (Json Web Token) authentication.

All protected routes require an: `Authorization Bearer Token`

### Main endpoints
#### Authentification
- `POST /api/token`: get an access token
- `POST /api/token/refresh`: refresh token
#### Users
- `GET /users`: get the list of users
- `GET /users/{id}`: get user detail
- `POST /users`: add a new user
- `PUT /users/{id}`: modify specific user datas
- `PATCH /users/{id}`: modify specific user data
- `DELETE /users/{id}`: delete a specific user
#### Projects
- `GET /projects`: get the list of projects
- `GET /projects/{id}`: get project detail
- `POST /projects`: add a new project
- `PUT /projects/{id}`: modify specific project datas
- `PATCH /projects/{id}`: modify specific project data
- `DELETE /projects/{id}`: delete a specific project
#### Contributors
- `GET /projects/{id}/contributors`: get the list of contributors
- `GET /projects/{id}/contributors/{id}`: get contributor detail
- `POST /projects{id}/contributors`: add a new contributor
- `DELETE /projects/{id}/contributors/{id}`: delete a specific contributor 
#### Issues
- `GET /projects/{id/issues`: get the list of issues
- `GET /projects/{id}/issues/{id}`: get issue detail
- `POST /projects/{id}/issues`: add a new issue
- `PUT /projects/{id}/issues/{id}`: modify specific issue datas
- `PATCH /projects/{id}/issues/{id}`: modify specific issue data
- `DELETE /projects/{id}/issues/{id}`: delete a specific issue
#### Comments
- `GET /projects/{id/issues/{id}/comments`: get the list of comments
- `GET /projects/{id}/issues/{id}/comments/{id}`: get comment detail
- `POST /projects/{id}/issues/{id}/comments`: add a new comment
- `PUT /projects/{id}/issues/{id}/comments/{id}`: modify specific comment datas
- `PATCH /projects/{id}/issues/{id}/comments/{id}`: modify specific comment data
- `DELETE /projects/{id}/issues/{id}/comments/{id}`: delete a specific comment
## API Testing
The API can be manually tested with Swagger UI.

The interactive documentation displays the list of requests to verify 
authentication, permissions, and core features.

If you don't have any account, you can create one on Postman, with the 
required datas on a JSON body, with this endpoint: `POST /users/`

To access to the documentation:
1. Launch the server on terminal `python manage.py runserver`
2. connect to the api at http://127.0.0.1:8000/api-auth/
3. generate a token with the `POST /api-token` endpoint
4. copy the 'access' value token on the response
5. click on the top "Authorize" button and paste the token value at the 
   "jwtAuth (http, Bearer)" section and authorize.

Now you can test the different endpoints with JWT.

![Swagger UI](docs/screenshot-api-docs.jpg)

## Code style and linting
This project follows the PEP8 coding style and uses flake8 as a linting tool 
to maintain code quality.

To launch and check the flake8 report:
1. open your terminal and go the application's root directory
2. execute the following command: 'flake8'

If the code is not valid, you will see a list of errors.

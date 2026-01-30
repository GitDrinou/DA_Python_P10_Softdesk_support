# Softdesk Support

## Version
1.0.0

## Overview
This project consists of building a secure RESTful API.

The API has been developed using Django REST Framework, following:
- OWASP security best pratices
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

Main endpoint:
- `POST /api/token`: to get an access token
- `POST /api/token/refresh`: refresh token

## API Testing
The API can be manually tested with Swagger UI.

The interactive documentation displays the list of requests to verify 
authentication, permissions, and core features.

To access to the documentation:
1. Launch the server on terminal `python manage.py runserver`
2. connect to the admin application at http://127.0.0.1:8000/admin/
3. open the documentation at http://127.0.0.1:8000/api/docs/

![Swagger UI](docs/screenshot-api-docs.jpg)

## Code style and linting
This project follows the PEP8 coding style and uses flake8 as a linting tool 
to maintain code quality.

To launch and check the flake8 report:
1. open your terminal and go the application's root directory
2. execute the following command: 'flake8'

If the code is not valid, you will see a list of errors.

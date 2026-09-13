# sweng861-crud-jcw5571
## Information

**Name:** Joshua Wendall

**Course Name:** SWENG 861 - Software Construction

## Project: Task Management Application

### Description 

A task managing application that will allow users to perform create, read, update, and delete tasks, persisting in a database. This project is to be developed incrementally through the course's weekly assignments.

### Technology Stack
 - Python
 - uv - Python project and dependency manager
 - FastAPI - backend web framework
 - Uvicorn - ASGI server
 - SQLAlchemy - ORM
 - SQLite - database
 - Pydantic - request and response validation
 - Authlib - OAuth2 and OpenID Connect client library
 - Google - OIDC provider
 - PyJWT - Application JWT authentication
 - Cohere API - third party API service for creating tasks from natural-language descriptions
 - mkcert - local development HTTPS certificates

### Project Structure
```
backend/
├── src/backend/
│   ├── ai/          # Cohere integration
│   ├── auth/        # Google OIDC and JWT authentication
│   ├── database/    # SQLAlchemy models and database connection
│   ├── events/      # Domain event definitions and handlers
│   └── tasks/       # Task API, schemas, and business logic
├── pyproject.toml
└── uv.lock
scripts/
└── generate_dev_cert.ps1
```

 ## Repository Cloning Instructions:
 Run the following command in the terminal:
 
 ```git clone https://github.com/psu-edu/sweng861-crud-jcw5571.git```

## Running the Application:
From the backend directory, start the FastAPI application using Uvicorn:

```uv run uvicorn backend.main:app```

The application will be available at:

```http://127.0.0.1:8000/```

With FastAPI's interactive documentation available at:

```http://127.0.0.1:8000/docs/```

If HTTPS is desired, run the ```generate_dev_cert.ps1``` script, found in ```scripts```, in Powershell. This will populate ```certs```. 

The run command for HTTPS after this is:

```uv run uvicorn backend.main:app --reload --ssl-certfile=../certs/localhost.pem --ssl-keyfile=../certs/localhost-key.pem```

And the application will be available at:

```https://127.0.0.1:8000/```

With FastAPI's interactive documentation available at:

```https://127.0.0.1:8000/docs/```

The HTTPS certificates are for local development; they are not production certificates.

## Environment Configuration

The application expects a ```.env``` file in the ```backend``` directory, containing secrets and other sensitive credentials. The current list of expected values is:
- Google OAuth client ID
- Google OAuth client secret
- Session secret
- JWT secret
- Cohere trial API key (free with any account upon writing)

  
## Authentication Strategy

For authentication, Option A: Social Login was implemented using Authlib and Google OIDC, both for its ability to meet modern security standards and as a better example for my eventual project of choice, that being the Campus Scheduler. Being a simple, student facing tool, and with Google Calendar integration being planned, using Google as an identity provider provided both a valuable learning experience of implementing external OIDC and served as a basis for the expected needs of my capstone project. Being a widely used industry standard, Google's OIDC implementation is well documented and supported, and widely utilized, making the knowledge of its implementation a valuable asset for future development endeavors.

As for the setup, as mentioned previously, Google is used as the identity provider. Authlib handles the OAuth2/OIDC protocol, accepting the Google provided credentials and user info. SQLAlchemy is used to interact with the SQLite database, storing an application-specific user ID, tied to the Google's stable user ID. Parameters like email and name are stored, but not checked for authentication. Metrics like time created, last login, and last updated are also stored. After authentication, the application establishes an authenticated session using a signed session cookie. Starlette, through FastAPI, is used for middleware, storing the OAuth state between the login redirect and callback.

```GET /api/hello``` and ```GET /api/me``` were protected using a reusable ```require_auth``` dependency, reading the authenticated stored user ID from the session, retrieves the corresponding local user from the database, rejecting the request with a **401 Unauthorized** response if no user is found. 

To establish a JWT token system, another layer was added to authentication. Upon authentication from Google OIDC, the client can then request a JWT token, which is then required to access the task endpoints. JWT tokens are signed using the applications JWT secret and expire after one hour.

**OWASP API Security Practices Employed:**
- Broken Object Level Authorization (BOLA): protected endpoints derive the current user's data from the authenticated session. 
- Avoid Excessive Data Exposure: API responses expose only the information required by the client, not returning full database entries or sensitive authentication data.
- Avoid Security Misconfiguration: Upon denied calls, the application only returns ```401 Unauthorized``` to the client. 

### Authentication Flow
1. The user selects Log in with Google from the application.
2. The backend redirects the user to Google's authorization endpoint.
3. Google authenticates the user and redirects the browser to /auth/callback.
4. The backend exchanges the authorization code for tokens and obtains the user's OIDC identity information.
5. The backend creates a new local user or updates the existing user's information.
6. The local user ID is stored in the authenticated session.
7. The user is redirected back to the application.
8. Protected API endpoints use the authenticated session to identify the current user.

Flow: Client → Login → Google IdP → Callback → Backend → Session → Protected API

JWT Flow: Client → Login → Google IdP → Callback → Backend → Request token → JWT token issued → Protected API

## Task Management API

The primary API is located under ```/api/tasks```

All endpoints require a valid JWT. 

### Create a Task

```POST /api/tasks``` creates a task for an authenticated user. 
 
 Format:
 
 ```
{
  "title": "string",
  "description": "string",
  "status": "enum",
  "priority": "enum",
  "due_date": datetime
}
```

```"status"``` only accepts ```"pending"``` (default) or ```completed```

```"priority"``` only accepts ```"low"```, ```"medium"``` (default), or ```"high"```

### Cohere Integration for Creating Tasks

```POST /api/tasks/from-description``` utilizes Cohere's API endpoint to generate a structured JSON, containing the appropriate fields, from a natural-language description. 
Format:

```
{
  "description": "string"
}
```

The data is validated using the same ```TaskCreate``` schema as the other ```POST``` method before the task is created. 

### Get All Tasks

```GET /api/tasks``` returns all of the tasks belonging to the authenticated user. 

### Get a Task

```GET /api/tasks/{task_id}``` returns the specified task, so long as it belongs to the authenticated user.

### Update a Task

```PUT /api/tasks/{task_id}``` updates the included fields in the specified task, so long as it belongs to the authenticated user. An empty request is rejected.

### Delete a Task

```DELETE /api/tasks/{task_id}``` deletes the specified task, so long as it belongs to the authenticated user. 

## Domain Events

Domain events are emitted upon important task changes. This includes task creation, updating, and deletion. Events are handled asynchronously by the application's event-handling layer and are currently used for logging and demonstrating event-driven behavior.

# sweng861-crud-jcw5571
## Information

**Name:** Joshua Wendall

**Course Name:** SWENG 861 - Software Construction

## Project: CRUD Application

**Description:** A simple CRUD application that will allow users to perform create, read, update, and delete operations on a database. This project is to be developed incrementally through the course's weekly assignments. Current functionality includes backend API and authentication using Google OIDC, with a backend database for persisting user data.

**Technology Stack:**
 - Python
 - uv - Python project and dependency manager
 - FastAPI - backend web framework
 - Uvicorn - ASGI server
 - SQLAlchemy - ORM
 - SQLite - database
 - Authlib - OAuth2 and OpenID Connect client library
 - Google - OIDC provider

 ## Repository Cloning Instructions:
 Run the following command in the terminal:
 
 ```git clone https://github.com/psu-edu/sweng861-crud-jcw5571.git```

## Running the Application:
From the backend directory, start the FastAPI application using Uvicorn:

```uv run uvicorn backend.main:app```

The application will be available at:

```http://127.0.0.1:8000```

See ```README.md``` in ```backend``` for additional information.

## Authentication Strategy

For authentication, Option A: Social Login was implemented using Authlib and Google OIDC, both for its ability to meet modern security standards and as a better example for my eventual project of choice, that being the Campus Scheduler. Being a simple, student facing tool, and with Google Calendar integration being planned, using Google as an identity provider provided both a valuable learning experience of implementing external OIDC and served as a basis for the expected needs of my capstone project. Being a widely used industry standard, Google's OIDC implementation is well documented and supported, and widely utilized, making the knowledge of its implementation a valuable asset for future development endeavors.

As for the setup, as mentioned previously, Google is used as the identity provider. Authlib handles the OAuth2/OIDC protocol, accepting the Google provided credentials and user info. SQLAlchemy is used to interact with the SQLite database, storing an application-specific user ID, tied to the Google's stable user ID. Parameters like email and name are stored, but not checked for authentication. Metrics like time created, last login, and last updated are also stored. After authentication, the application establishes an authenticated session using a signed session cookie. Starlette, through FastAPI, is used for middleware, storing the OAuth state between the login redirect and callback.

```GET /api/hello``` and ```GET /api/me``` were protected using a reusable ```require_auth``` dependency, reading the authenticated stored user ID from the session, retrieves the corresponding local user from the database, rejecting the request with a **401 Unauthorized** response if no user is found. 

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
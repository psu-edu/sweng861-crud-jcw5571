# sweng861-crud-jcw5571
## Information

**Name:** Joshua Wendall

**Course Name:** SWENG 861 - Software Construction

## Project: Project S - Campus Scheduler (Appointments)

**Description:** The Campus Scheduler will be an appointment system for scheduling office hours and advising appointments.
 - Two authenticated roles: Professor (sets availability) and Student (books appointments).
 - Key Workflow: "Book Office Hours" (Check Calendar → Lock Slot → Send Invite).

**Technology Stack:**
 - Python
 - uv - Python project and dependency manager
 - FastAPI - backend web framework
 - Uvicorn - ASGI server to run FastAPI application
 - Google Calendar API - external calendar integration (in progress)

 ## Cloning Instructions:
 Run the following command in the terminal:
 
 ```git clone https://github.com/psu-edu/sweng861-crud-jcw5571.git```

## Running the Backend:
From the backend directory, start the FastAPI application using Uvicorn:

```uv run uvicorn backend.main:app```

The API will be available at:

```http://127.0.0.1:8000```

See ```README.md``` in ```backend``` for additional information.

# Backend


## **Technologies:**
- Python 3.14
- FastAPI: web framework used to build the API
- Uvicorn: web server used to run the FastAPI application
- uv: Python project and dependency management


## **Commands:**

From the backend directory, run:

```uv run uvicorn backend.main:app```

The API will be available at:

http://127.0.0.1:8000


Health-check endpoint:

GET /health
Example: ```curl.exe http://127.0.0.1:8000/health```

Returns:
{
    "status": "ok"
}



Interactive API documentation (FastAPI) available:

http://127.0.0.1:8000/docs

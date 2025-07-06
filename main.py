import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI
from src.routers import data_handler
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="CAG Project API Chat with Your PDF",
    description="API for chatting with PDFs, querying content via LLM and managing data.",
    version="1.0.0"
)

app.include_router(
    data_handler.router,
    prefix="/api/v1",
    tags=["Data Handling and Chat with PDF"],
)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    """
    Provides a simple HTML welcome page with a link to the API documentation.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to CAG Project API</title>
        <style>
            body {font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;}
            .container {max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);}
            h1 {color: #333;}
            a {color: #007BFF; text-decoration: none;}
            a:hover {text-decoration: underline;}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to CAG Project API</h1>
            <p>View the automatically generated API documentation here:</p>
            <p><a href="/docs" target="_blank">Swagger UI (OpenAPI docs)</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    # You can test tools like curl or Postman to interact with the API
    uvicorn.run(
        app, host="127.0.0.1", port=8000
    ) #Using different port to avoid conflicts with other services

    # Please set it to your google gemini key (get key from https://aistudio.google.com/)
"""Main FastAPI application entrypoint for NainProspect Gateway."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.nainprospect.api.routes import router

app = FastAPI(
    title="NainProspect — B2B Prospecting & Compliance Gateway",
    description=(
        "Autonomous B2B prospect sourcing, AI enrichment, and compliance verification engine. "
        "Enforces GDPR Article 6.1.f and Spanish LSSI-CE Article 21 compliance gates."
    ),
    version="1.0.0",
    docs_url=None,  # Disabled default Swagger in favor of Scalar reference
    redoc_url=None,
)

# CORS configuration for Vue SPA and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5377",
        "http://127.0.0.1:5377",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://prospect.naindev.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Liveness probe returning application operational status."""
    return {"status": "healthy", "service": "NainProspect Gateway", "version": "1.0.0"}


@app.get("/health/ready", tags=["Health"])
def readiness_check() -> dict:
    """Readiness probe indicating service is ready to accept prospecting traffic."""
    return {"status": "ready", "service": "NainProspect Gateway"}


@app.get("/docs", include_in_schema=False)
def scalar_api_reference() -> HTMLResponse:
    """Interactive OpenAPI documentation powered by Scalar."""
    html_content = """
    <!doctype html>
    <html>
      <head>
        <title>NainProspect API Reference</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          body { margin: 0; background-color: #0b0f19; }
        </style>
      </head>
      <body>
        <script
          id="api-reference"
          data-url="/openapi.json"
          data-configuration='{"theme": "deepSpace"}'
          src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.nainprospect.main:app", host="0.0.0.0", port=8106, reload=True)

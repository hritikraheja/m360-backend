# m360-backend

FastAPI wrapper over Quran Foundation APIs with OAuth2 authentication.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Setup

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   
   Create a `.env` file (or `.env.local`, `.env.dev`, `.env.preprod`, `.env.prod`) in the root directory with the following required variables:
   ```
   QURAN_CLIENT_ID=your_client_id
   QURAN_CLIENT_SECRET=your_client_secret
   QURAN_BASE_URL=your_base_url
   QURAN_OAUTH_URL=your_oauth_url
   ```
   
   You can also set the `APP_ENV` environment variable to explicitly specify which environment file to use:
   - `local` → `.env.local`
   - `dev` → `.env.dev`
   - `preprod` → `.env.preprod`
   - `prod` → `.env.prod`

## Starting the Service

### Option 1: Using uvicorn directly

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

### Option 2: Using Python module

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using Docker

```bash
docker build -t m360-backend .
docker run -p 8000:8000 m360-backend
```

## Accessing the Service

Once started, the service will be available at:
- **API**: http://localhost:8000
- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

## Health Check

Check if the service is running:
```bash
curl http://localhost:8000/health
```
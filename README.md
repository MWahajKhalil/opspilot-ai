# OpsPilot AI

OpsPilot AI is a growing industrial operations and device-reliability platform. The current version provides a structured FastAPI backend for registering, listing, filtering, and retrieving devices, plus an experimental temperature endpoint that calls an external HTTP service. Future checkpoints will expand the same project with persistent storage, simulated telemetry, operational alerts, AI-assisted investigations, and production infrastructure.

> **Current scope:** The Module 9 Device API and the core CP2A layered-backend exercise are implemented. The temperature endpoint requires a separate provider at `http://localhost:9000`; this repository does not supply one. Tests simulate that provider without live network access. Later capabilities listed in the roadmap are planned, not implemented.

## Current features

- FastAPI application with lifespan startup and shutdown handling
- Layered application structure using API, schema, service, repository, external-client, and dependency modules
- Pydantic request and response validation
- Device collection endpoint with optional status filtering
- Individual device lookup using a path parameter
- Device creation using a JSON request body
- Explicit `200`, `201`, `404`, and `422` HTTP behavior
- Dependency injection with FastAPI `Depends()`
- External temperature lookup for an existing device, with upstream HTTP/request failures translated to `503`
- Automated API tests using pytest and FastAPI `TestClient`
- Interactive OpenAPI documentation provided by FastAPI

## Architecture

```text
HTTP request
    ↓
FastAPI router          app/api/
    ↓
Dependency providers    app/dependencies.py
    ↓
Device service          app/services/
    ├── In-memory repository    app/repositories/
    └── Temperature client      app/clients/ → external HTTP service
    ↓
Pydantic response       app/schemas/
```

The dependency providers in `app/dependencies.py` connect the repository, HTTP client, temperature client, and device service. The service checks that a device exists before requesting its temperature. Tests override the repository and HTTP client to use fresh in-memory data and a fake external response.

## Project structure

```text
opspilot-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── device.py
│   │   ├── schemas/
│   │   │   ├── device.py
│   │   │   └── telemetry.py
│   │   ├── services/
│   │   │   └── device.py
│   │   ├── repositories/
│   │   │   └── device.py
│   │   ├── clients/
│   │   │   └── temperature.py
│   │   ├── errors/
│   │   │   ├── device.py
│   │   │   └── temperature.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_devices.py
│   ├── requirements.txt
│   └── requirements-dev.txt
├── design/
│   └── concepts/
└── README.md
```

## API endpoints

| Method | Endpoint | Purpose | Successful status |
| --- | --- | --- | --- |
| `GET` | `/health` | Check whether the API is running | `200` |
| `GET` | `/devices` | List all devices | `200` |
| `GET` | `/devices?status=warning` | Filter devices by status | `200` |
| `GET` | `/devices/{device_id}` | Retrieve one device | `200` |
| `POST` | `/devices` | Create a device | `201` |
| `GET` | `/devices/{device_id}/temperature` | Request temperature from the configured external service | `200` |

A request for an unknown local device returns `404`. Invalid path parameters or request bodies return `422` through FastAPI and Pydantic validation. If the external temperature service returns an HTTP error or its request fails, the temperature endpoint returns `503`.

## Run locally

### 1. Create and activate a virtual environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install the application dependencies

```bash
python -m pip install -r backend/requirements.txt
```

### 3. Start the API

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Example request

Create a device:

```bash
curl -X POST http://127.0.0.1:8000/devices \
  -H "Content-Type: application/json" \
  -d '{"name":"Pump-17","status":"ok"}'
```

Example response:

```json
{
  "id": 3,
  "name": "Pump-17",
  "status": "ok"
}
```

## Run the tests

Install the development dependencies from the repository root:

```bash
python -m pip install -r backend/requirements-dev.txt
```

Then run the test suite:

```bash
cd backend
python -m pytest -v
```

The current suite contains twelve tests covering the Device API, repository creation, temperature success, and upstream HTTP-error translation. The temperature tests use a fake HTTP transport and do not need the external service running.

## Current limitations

- Device data is stored only in memory.
- Data resets when the application restarts.
- Device statuses are currently plain strings.
- Authentication and authorization are not implemented.
- No temperature provider or simulator is included; the configured `localhost:9000` endpoint is only an integration target.
- Timeout translation is implemented through HTTPX request-error handling, but has no dedicated timeout test.
- Invalid JSON or schema-invalid provider responses are not yet translated to a stable application error.
- The shared HTTP client is created at module import and is not yet closed through application lifespan.

## Planned growth

The project is intended to grow incrementally as each supporting technology is introduced:

1. PostgreSQL, SQLAlchemy, migrations, and data workflows
2. Next.js and TypeScript operations dashboard
3. Simulated device events, MQTT, Redis, and background processing
4. Rule-based alerts followed by optional ML anomaly detection
5. RAG over equipment manuals and troubleshooting documents
6. Agent-based investigation workflows
7. MCP diagnostic tools with human approval boundaries
8. AI evaluation and expanded automated testing
9. Docker, CI/CD, cloud deployment, and observability

Physical hardware is not required. Device and telemetry behavior can be simulated in software; hardware integration can be added later as an optional extension.

## Design concepts

Early product concepts are available in [`design/concepts`](design/concepts). They illustrate the intended direction and do not represent implemented frontend functionality.

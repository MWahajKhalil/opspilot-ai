# OpsPilot AI

OpsPilot AI is a growing industrial operations and device-reliability platform. The current version provides a structured FastAPI backend for registering, listing, filtering, and retrieving devices. Future checkpoints will expand the same project with persistent storage, simulated telemetry, operational alerts, AI-assisted investigations, and production infrastructure.

> **Current scope:** Module 9 establishes the FastAPI application structure and an in-memory Device API. Later capabilities listed in the roadmap are planned and are not implemented yet.

## Current features

- FastAPI application with lifespan startup and shutdown handling
- Layered application structure using API, schema, service, and dependency modules
- Pydantic request and response validation
- Device collection endpoint with optional status filtering
- Individual device lookup using a path parameter
- Device creation using a JSON request body
- Explicit `200`, `201`, `404`, and `422` HTTP behavior
- Dependency injection with FastAPI `Depends()`
- Automated API tests using pytest and FastAPI `TestClient`
- Interactive OpenAPI documentation provided by FastAPI

## Architecture

```text
HTTP request
    ↓
FastAPI router          app/api/
    ↓
Pydantic schemas        app/schemas/
    ↓
Device service          app/services/
    ↓
In-memory device list
```

The dependency provider in `app/dependencies.py` supplies the shared `DeviceService` instance to the routes. This keeps HTTP handling separate from device-related business logic and allows tests to replace the dependency with an isolated service instance.

## Project structure

```text
opspilot-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── device.py
│   │   ├── schemas/
│   │   │   └── device.py
│   │   ├── services/
│   │   │   └── device.py
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

A request for an unknown device returns `404`. Invalid path parameters or request bodies return `422` through FastAPI and Pydantic validation.

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

The current suite contains nine API tests covering health, listing, query filtering, device lookup, device creation, persistence within a service instance, and validation/error responses.

## Current limitations

- Device data is stored only in memory.
- Data resets when the application restarts.
- Device statuses are currently plain strings.
- Authentication and authorization are not implemented.
- No real or simulated telemetry is connected yet.

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

# OpsPilot AI

OpsPilot AI is an evolving industrial-operations backend focused on device reliability and safe operational workflows. The current FastAPI implementation demonstrates layered application architecture, an asynchronous external-service boundary, API-key protection, validated device actions, and approval-required behavior for risky commands.

> **Current scope:** This repository contains an in-memory backend and automated tests. It does not include physical-device control, a live temperature provider, a database, frontend, AI, RAG, or MCP features. Those capabilities remain planned work.

## Implemented features

- FastAPI application with lifespan-managed startup and shutdown
- Shared asynchronous `httpx.AsyncClient` with explicit connect/total timeouts
- Layered API, schema, service, repository, external-client, and dependency modules
- Pydantic request, response, enum, and external-response validation
- Device listing, filtering, lookup, and creation
- External temperature lookup with safe timeout, upstream HTTP, malformed JSON, and invalid-schema handling
- Router-level `X-API-Key` protection for all `/devices...` endpoints
- Public `/health` endpoint
- Environment-configured expected API key with constant-time comparison
- Allow-listed device actions: `inspect`, `restart`, and `shutdown`
- Approval-required decisions for risky `restart` and `shutdown` requests
- Safe logging that omits API keys, authorization headers, and raw provider bodies
- Integration-style tests using FastAPI `TestClient`, dependency overrides, and `httpx.MockTransport`

## Architecture

```text
HTTP request
    ↓
API-key dependency       app/security.py
    ↓
FastAPI + Pydantic       app/api/ + app/schemas/
    ↓
Dependency providers     app/dependencies.py
    ↓
DeviceService            app/services/
    ├── DeviceRepository     app/repositories/
    └── TemperatureClient    app/clients/ → controlled external HTTP
```

The service coordinates application rules. The repository owns in-memory device data. The external client owns HTTP mechanics and validates provider responses. Routes translate known application failures into stable HTTP responses.

## Project structure

```text
opspilot-ai/
├── backend/
│   ├── app/
│   │   ├── api/device.py
│   │   ├── clients/temperature.py
│   │   ├── errors/
│   │   ├── repositories/device.py
│   │   ├── schemas/
│   │   │   ├── action.py
│   │   │   ├── device.py
│   │   │   └── telemetry.py
│   │   ├── services/device.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── security.py
│   ├── tests/test_devices.py
│   ├── requirements.txt
│   └── requirements-dev.txt
├── design/concepts/
└── README.md
```

## API endpoints

| Method | Endpoint | Authentication | Purpose | Success |
| --- | --- | --- | --- | --- |
| `GET` | `/health` | Public | Application health | `200` |
| `GET` | `/devices` | API key | List/filter devices | `200` |
| `GET` | `/devices/{device_id}` | API key | Retrieve one device | `200` |
| `POST` | `/devices` | API key | Create a device | `201` |
| `GET` | `/devices/{device_id}/temperature` | API key | Retrieve validated external temperature data | `200` |
| `POST` | `/devices/{device_id}/actions` | API key | Validate an action and apply approval policy | `202` |

Expected errors include `401` for missing/incorrect caller credentials, `404` for a missing device, automatic `422` request-validation responses, and safe `503` responses for missing server authentication configuration or temperature-provider failures.

## Run locally

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Start the API with a development API key:

```bash
cd backend
OPSPILOT_API_KEY=replace-with-a-development-key \
  python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

Except for `/health`, requests must include:

```text
X-API-Key: replace-with-a-development-key
```

Do not commit real credentials. Set `OPSPILOT_API_KEY` through the runtime environment or a deployment secret manager.

## Example action request

```bash
curl -X POST http://127.0.0.1:8000/devices/1/actions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: replace-with-a-development-key" \
  -d '{"action":"restart"}'
```

Example response:

```json
{
  "device_id": 1,
  "action": "restart",
  "status": "approval_required"
}
```

The status is a policy decision, not evidence that a physical command was executed.

## Run tests

Install development dependencies and run the suite:

```bash
python -m pip install -r backend/requirements-dev.txt
cd backend
python -m pytest -q
```

Latest verified result: **20 passed**.

Tests use fresh repository state and fake outbound HTTP transport. No live provider or internet connection is required.

## Security and safety decisions

- The expected API key is read from `OPSPILOT_API_KEY`; it is not hardcoded.
- Caller credentials arrive only through `X-API-Key`.
- Authentication logs never contain the supplied or expected key.
- Only enum-defined actions enter business logic.
- `restart` and `shutdown` stop at `approval_required`.
- `accepted` is used instead of `executed` because no device-command integration exists.
- Unexpected internal exception details are not intentionally returned to callers.

The API-key mechanism is suitable for demonstrating a service boundary, not a complete production identity system. A production deployment would require stronger identity, authorization, key rotation, rate limiting, audit records, and deployment-specific controls.

## Current limitations

- Device data is stored only in memory and resets on restart.
- Device status values are still plain strings.
- No live temperature provider is included; `http://localhost:9000` is an integration target used with a fake transport in tests.
- No approver identity, persisted approval request, approval endpoint, or audit database exists.
- No real device-command client exists; actions are validated but not physically executed.
- Logs are emitted to the runtime logging stream and are not shipped to persistent observability storage.
- No frontend, database, IoT broker, AI/RAG/agent/MCP, deployment, or cloud infrastructure is implemented yet.

## Planned growth

1. PostgreSQL, SQLAlchemy, migrations, and persistent action/approval records
2. Next.js and TypeScript operations dashboard
3. Simulated telemetry, MQTT, Redis, and background processing
4. Rule-based alerts followed by optional anomaly detection
5. RAG over equipment manuals and troubleshooting documents
6. Agent-based investigation workflows with explicit human approval
7. MCP diagnostic tools with constrained permissions
8. AI evaluation and expanded automated testing
9. Docker, CI/CD, deployment, and observability

Physical hardware is optional. Device and telemetry behavior can be simulated until a real integration and its safety requirements are explicitly defined.

## Design concepts

Concept diagrams are available in [`design/concepts`](design/concepts). They document architecture and intended product direction; product mockups do not imply implemented frontend functionality.

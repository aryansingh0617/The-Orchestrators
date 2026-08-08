# Chimera Backend

FastAPI backend for Project Chimera.

Milestone 3 establishes the backend architecture foundation only:

- FastAPI application shell
- typed settings
- domain model foundations
- application service contracts
- provider abstraction
- deterministic stub provider
- dependency injection boundaries
- structured error handling
- health endpoint
- backend tests

The full assessment engines, database persistence, and production AI providers are implemented in later milestones.

## Local Commands

```bash
python -m pytest backend/tests
python -m uvicorn app.main:app --app-dir backend --reload
```


# Database Migrations

## Tooling

Chimera uses Alembic with SQLAlchemy models under `backend/app/infrastructure/database/`.

- Config: `backend/alembic.ini`
- Environment: `backend/migrations/env.py`
- Revisions: `backend/migrations/versions/`

Repositories are unchanged. Alembic owns schema evolution; application repositories continue to implement domain interfaces.

## Fresh database bootstrap

From `backend/`:

```bash
# optional: point alembic at a fresh sqlite file
# edit sqlalchemy.url in alembic.ini or export for your environment

python -m alembic upgrade head
uvicorn app.main:app --reload
```

For automated tests, the app uses in-memory repositories when `CHIMERA_ENVIRONMENT=test`.

## Common commands

```bash
python -m alembic current
python -m alembic history
python -m alembic upgrade head
python -m alembic downgrade -1
```

## Notes

- Initial revision `1969bf990e87` creates the full Chimera assessment schema.
- Do not commit production database files or secrets.
- `Base.metadata.create_all` remains a local development fallback in `create_app`, but migrations are the supported path for clean environments.

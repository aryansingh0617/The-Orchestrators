# Folder Structure

## Root Layout

```text
.
├── backend/
├── frontend/
├── docs/
├── scripts/
├── tests/
├── .editorconfig
├── .env.example
├── .gitignore
└── README.md
```

## Backend Target Layout

```text
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── errors.py
│   │   └── routes/
│   ├── application/
│   │   ├── commands/
│   │   ├── services/
│   │   └── use_cases/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── events/
│   │   └── interfaces/
│   ├── infrastructure/
│   │   ├── ai/
│   │   ├── database/
│   │   ├── repositories/
│   │   └── observability/
│   ├── modules/
│   │   ├── curriculum_analyzer/
│   │   ├── candidate_analyzer/
│   │   ├── interview_planner/
│   │   ├── mission_generator/
│   │   ├── world_state_engine/
│   │   ├── memory_engine/
│   │   ├── adaptive_difficulty_engine/
│   │   ├── evidence_collector/
│   │   ├── evaluation_engine/
│   │   ├── engineering_profile_generator/
│   │   ├── hiring_recommendation_engine/
│   │   └── feedback_generator/
│   ├── schemas/
│   ├── settings.py
│   └── main.py
├── migrations/
├── tests/
└── pyproject.toml
```

## Frontend Target Layout

```text
frontend/
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   ├── sessions/
│   └── reports/
├── components/
│   ├── ui/
│   ├── assessment/
│   ├── missions/
│   ├── evidence/
│   └── reports/
├── lib/
│   ├── api/
│   ├── types/
│   └── utils/
├── hooks/
├── tests/
├── next.config.ts
├── package.json
└── tsconfig.json
```

## Docs Layout

```text
docs/
├── PRODUCT_VISION.md
├── ARCHITECTURE.md
├── SYSTEM_DESIGN.md
├── IMPLEMENTATION_PLAN.md
├── DATABASE_SCHEMA.md
├── API_SPEC.md
├── PROMPT_ARCHITECTURE.md
├── FOLDER_STRUCTURE.md
├── TESTING_STRATEGY.md
├── GIT_WORKFLOW.md
├── RISKS.md
├── DEMO_SCRIPT.md
└── README.md
```

## Module Layout

Each backend module follows:

```text
module_name/
├── contract.py
├── service.py
├── schemas.py
├── prompts.py
├── errors.py
└── README.md
```

Required module docs:

- purpose
- inputs
- outputs
- error handling
- test cases
- prompt IDs if AI-backed

## Tests Layout

```text
tests/
├── fixtures/
├── integration/
└── e2e/
```

Backend tests live near backend code when they are package-specific. Cross-project tests live in root `tests/`.

## Naming Conventions

- Python packages: `snake_case`
- TypeScript components: `PascalCase`
- API routes: plural nouns
- database tables: plural `snake_case`
- prompt IDs: `module.action.version`
- branches: `type/milestone-description`

## Boundary Rules

- `backend/app/domain` cannot import `backend/app/api` or `backend/app/infrastructure`.
- `backend/app/application` cannot import FastAPI route modules.
- `backend/app/modules/*` expose contracts and services, not HTTP handlers.
- `frontend/components/ui` contains reusable primitives only.
- `frontend/lib/api` is the only frontend layer that knows raw endpoint paths.


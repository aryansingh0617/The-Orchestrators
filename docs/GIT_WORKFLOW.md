# Git Workflow

## Branching Model

Work is done on milestone branches.

Branch format:

- `chore/milestone-1-scaffolding`
- `docs/milestone-2-engineering-documentation`
- `feat/planner-adaptive-interview-planner`
- `feat/world-dynamic-interview-state`
- `test/core-integration-coverage`

Default branch:

- `main`

Rules:

- Do not overwrite remote history.
- Do not commit unrelated changes.
- Do not use broad staging commands for mixed worktrees.
- Preserve user changes.
- Push milestone branches for review.

## Milestone Workflow

Every milestone follows:

1. Design
2. Review
3. Refine
4. Implement
5. Test
6. Refactor
7. Document
8. Commit
9. Stop

## Commit Rules

Use Conventional Commits.

Examples:

- `chore(repo): scaffold project repository`
- `docs: define assessment operating system architecture`
- `feat(planner): implement adaptive interview planner`
- `feat(memory): add reasoning memory engine`
- `feat(world): implement dynamic interview state`
- `feat(eval): add evidence-based evaluation`
- `feat(api): implement assessment endpoints`
- `feat(ui): integrate mission dashboard`
- `test(core): planner integration tests`

## Staging Rules

Before committing:

1. Run `git status --short --branch`.
2. Review unstaged changes.
3. Stage only files that belong to the milestone.
4. Run `git diff --cached --stat`.
5. Run `git diff --cached` when the change is small enough to inspect directly.

Avoid:

- `git add -A`
- `git add .`
- `git reset --hard`
- force push unless explicitly approved and justified

## Push Rules

Push only after:

- tests/builds pass or documented exception is explained
- staged scope is confirmed
- commit message is clean
- remote branch target is known

Milestone branches should be pushed with upstream tracking:

```bash
git push -u origin <branch-name>
```

## Pull Request Rules

When creating a PR:

- target `main` unless a milestone dependency branch is required
- explain milestone scope
- list tests run
- mark as draft unless explicitly ready
- link prior milestone branch when dependent

## Release Readiness

A release candidate requires:

- all milestone branches merged
- full test suite passing
- frontend production build passing
- backend health check passing
- demo script verified
- deployment configuration documented


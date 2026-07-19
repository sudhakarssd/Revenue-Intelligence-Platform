# Workspace Rules - Revenue Intelligence Platform

This repository follows standard conventions to maintain high code quality and clean architecture:

## 1. Architecture Decision Records (ADRs)
- Every merge or significant design decision must be accompanied by an ADR written in Markdown under the `docs/adr/` directory.

## 2. Commit Message Conventions
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format for all git commits:
  - `feat:` for new platform features.
  - `fix:` for bug fixes.
  - `refactor:` for codebase refactorings.
  - `test:` for writing tests.
  - `docs:` for documentation updates.

## 3. Unit Test Coverage
- Maintain **>80%** unit test coverage for the AI Platform module (`app/ai`).
- Run coverage checks using:
  ```bash
  .venv/Scripts/pytest --cov=app/ai --cov-report=term-missing
  ```

## 4. Coding Style and Documentation
- Every public class, function, and method must include explicit Python type hints.
- Write concise docstrings for all public interfaces.

## 5. Dependency Direction
- Business modules must never depend on provider SDKs.
- Allowed dependency flow:
  ```text
  API (or Business Module)
          │
          ▼
     AI Gateway
          │
          ▼
    Policy Engine
          │
          ▼
     Model Router
          │
          ▼
   Provider Factory
          │
          ▼
     AI Provider
  ```

## 6. Platform Ownership
- Only provider adapters may reference provider SDK request/response models.
- All other layers must use platform-owned contracts.


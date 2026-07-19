# ADR 0001: Task-Based AI Gateway and Clean Architecture Routing

## Status

Accepted

## Context

The **Revenue Intelligence Platform** requires a design that can service several business operations (such as Summarization, Opportunity Analytics, and Conversational Assistants) while maintaining provider independence. Directly referencing provider SDKs (like OpenAI, Anthropic, or Gemini) inside API controllers or business logic modules creates high coupling and makes migrating between models or configurations complex and error-prone.

## Decision

We have established a Clean Architecture decoupling strategy with the following patterns:

1. **Platform-Owned Contracts**:
   - Business modules interact exclusively with task-driven, platform-owned schemas (`AIRequest`, `AIResponse`, `Message`, `TokenUsage`, `ProviderInfo`) instead of provider-specific types.
   
2. **Task-Based Model Routing**:
   - Clients request tasks (e.g. `summarize`, `analyze`) rather than specifying model versions directly. 
   - A `ModelRouter` maps tasks to mapped provider/model pairs, hiding the model configurations from the business applications.

3. **Isolated Adapters and Factories**:
   - All provider integrations inherit from `BaseAIProvider`. The `ProviderFactory` handles instantiation and adapter lifecycle management. Only the provider adapter classes are allowed to import model SDKs.

4. **Structured Pipeline Orchestration**:
   - The `AIGateway` acts as the single coordinator following the execution path: 
     `AIRequest` → `Policy Engine` → `Model Router` → `Provider Factory` → `AI Provider` → `AIResponse`.

5. **Lazy Dependency Injection**:
   - FastAPI dependencies are resolved lazily (`get_gateway()`) to support mock injections during unit and integration test runs.

## Consequences

### Positive
- **Provider Independence**: Swapping model vendors (e.g., from OpenAI to Claude) only requires editing the routing configuration or implementing a new `BaseAIProvider` subclass, with no changes to business APIs.
- **Improved Testability**: We can easily mock provider adapters for unit tests without hitting external API endpoints.
- **Maintainability**: Clear separation of concerns, concrete type hints, and decoupled schemas keep the project flexible.

### Negative
- **Abstraction Overhead**: Converting request and response structures between the platform contract and provider SDK structures adds small translation steps.

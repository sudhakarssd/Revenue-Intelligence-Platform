# System Architecture

The Revenue Intelligence Platform is designed with a Clean Architecture approach to separate business logic from technical implementations:

- **Contracts Layer (`app/ai/contracts/`)**: Declares task-driven, platform-owned schemas (`AIRequest`, `AIResponse`, `Message`, `TokenUsage`) to decouple business code from specific provider formats.
- **Policy Layer (`app/ai/policies/`)**: Pre-evaluates incoming requests for constraints and safety checks prior to model execution.
- **Router Layer (`app/ai/routing/`)**: Automatically resolves task types to mapped providers and target models based on routing tables.
- **Provider Layer (`app/ai/providers/`)**: Standardizes integrations with external model vendors. The `ProviderFactory` caches and retrieves instances of providers implementing the `BaseAIProvider` interface.
- **Gateway Layer (`app/ai/gateway/`)**: Directs the flow of execution: Evaluates Policy → Routes Task → Resolves Provider Adapter → Executes and Logs Telemetry.
- **Telemetry Layer (`app/ai/telemetry/`)**: Captures latency, transaction trace IDs, and token usage metrics.
- **API Layer (`app/api/`)**: Declares FastAPI routes and exposes a centralized dependency injection provider.
- **Shared Layer (`app/shared/`)**: Houses enums, defaults, constants, and logging wrappers.

from app.ai.gateway.gateway import AIGateway
from app.ai.policies.default_policy import DefaultPolicy
from app.ai.routing.router import ModelRouter
from app.ai.providers.factory import ProviderFactory
from app.ai.telemetry.tracker import TelemetryTracker
from app.infrastructure.config import settings


_gateway_instance = None


def get_gateway() -> AIGateway:
    """Dependency injection provider supplying the configured AIGateway instance."""
    global _gateway_instance
    if _gateway_instance is None:
        _policy_engine = DefaultPolicy()
        _model_router = ModelRouter(
            default_provider=settings.default_provider,
            default_model=settings.default_model
        )
        _provider_factory = ProviderFactory(settings_obj=settings)
        _telemetry_tracker = TelemetryTracker()

        _gateway_instance = AIGateway(
            policy_engine=_policy_engine,
            router=_model_router,
            provider_factory=_provider_factory,
            telemetry_tracker=_telemetry_tracker
        )
    return _gateway_instance

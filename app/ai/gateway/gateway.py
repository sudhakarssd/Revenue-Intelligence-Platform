from app.ai.contracts import AIRequest, AIResponse
from app.ai.policies.default_policy import DefaultPolicy
from app.ai.routing.router import ModelRouter
from app.ai.providers.factory import ProviderFactory
from app.ai.telemetry.tracker import TelemetryTracker
from app.ai.exceptions.exceptions import ModelRouteException


class AIGateway:
    def __init__(
        self,
        policy_engine: DefaultPolicy,
        router: ModelRouter,
        provider_factory: ProviderFactory,
        telemetry_tracker: TelemetryTracker
    ):
        """Initializes the AI Gateway with its dependent platform layers.

        Args:
            policy_engine: Policy rules evaluator.
            router: Decoupled router mapping tasks to models.
            provider_factory: Registry and instantiation manager for provider adapters.
            telemetry_tracker: Metric logger.
        """
        self.policy_engine = policy_engine
        self.router = router
        self.provider_factory = provider_factory
        self.telemetry = telemetry_tracker

    async def generate(self, request: AIRequest) -> AIResponse:
        """Executes the complete generation request lifecycle.

        1. Evaluates input against the Policy Engine.
        2. Resolves model selection via the Model Router.
        3. Obtains the provider adapter from the Provider Factory.
        4. Issues request and tracks latency/usage stats.

        Args:
            request: Standard platform AIRequest.

        Returns:
            Standard platform AIResponse.
        """
        # Step 1: Evaluate Policy constraints
        self.policy_engine.evaluate(request)

        # Step 2: Route task type to provider and target model
        provider_name, target_model = self.router.route(request)

        # Step 3: Instantiate/retrieve provider adapter
        provider = self.provider_factory.get_provider(provider_name)

        # Step 4: Record telemetry request metrics
        start_time = self.telemetry.record_request(request)

        # Step 5: Inject target_model into extra_params and execute generation on the provider
        extra_params = request.extra_params.copy() if request.extra_params else {}
        extra_params["target_model"] = target_model
        resolved_request = request.model_copy(update={"extra_params": extra_params})

        response = await provider.generate(resolved_request)

        # Step 6: Log latency and token usage metrics
        self.telemetry.record_response(request, response, start_time)

        return response

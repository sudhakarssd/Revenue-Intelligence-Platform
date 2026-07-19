from typing import Tuple, Dict, Optional, Union
from app.ai.contracts import AIRequest
from app.shared.enums import TaskType, ProviderType
from app.ai.exceptions.exceptions import ModelRouteException


class ModelRouter:
    def __init__(
        self,
        default_provider: str,
        default_model: str,
        task_routing_table: Optional[Dict[TaskType, Dict[str, str]]] = None
    ):
        self.default_provider = default_provider
        self.default_model = default_model
        
        # Maps platform TaskType enums to provider and target models
        self.task_routing_table = task_routing_table if task_routing_table is not None else {
            TaskType.SUMMARIZE: {"provider": "openai", "target_model": "gpt-4o"},
            TaskType.ANALYZE: {"provider": "openai", "target_model": "gpt-4-turbo"},
            TaskType.CHAT: {"provider": "openai", "target_model": "gpt-4o"},
            TaskType.FORECAST: {"provider": "openai", "target_model": "gpt-4-turbo"},
            TaskType.SUGGEST: {"provider": "openai", "target_model": "gpt-3.5-turbo"},
        }

    def route(self, request: AIRequest) -> Tuple[str, str]:
        """Routes a task-based AIRequest to the mapped provider and target model.

        Args:
            request: The standard platform AIRequest contract.

        Returns:
            A tuple of (provider_name, target_model)

        Raises:
            ModelRouteException: If the task cannot be routed and no default fallback is set.
        """
        task = request.task

        # Resolve TaskType if it was loaded as a string
        resolved_task = None
        if isinstance(task, str):
            try:
                resolved_task = TaskType(task.lower())
            except ValueError:
                pass
        elif isinstance(task, TaskType):
            resolved_task = task

        # Check explicit routing table
        if resolved_task and resolved_task in self.task_routing_table:
            mapping = self.task_routing_table[resolved_task]
            return mapping["provider"], mapping["target_model"]

        # Default fallback if set
        if self.default_provider and self.default_model:
            return self.default_provider, self.default_model

        raise ModelRouteException(
            f"Unable to route task request for task '{task}'. Check routing table."
        )

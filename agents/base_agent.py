from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from pydantic import BaseModel, ValidationError


# -------------------------------------------------------------------
# Shared system context injected into every agent
# -------------------------------------------------------------------

SHARED_SYSTEM_CONTEXT = """
You are part of an AI decision-support system designed to help the owner
of a small business decide what actions to take based on daily business metrics.

Your role is not to replace human judgment, but to reduce cognitive load by
surfacing clear, actionable insights with appropriate confidence, caveats,
and traceability.

You must:
- Rely only on validated, structured inputs
- Avoid speculation beyond the data
- Prefer simple, practical actions over abstract advice
- Be explicit about uncertainty when it exists
- Maintain traceability between observations and recommendations
""".strip()


# -------------------------------------------------------------------
# Base Agent
# -------------------------------------------------------------------

class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    Subclasses must define:
    - input_model: Pydantic model for validated input
    - output_model: Pydantic model for validated output
    - agent_prompt: Agent-specific system instructions
    """

    input_model: Type[BaseModel]
    output_model: Type[BaseModel]
    agent_prompt: str

    def __init__(self, llm_client: Any):
        """
        llm_client is expected to expose a method:
            generate(system_prompt: str, user_prompt: str) -> dict
        """
        self.llm_client = llm_client

    def run(self, input_data: Dict[str, Any]) -> BaseModel:
        """
        Execute the agent:
        - Validate inputs
        - Construct prompt
        - Call LLM
        - Validate outputs
        """
        validated_input = self._validate_input(input_data)
        raw_output = self._call_llm(validated_input)
        validated_output = self._validate_output(raw_output)
        return validated_output

    # ----------------------------------------------------------------
    # Validation
    # ----------------------------------------------------------------

    def _validate_input(self, input_data: Dict[str, Any]) -> BaseModel:
        try:
            return self.input_model(**input_data)
        except ValidationError as e:
            raise ValueError(
                f"{self.__class__.__name__} input validation failed: {e}"
            )

    def _validate_output(self, output_data: Dict[str, Any]) -> BaseModel:
        try:
            return self.output_model(**output_data)
        except ValidationError as e:
            raise ValueError(
                f"{self.__class__.__name__} output validation failed: {e}"
            )

    # ----------------------------------------------------------------
    # Prompt Construction
    # ----------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        return f"{SHARED_SYSTEM_CONTEXT}\n\n{self.agent_prompt}".strip()

    def _build_user_prompt(self, validated_input: BaseModel) -> str:
        """
        Default behavior: pass structured input as JSON.
        Subclasses may override if needed.
        """
        return validated_input.json(indent=2)

    # ----------------------------------------------------------------
    # LLM Call
    # ----------------------------------------------------------------

    def _call_llm(self, validated_input: BaseModel) -> Dict[str, Any]:
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(validated_input)

        response = self.llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        if not isinstance(response, dict):
            raise ValueError(
                f"{self.__class__.__name__} LLM response must be a JSON object"
            )

        return response
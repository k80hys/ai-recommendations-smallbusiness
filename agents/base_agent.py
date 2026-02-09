from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel, ValidationError

SHARED_SYSTEM_CONTEXT = """
You are part of an AI decision-support system for small business metrics.
Provide clear insights, traceable actions, and appropriate caveats.
""".strip()

class BaseAgent(ABC):
    input_model: Type[BaseModel]
    output_model: Type[BaseModel]
    agent_prompt: str

    def __init__(self, llm_client: Any):
        self.llm_client = llm_client

    def run(self, input_data: Any) -> BaseModel:
        validated_input = self._validate_input(input_data)
        raw_output = self._call_llm(validated_input)
        validated_output = self._validate_output(raw_output)
        return validated_output

    def _validate_input(self, input_data: Any) -> BaseModel:
        if isinstance(input_data, self.input_model):
            return input_data
        if hasattr(input_data, "model_dump"):
            input_data = input_data.model_dump()
        if not isinstance(input_data, dict):
            raise TypeError(f"{self.__class__.__name__} input must be dict or {self.input_model.__name__}")
        try:
            return self.input_model(**input_data)
        except ValidationError as e:
            raise ValueError(f"{self.__class__.__name__} input validation failed: {e}")

    def _validate_output(self, output_data: Any) -> BaseModel:
        if isinstance(output_data, self.output_model):
            return output_data
        if hasattr(output_data, "model_dump"):
            output_data = output_data.model_dump()
        if not isinstance(output_data, dict):
            raise TypeError(f"{self.__class__.__name__} output must be dict or {self.output_model.__name__}")
        try:
            return self.output_model(**output_data)
        except ValidationError as e:
            raise ValueError(f"{self.__class__.__name__} output validation failed: {e}")

    def _build_system_prompt(self) -> str:
        return f"{SHARED_SYSTEM_CONTEXT}\n\n{self.agent_prompt}".strip()

    def _build_user_prompt(self, validated_input: BaseModel) -> str:
        return validated_input.model_dump_json(indent=2)

    def _call_llm(self, validated_input: BaseModel) -> Dict[str, Any]:
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(validated_input)
        response = self.llm_client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        if not isinstance(response, dict):
            raise ValueError(f"{self.__class__.__name__} LLM response must be a dict")
        return response

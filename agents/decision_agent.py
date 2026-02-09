from pydantic import BaseModel

from agents.base_agent import BaseAgent
from schemas import Signals, FullSnapshot, DecisionAction


# -------------------------------------------------------------------
# Input Model
# -------------------------------------------------------------------

class DecisionAgentInput(BaseModel):
    """
    Input to the Decision Agent:
    - Analyst observations (Signals)
    - Full snapshot of business context
    """
    signals: Signals
    full_snapshot: FullSnapshot


# -------------------------------------------------------------------
# Decision Agent
# -------------------------------------------------------------------

class DecisionAgent(BaseAgent):
    """
    Decision Agent:
    Converts analyst observations into prioritized, actionable recommendations.
    """

    input_model = DecisionAgentInput
    output_model = DecisionAction

    agent_prompt = """
You are the Decision Agent.

Your task is to convert business observations into a small set of prioritized,
actionable recommendations for a small business owner. The action suggestion
cadence is daily.

Rules:
- Propose a maximum of 3 actions.
- Each action must directly reference at least one observation.
- Actions must be realistic, specific, and achievable within days (not months).
- Avoid vague advice (e.g., "optimize", "improve", "consider").
- Prefer reversible actions when uncertainty is high.

Input:
You will receive:
- A JSON object containing analyst observations (Signals)
- A JSON object containing the full business context (FullSnapshot)

Output:
Return a JSON object with the following structure:

{
  "actions": [
    {
      "action": "<clear, concrete action>",
      "rationale": "<why this action follows from the observations>",
      "priority": 1,
      "source_observation_ids": [1, 3],
      "uncertainty": "low | medium | high"
    }
  ]
}

Guidelines:
- Priority 1 = highest impact or urgency.
- If no action is warranted, return an empty actions list and explain why
  in the rationale fields of the (empty) response.
""".strip()
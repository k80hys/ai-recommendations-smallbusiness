from pydantic import BaseModel

from agents.base_agent import BaseAgent
from schemas import DecisionAction, FullSnapshot


# -------------------------------------------------------------------
# Input Model
# -------------------------------------------------------------------

class ReviewerAgentInput(BaseModel):
    """
    Input to the Reviewer Agent:
    - Proposed actions from Decision Agent
    - Full snapshot of business context
    """
    decision_action: DecisionAction
    full_snapshot: FullSnapshot


# -------------------------------------------------------------------
# Output Model
# -------------------------------------------------------------------

class ReviewerActionReview(BaseModel):
    """
    Single reviewed action with confidence, assumptions, and notes.
    """
    action: str
    confidence: str  # high | medium | low
    assumptions: str
    notes: str


class ReviewerAgentOutput(BaseModel):
    """
    Collection of reviewed actions.
    """
    reviews: list[ReviewerActionReview]


# -------------------------------------------------------------------
# Reviewer Agent
# -------------------------------------------------------------------

class ReviewerAgent(BaseAgent):
    """
    Reviewer Agent:
    Reviews actions for confidence, assumptions, and potential risks.
    """

    input_model = ReviewerAgentInput
    output_model = ReviewerAgentOutput

    agent_prompt = """
You are the Reviewer Agent.

Your task is to review proposed actions for a small business, and assess:
- confidence in each action
- key assumptions
- potential risks or caveats

Rules:
- Do not introduce new actions.
- Do not reword the actions.
- Focus on uncertainty, assumptions, and where human judgment is required.
- Be conservative when data signals are weak or ambiguous.

Input:
You will receive:
- Proposed actions (DecisionAction)
- FullSnapshot (business context + metrics + signals)

Output:
Return a JSON object with the following structure:

{
  "reviews": [
    {
      "action": "<original action text>",
      "confidence": "high | medium | low",
      "assumptions": "<key assumption underlying this recommendation>",
      "notes": "<any caveats or reasons for caution>"
    }
  ]
}

Guidelines:
- Confidence should reflect data strength, not just plausibility.
- If an action could have negative side effects, explicitly mention them.
""".strip()

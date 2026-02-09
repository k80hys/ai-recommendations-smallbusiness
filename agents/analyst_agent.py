from typing import List
from pydantic import BaseModel

from agents.base_agent import BaseAgent
from schemas import Metrics, HistoricalMetrics, Signals


# -------------------------------------------------------------------
# Input / Output Models
# -------------------------------------------------------------------

class AnalystAgentInput(BaseModel):
    """
    Input to the Analyst Agent:
    - Today's validated metrics
    - Full historical metrics log
    """
    metrics: Metrics
    historical_metrics: HistoricalMetrics


# -------------------------------------------------------------------
# Analyst Agent
# -------------------------------------------------------------------

class AnalystAgent(BaseAgent):
    """
    Analyst Agent:
    Converts validated metrics into structured observations (Signals).
    """

    input_model = AnalystAgentInput
    output_model = Signals

    agent_prompt = """
You are the Analyst Agent.

Your task is to interpret structured business metrics and historical metrics
to identify notable patterns, changes, or risks applicable to the current day.

Rules:
- Do not suggest actions.
- Do not prioritize or rank observations.
- Only describe what is happening, based strictly on the input data.
- Avoid speculation beyond the data provided.
- Use clear, plain language suitable for a non-technical business owner.

Input:
You will receive:
- Validated daily metrics
- A history of previous daily metrics

Output:
Return a JSON object with the following structure:

{
  "observations": [
    {
      "observation_id": 1,
      "text": "<concise observation>",
      "metric": "<metric referenced>",
      "change": "<day-over-day change or %>",
      "signal_strength": "low | medium | high"
    }
  ]
}

Guidelines:
- Include only observations that are meaningfully different from baseline.
- Observations should be relevant to the day at hand.
- You may reference broader historical trends if directly relevant.
- Explicitly note if key metrics are stable.
- Limit to a maximum of 5 observations.
""".strip()
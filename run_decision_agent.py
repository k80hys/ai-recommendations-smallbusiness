import json
from datetime import date
from pathlib import Path

from preprocessing.validate_metrics import validate_and_process_metrics
from agents.analyst_agent import AnalystAgent, AnalystAgentInput
from agents.decision_agent import DecisionAgent, DecisionAgentInput
from agents.reviewer_agent import ReviewerAgent, ReviewerAgentInput, ReviewerAgentOutput, ReviewerActionReview
from schemas import FullSnapshot, DailyDecisionBrief, DailyDecisionBriefItem

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
DATA_DIR = Path("data")
FINAL_OUTPUT_FILE = DATA_DIR / "daily_decision_brief.json"

# -------------------------------------------------------------------
# Mock LLM client for demonstration
# Replace with real LLM API client in production
# -------------------------------------------------------------------
class MockLLMClient:
    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Dummy response for testing.
        Replace this method with your LLM API call.
        """
        # This just echoes back a plausible structure; real LLM call needed in production
        return {}

# -------------------------------------------------------------------
# Main orchestration
# -------------------------------------------------------------------
def run_pipeline():
    # -----------------------
    # 1. Preprocessing
    # -----------------------
    metrics, historical_metrics = validate_and_process_metrics()

    # -----------------------
    # 2. Analyst Agent
    # -----------------------
    analyst_agent = AnalystAgent(llm_client=MockLLMClient())
    analyst_input = AnalystAgentInput(
        metrics=metrics,
        historical_metrics=historical_metrics
    )
    signals = analyst_agent.run(analyst_input)

    # -----------------------
    # 3. Build FullSnapshot
    # -----------------------
    # For demonstration, we load static business/industry info from the daily_snapshot.json
    # Replace this with real BusinessConfig and IndustryProfile if separate
    full_snapshot = FullSnapshot(
        business_config=metrics.dict().get("business_config", {}),
        industry_profile=metrics.dict().get("industry_profile", {}),
        metrics=metrics,
        signals=signals
    )

    # -----------------------
    # 4. Decision Agent
    # -----------------------
    decision_agent = DecisionAgent(llm_client=MockLLMClient())
    decision_input = DecisionAgentInput(
        signals=signals,
        full_snapshot=full_snapshot
    )
    decision_action = decision_agent.run(decision_input)

    # -----------------------
    # 5. Reviewer Agent
    # -----------------------
    reviewer_agent = ReviewerAgent(llm_client=MockLLMClient())
    reviewer_input = ReviewerAgentInput(
        decision_action=decision_action,
        full_snapshot=full_snapshot
    )
    reviewer_output: ReviewerAgentOutput = reviewer_agent.run(reviewer_input)

    # -----------------------
    # 6. Merge into DailyDecisionBrief
    # -----------------------
    items: list[DailyDecisionBriefItem] = []
    for review in reviewer_output.reviews:
        items.append(DailyDecisionBriefItem(
            action=review.action,
            rationale=next((a.rationale for a in decision_action.actions if a.action == review.action), ""),
            confidence=review.confidence,
            notes=review.notes
        ))

    daily_brief = DailyDecisionBrief(
        date=date.today(),
        items=items
    )

    # -----------------------
    # 7. Save & Print
    # -----------------------
    with open(FINAL_OUTPUT_FILE, "w") as f:
        f.write(daily_brief.json(indent=2))

    print(f"DailyDecisionBrief saved to {FINAL_OUTPUT_FILE}")
    print(daily_brief.json(indent=2))


if __name__ == "__main__":
    run_pipeline()

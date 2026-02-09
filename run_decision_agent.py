import json
from datetime import date
from pathlib import Path

from preprocessing.validate_metrics import validate_and_process_metrics
from agents.analyst_agent import AnalystAgent, AnalystAgentInput
from agents.decision_agent import DecisionAgent, DecisionAgentInput
from agents.reviewer_agent import ReviewerAgent, ReviewerAgentInput
from schemas import (
    FullSnapshot, DailyDecisionBrief, DailyDecisionBriefItem,
    BusinessConfig, IndustryProfile, Signals, DecisionAction, DecisionActionItem
)

DATA_DIR = Path("data")
FINAL_OUTPUT_FILE = DATA_DIR / "daily_decision_brief.json"

# ----------------------------
# Mock LLM Client
# ----------------------------
class MockLLMClient:
    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        # Return minimal valid demo outputs based on the calling agent
        if "Analyst Agent" in system_prompt:
            return {
                "observations": [
                    {
                        "observation_id": 1,
                        "text": "Daily sales performance appears normal for current business operations",
                        "metric": "sales",
                        "change": 0.0,
                        "signal_strength": "medium"
                    }
                ]
            }
        elif "Decision Agent" in system_prompt:
            return {
                "actions": [
                    {
                        "action": "Monitor current operations",
                        "rationale": "Current metrics show stable performance",
                        "priority": 1,
                        "source_observation_ids": [1],
                        "uncertainty": "low"
                    }
                ]
            }
        elif "Reviewer Agent" in system_prompt:
            return {
                "reviews": [
                    {
                        "action": "Monitor current operations",
                        "confidence": "high",
                        "assumptions": "Business metrics will continue at current levels",
                        "notes": "No immediate action required based on current data"
                    }
                ]
            }
        else:
            return {}

# ----------------------------
# Main Pipeline
# ----------------------------
def run_pipeline():
    # 1. Preprocessing
    metrics, historical_metrics = validate_and_process_metrics()

    # 2. Analyst Agent
    analyst_agent = AnalystAgent(llm_client=MockLLMClient())
    analyst_input = AnalystAgentInput(metrics=metrics, historical_metrics=historical_metrics)
    signals = analyst_agent.run(analyst_input)
    if not signals or not hasattr(signals, "observations"):
        signals = Signals(observations=[])

    # 3. Build FullSnapshot
    business_config = metrics.business_config or BusinessConfig(
        name="Demo Business", hours="08:00-20:00", staffing=5,
        capacity=50, operating_days=["Mon","Tue","Wed","Thu","Fri"], preferences={}
    )
    industry_profile = metrics.industry_profile or IndustryProfile(
        industry_type="bakery", tone="supportive", assumptions={}, signal_priorities=[]
    )
    
    full_snapshot = FullSnapshot(
        business_config=business_config,
        industry_profile=industry_profile,
        metrics=metrics,
        signals=signals
    )

    # 4. Decision Agent
    decision_agent = DecisionAgent(llm_client=MockLLMClient())
    decision_input = DecisionAgentInput(signals=signals, full_snapshot=full_snapshot)
    decision_action = decision_agent.run(decision_input)
    if not hasattr(decision_action, "actions"):
        decision_action = DecisionAction(actions=[])

    # 5. Reviewer Agent
    reviewer_agent = ReviewerAgent(llm_client=MockLLMClient())
    reviewer_input = ReviewerAgentInput(decision_action=decision_action, full_snapshot=full_snapshot)
    reviewer_output = reviewer_agent.run(reviewer_input)
    if not hasattr(reviewer_output, "reviews"):
        from agents.reviewer_agent import ReviewerAgentOutput
        reviewer_output = ReviewerAgentOutput(reviews=[])

    # 6. Merge into DailyDecisionBrief
    items: list[DailyDecisionBriefItem] = []
    for review in reviewer_output.reviews:
        rationale = next((a.rationale for a in decision_action.actions if a.action == review.action), "")
        items.append(DailyDecisionBriefItem(
            action=review.action,
            rationale=rationale,
            confidence=review.confidence,
            notes=review.notes
        ))

    daily_brief = DailyDecisionBrief(date=date.today(), items=items)

    # 7. Save & Print
    FINAL_OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(FINAL_OUTPUT_FILE, "w") as f:
        f.write(daily_brief.model_dump_json(indent=2))

    print(f"DailyDecisionBrief saved to {FINAL_OUTPUT_FILE}")
    print(daily_brief.model_dump_json(indent=2))


if __name__ == "__main__":
    run_pipeline()

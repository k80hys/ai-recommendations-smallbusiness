# AI-Agent-Driven Recommendations for Small Businesses
**Author:** Katie Hayes  
**Role Demonstrated:** AI-Native Product Management / Decision Support 

---

## Overview

This project is a prototype AI-native decision system designed to help small business owners turn daily operational metrics into actionable, prioritized recommendations.  

It showcases a **three-agent architecture** that separates reasoning into interpretable stages:  

- **Analyst Agent** – converts raw metrics into structured observations and signals  
- **Decision Agent** – transforms observations into actionable recommendations  
- **Reviewer Agent** – evaluates recommendations, providing confidence scores and contextual notes  

The goal is **not to replace human judgment**, but to reduce cognitive load, surface reliable recommendations quickly, and illustrate scalable AI-native decision workflows.

---

## Problem
Small businesses face daily challenges:  

- Tracking and interpreting multiple metrics (sales, traffic, inventory)  
- Prioritizing actions amid fluctuating demand and operational constraints  
- Making decisions while balancing risk, staffing, and customer experience  

This system demonstrates a structured AI-native workflow for turning **signals into decisions** while mitigating AI hallucination risks.

---

## Scope
- **Business example:** Small bakery (e.g., Hayes Baked Goods)  
- **Decision horizon:** Daily  
- **Inputs:** Daily metrics (sales, traffic, inventory) and business configuration  
- **Outputs:** Ranked, actionable recommendations with confidence and notes  
- **Design:** Lightweight, reproducible, and easily extendable to other small business types  

---

## Architecture

      ┌──────────────────┐
      │  Daily Metrics   │
      │  (sales, traffic,│
      │   inventory, etc.)│
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │  Analyst Agent   │
      │  (Observations & │
      │   Signals)       │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Decision Agent   │
      │ (Actions &       │
      │  Prioritization) │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Reviewer Agent   │
      │ (Confidence &    │
      │  Contextual Notes)│
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Daily Decision   │
      │ Brief (Output)   │
      └──────────────────┘

**Design Highlights:**  
- Stepwise reasoning: **Observations → Actions → Confidence**  
- Guardrails: schema validation and constrained signal values  
- Human-in-the-loop ready: outputs are interpretable and reversible  
- Clear AI- workflow: each agent has a distinct responsibility  

---

## Input Data

Daily metrics are stored in `data/daily_snapshot.json`. Example structure:

```json
{
  "business_config": {
    "name": "Your Business",
    "hours": "08:00-20:00",
    "staffing": 5,
    "capacity": 50,
    "operating_days": ["Mon","Tue","Wed","Thu","Fri"],
    "preferences": {"risk_tolerance": "medium"}
  },
  "industry_profile": {
    "industry_type": "bakery",
    "tone": "supportive",
    "assumptions": {},
    "signal_priorities": ["revenue_change","inventory_risk"]
  },
  "metrics": {
    "date": "2026-02-08",
    "sales": 540.75,
    "traffic": 120,
    "inventory": {"bread": 15,"croissant": 8,"muffin": 12}
  }
}

See `schemas.py` for full definitions and validation logic.

## Example Output

The system generates a `DailyDecisionBrief` with prioritized, actionable recommendations.  

### JSON Example

```json
{
  "date": "2026-02-08",
  "items": [
    {
      "action": "Adjust inventory levels for high-demand items",
      "rationale": "Sales data shows inventory depletion faster than historical average",
      "confidence": "high",
      "notes": "Consider weather impact on foot traffic"
    }
  ]
}

## Console Output Example

### Focus production on top 2 products
- **Reason:** Revenue decline combined with concentration in top product  
- **Confidence:** Medium  
- **Notes:** Assumes decline is demand-driven, not seasonal  

### Restock critical ingredients immediately
- **Reason:** Inventory levels are low, risk of running out  
- **Confidence:** High  

### Limit new custom orders this week
- **Reason:** High operational load could affect quality and delivery  
- **Confidence:** Medium  

---

## Key Technical Highlights
- **AI-native design:** Multi-agent system separates analysis, decision-making, and review  
- **Robust input handling:** Pydantic schemas ensure metrics and signals are reliable  
- **Rule-based reasoning with AI augmentation:** Actions are deterministic, reproducible, and interpretable  
- **Customizable industry profiles:** Add industry-specific assumptions, priorities, and recommendation logic  
- **LLM integration-ready:** Easily swap `MockLLMClient` for OpenAI, Anthropic, or local models  

---

## Future Enhancements
- Connect to real business systems such as Square
- Replace `MockLLMClient` with preferred LLM for full capability
- Extend to multiple industry types - build out /industry_profiles section
- Add event-driven automation to run the agent daily

---

## Reproducible Steps

### Clone the repository

```
git clone https://github.com/k80hys/ai-decision-agent.git
cd ai-decision-agent
```

### Install dependencies

```
pip install -r requirements.txt
```

### Run the daily decision agent

```
python run_decision_agent.py
```

###Check the output

- Check the console output for the Daily Decision Brief
- Or view the generated output at `data/daily_decision_brief.json`

## File Structure

```
ai-decision-agent/
├── README.md
├── requirements.txt
├── run_decision_agent.py      # Main pipeline
├── schemas.py                 # Data models
├── agents/
│   ├── base_agent.py         # Base agent class
│   ├── analyst_agent.py      # Metrics → Signals
│   ├── decision_agent.py     # Signals → Actions
│   └── reviewer_agent.py     # Actions → Reviews
├── preprocessing/
│   └── validate_metrics.py   # Input validation
├── industry_profiles/
│   ├── base.py
│   ├── bakery.py
│   └── bar.py
├── data/
│   ├── daily_snapshot.json   # Input metrics
│   ├── historical_metrics.json  # Historical data
│   └── daily_decision_brief.json  # Output
└── examples/
    ├── sample_input.json
    └── sample_output.md
```
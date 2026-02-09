# AI-Agent-Driven Recommendations for Small Businesses

An intelligent decision-support system for small businesses that analyzes daily metrics and provides actionable recommendations through a multi-agent AI pipeline.

## Overview

The AI Decision Agent processes daily business metrics through a three-stage pipeline to generate prioritized, actionable recommendations:

1. **Analyst Agent** - Converts raw metrics into structured observations and signals
2. **Decision Agent** - Transforms observations into specific, actionable recommendations  
3. **Reviewer Agent** - Reviews and validates recommendations with confidence scores

## Architecture

```
Daily Metrics → Analyst Agent → Decision Agent → Reviewer Agent → Daily Decision Brief
```

### Components

- **`schemas.py`** - Pydantic models defining the data structures
- **`agents/`** - The three-agent pipeline (analyst, decision, reviewer)
- **`preprocessing/`** - Input validation and historical data management
- **`industry_profiles/`** - Industry-specific configurations and assumptions
- **`data/`** - Input metrics and generated outputs
- **`run_decision_agent.py`** - Main pipeline orchestrator

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai-decision-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Pipeline

```bash
python run_decision_agent.py
```

This will:
- Load daily metrics from `data/daily_snapshot.json` (or create demo data if missing)
- Process through the three-agent pipeline
- Generate `data/daily_decision_brief.json` with actionable recommendations
- Display results in the console

## Input Data Format

Place your daily metrics in `data/daily_snapshot.json`:

```json
{
  "business_config": {
    "name": "Your Business",
    "hours": "08:00-20:00",
    "staffing": 5,
    "capacity": 50,
    "operating_days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "preferences": {"risk_tolerance": "medium"}
  },
  "industry_profile": {
    "industry_type": "bakery",
    "tone": "supportive",
    "assumptions": {},
    "signal_priorities": ["revenue_change", "inventory_risk"]
  },
  "metrics": {
    "date": "2026-02-08",
    "sales": 540.75,
    "traffic": 120,
    "inventory": {
      "bread": 15,
      "croissant": 8,
      "muffin": 12
    }
  }
}
```

## Output Format

The system generates a `DailyDecisionBrief` with prioritized actions:

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
```

## Pipeline Details

### 1. Analyst Agent
- **Input:** Daily metrics + historical data
- **Output:** Structured observations and signals
- **Purpose:** Identify patterns, changes, and noteworthy trends

### 2. Decision Agent  
- **Input:** Analyst signals + full business context
- **Output:** Specific, actionable recommendations
- **Purpose:** Convert observations into concrete business actions

### 3. Reviewer Agent
- **Input:** Proposed actions + business context
- **Output:** Reviewed actions with confidence scores
- **Purpose:** Validate recommendations and assess confidence levels

## Customization

### Industry Profiles
Add industry-specific logic in `industry_profiles/`:
- Custom business assumptions
- Industry-specific signal priorities
- Tailored recommendation patterns

### LLM Integration
Replace `MockLLMClient` in `run_decision_agent.py` with your preferred LLM:
- OpenAI GPT models
- Anthropic Claude
- Local models via ollama/llama.cpp

Example:
```python
from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        # Implement OpenAI API call
        pass
```

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
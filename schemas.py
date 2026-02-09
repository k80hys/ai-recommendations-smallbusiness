from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


# ----------------------------
# Static Business & Industry
# ----------------------------

class BusinessConfig(BaseModel):
    name: str
    hours: str  # e.g., "08:00-20:00"
    staffing: int
    capacity: int
    operating_days: List[str]  # e.g., ["Mon", "Tue", "Wed"]
    preferences: Optional[dict] = None  # e.g., {"risk_tolerance": "medium", "growth_focus": True}


class IndustryProfile(BaseModel):
    industry_type: str  # e.g., "bar", "bakery"
    tone: str  # e.g., "friendly", "supportive"
    assumptions: dict
    signal_priorities: List[str]  # e.g., ["revenue_change", "inventory_risk"]


# ----------------------------
# Automated Metrics
# ----------------------------

class Metrics(BaseModel):
    date: date
    sales: float
    traffic: int
    inventory: dict  # item_name -> quantity
    reservations: Optional[int] = None
    other_metrics: Optional[dict] = None


# ----------------------------
# Historical Metrics Log
# ----------------------------

class HistoricalMetrics(BaseModel):
    history: List[Metrics] = Field(default_factory=list)


# ----------------------------
# Analyst Observations
# ----------------------------

class AnalystObservation(BaseModel):
    observation_id: int  # unique identifier
    text: str  # concise observation text
    metric: Optional[str] = None  # referenced metric, e.g., "sales", "traffic"
    change: Optional[float] = None  # e.g., day-over-day percent change
    signal_strength: Optional[str] = Field(
        default="medium", description="low | medium | high"
    )


class Signals(BaseModel):
    observations: List[AnalystObservation]


# ----------------------------
# Decision Actions
# ----------------------------

class DecisionActionItem(BaseModel):
    action: str  # clear, concrete action
    rationale: str  # why this action follows from observations
    priority: int  # 1 = highest impact/urgency
    source_observation_ids: List[int]  # links to AnalystObservation IDs
    uncertainty: Optional[str] = Field(
        default=None, description="optional: low | medium | high"
    )


class DecisionAction(BaseModel):
    actions: List[DecisionActionItem]


# ----------------------------
# Full Snapshot
# ----------------------------

class FullSnapshot(BaseModel):
    business_config: BusinessConfig
    industry_profile: IndustryProfile
    metrics: Metrics
    signals: Optional[Signals] = None


# ----------------------------
# Daily Decision Brief
# ----------------------------

class DailyDecisionBriefItem(BaseModel):
    action: str
    rationale: str
    confidence: str  # high | medium | low
    notes: Optional[str] = None


class DailyDecisionBrief(BaseModel):
    date: date
    items: List[DailyDecisionBriefItem]
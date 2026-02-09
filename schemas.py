from typing import List, Optional, Dict
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
    preferences: Optional[Dict[str, object]] = None  # e.g., {"risk_tolerance": "medium"}

class IndustryProfile(BaseModel):
    industry_type: str  # e.g., "bar", "bakery"
    tone: str  # e.g., "friendly", "supportive"
    assumptions: Dict[str, object] = {}
    signal_priorities: List[str] = []

# ----------------------------
# Automated Metrics
# ----------------------------
class Metrics(BaseModel):
    date: date
    sales: float
    traffic: int
    inventory: Dict[str, int]  # item_name -> quantity
    reservations: Optional[int] = None
    other_metrics: Optional[Dict[str, object]] = None
    # Optional placeholders for demo
    business_config: Optional[BusinessConfig] = None
    industry_profile: Optional[IndustryProfile] = None

# ----------------------------
# Historical Metrics Log
# ----------------------------
class HistoricalMetrics(BaseModel):
    history: List[Metrics] = Field(default_factory=list)

# ----------------------------
# Analyst Observations & Signals
# ----------------------------
class AnalystObservation(BaseModel):
    observation_id: int
    text: str
    metric: Optional[str] = None
    change: Optional[float] = None
    signal_strength: Optional[str] = Field(default="medium", description="low | medium | high")

class Signals(BaseModel):
    observations: List[AnalystObservation] = Field(default_factory=list)

# ----------------------------
# Decision Actions
# ----------------------------
class DecisionActionItem(BaseModel):
    action: str
    rationale: str
    priority: int
    source_observation_ids: List[int]
    uncertainty: Optional[str] = Field(default=None, description="low | medium | high")

class DecisionAction(BaseModel):
    actions: List[DecisionActionItem] = Field(default_factory=list)

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
    confidence: str
    notes: Optional[str] = None

class DailyDecisionBrief(BaseModel):
    date: date
    items: List[DailyDecisionBriefItem] = Field(default_factory=list)

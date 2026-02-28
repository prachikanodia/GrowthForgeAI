from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal, Optional



class DecisionRequest(BaseModel):
    decision: str = Field(description="Users input", min_length=8)
    domain: str= Field(description="domain where the query is related to")
    goal: str = Field(description="goal of the user", min_length=5)
    context: str = Field(description="Any further context to help the output")
    constraints: Optional[list[str]] = Field(default=[], description="Any constraints to keep in mind before generating the final reccomendation.")
    options_considered: Optional[list[str]] = Field(default=[], description="Any options user has thought of already")
    urgency: Literal["low","medium","high"] = Field(description="Urgency level of the user query.")
    risk_tolerance: Literal["low", "medium", "high"] = Field(description="How much risk user is okay to accept.")
    success_metrics: List[str] = Field(description="Options to be prioritised first.")

    @field_validator("success_metrics")
    @classmethod
    def validate_success_metrics(cls, value):
        if not value:
            raise ValueError("At least one success metric must be provided")
        return value
    
    @model_validator(mode="after")
    def validate_high_urgency_context(self):
        if self.urgency == "high" and len(self.context) < 20:
            raise ValueError(
                "For high urgency decisions, context must be more detailed"
            )
        return self

class RiskItem(BaseModel):
    risk: str = Field(description="A specific risk associated with this option.")
    probability: Literal["low", "medium", "high"] = Field(description="How likely this risk is.")
    impact: Literal["low", "medium", "high"] = Field(description="How severe the impact would be if it happens.")
    mitigation: str = Field(description="How to reduce the chance/impact of this risk.")
    early_warning: str = Field(description="Early signal that this risk is starting to happen.")

class StrategyOption(BaseModel):
    name: str = Field(description="Short name for this option (e.g., 'Pilot rollout', 'Full launch').")
    summary: str = Field(description="2-3 line summary of what this option means and how it would be executed.")
    pros: List[str] = Field(description="Advantages of this option.")
    cons: List[str] = Field(description="Disadvantages / trade-offs of this option.")
    expected_outcome: str = Field(description="What is the expected result if this option is executed.")
    risks: List[RiskItem] = Field(description="Risk analysis for this option (3-6 items recommended).")
    effort: Literal["low", "medium", "high"] = Field(description="Effort required to execute this option.")
    time_to_value: Literal["days", "weeks", "months"] = Field(description="How quickly this option is expected to show results.")

class DecisionResponse(BaseModel):
    assumptions: List[str] = Field(description="Assumptions the model is making based on user inputs. Should be explicit and checkable.")
    key_questions: List[str] = Field(description="Questions to ask the user to reduce uncertainty. Use this instead of guessing.")
    framework_refs: List[str] = Field(description="Frameworks used to structure the decision (e.g., ['SWOT','Risk Matrix']).")
    options: List[StrategyOption] = Field(description="2-3 strategy options. Each option must include risks, effort, time-to-value.")
    recommendation: str = Field(description="The final recommended decision (must be concrete, not 'it depends').")
    recommendation_rationale: List[str] = Field(description="Bullet reasons why this recommendation was chosen over other options.")
    experiment_plan: List[str] = Field(description="A short plan to validate the recommendation (hypothesis, metric, timeline, rollback).")
    confidence: float = Field(gt=0.0,lt=1.0,description="Confidence score between 0 and 1 based on completeness of information and uncertainty.")



from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class ThresholdItem:
    name: str
    value: float


@dataclass(frozen=True)
class Summary:
    credit_rationed: bool
    early_bidding_type: Literal["No", "Separating", "Pooling"]
    late_bidding_type: Literal["No", "Separating", "Pooling"]
    development_attempt: bool
    development_outcome: bool
    early_takeover: bool
    late_takeover: bool


@dataclass(frozen=True)
class OptimalMergerPolicySummary(Summary):
    optimal_policy: Literal[
        "Strict",
        "Intermediate (late takeover prohibited)",
        "Intermediate (late takeover allowed)",
        "Laissez-faire",
    ]

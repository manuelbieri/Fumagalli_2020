from dataclasses import dataclass
from enum import Enum


class MergerPolicies(Enum):
    Strict = "Strict"
    Intermediate_late_takeover_prohibited = "Intermediate (late takeover prohibited)"
    Intermediate_late_takeover_allowed = "Intermediate (late takeover allowed)"
    Laissez_faire = "Laissez-faire"


class Takeover(Enum):
    No = "No bid"
    Separating = "Separating bid"
    Pooling = "Pooling bid"


@dataclass(frozen=True)
class ThresholdItem:
    name: str
    value: float


@dataclass(frozen=True)
class Summary:
    credit_rationed: bool
    early_bidding_type: Takeover
    late_bidding_type: Takeover
    development_attempt: bool
    development_outcome: bool
    early_takeover: bool
    late_takeover: bool


@dataclass(frozen=True)
class OptimalMergerPolicySummary(Summary):
    optimal_policy: MergerPolicies

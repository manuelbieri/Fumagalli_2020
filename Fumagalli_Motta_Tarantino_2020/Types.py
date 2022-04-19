from dataclasses import dataclass
from enum import Enum


class MergerPolicies(Enum):
    Strict = "Strict"
    Intermediate_late_takeover_prohibited = "Intermediate (late takeover prohibited)"
    Intermediate_late_takeover_allowed = "Intermediate (late takeover allowed)"
    Laissez_faire = "Laissez-faire"

    def __str__(self) -> str:
        return self.value


class Takeover(Enum):
    No = "No bid"
    Separating = "Separating bid"
    Pooling = "Pooling bid"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ThresholdItem:
    name: str
    value: float


@dataclass(frozen=True)
class Summary:
    set_policy: MergerPolicies
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

from dataclasses import dataclass
from enum import Enum


class MergerPolicies(Enum):
    Strict = "Strict"
    Intermediate_late_takeover_prohibited = "Intermediate (late takeover prohibited)"
    Intermediate_late_takeover_allowed = "Intermediate (late takeover allowed)"
    Laissez_faire = "Laissez-faire"

    def abbreviation(self) -> str:
        if self is MergerPolicies.Intermediate_late_takeover_prohibited:
            return "$I^P$"
        if self is MergerPolicies.Intermediate_late_takeover_allowed:
            return "$I^A$"
        return f"${self.value[0]}$"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def legend() -> str:
        return (
            f"{MergerPolicies.Strict.abbreviation()}: Strict\n"
            f"{MergerPolicies.Intermediate_late_takeover_prohibited.abbreviation()}: Intermediate (late takeover prohibited)\n"
            f"{MergerPolicies.Intermediate_late_takeover_allowed.abbreviation()}: Intermediate (late takeover allowed)\n"
            f"{MergerPolicies.Laissez_faire.abbreviation()}: Laissez-faire"
        )


class Takeover(Enum):
    No = "No bid"
    Separating = "Separating bid"
    Pooling = "Pooling bid"

    def abbreviation(self) -> str:
        return f"${self.value[0]}$"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def legend() -> str:
        return (
            f"{Takeover.No.abbreviation()}: No bid by the incumbent\n"
            f"{Takeover.Separating.abbreviation()}: Separating bid by the incumbent\n"
            f"{Takeover.Pooling.abbreviation()}: Pooling bid by the incumbent"
        )


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

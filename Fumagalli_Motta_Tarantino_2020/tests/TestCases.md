# Explanations about the Unittests

In this file the different Test cases used, are explained. Tests written in bold letters are not yet implemented, but needed for full coverage.

## Glossary about the naming of tests

| Part of name             | Remark                                                                                                           |
|:-------------------------|:-----------------------------------------------------------------------------------------------------------------|
| *not_profitable*         | $p(\pi^M_I-\pi^m_I) < K$ is satisfied                                                                            | 
| *profitable*             | $p(\pi^M_I-\pi^m_I) \ge K$ is satisfied                                                                          |
| *below_assets_threshold* | $F < \Phi$ is satisfied                                                                                          |
| *above_assets_threshold* | $F \ge \Phi$ is satisfied                                                                                        |
| *credit_rationed*        | The start-up is credit constraint                                                                                |
| *not_credit_rationed*    | The start-up is not credit constraint                                                                            |
| *unsuccessful*           | The development (if it will take place) is unsuccessful, otherwise we will assume the development was successful |

$F$ may correspond to $F(\bar{A})$ or $F(\bar{A}^T)$ and $\Phi$ to $\Phi(\cdot)$, $\Phi^\prime(\cdot)$ or $\Phi^T(\cdot)$.

## TestBaseModel

This testcase includes tests for the following matters:
- Test properties (public access for private variables)
- Test necessary conditions for correct values (see pre- and post-conditions)

## TestMergerPolicyModel

This  testcase tests, whether the default model properly works.

## TestLaissezFaireMergerPolicyModel

This testcase tests, whether the implemented logic for a laissez-faire merger policy works as expected. The following tests are included:

| Name of test                                                                | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:----------------------------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_below_assets_threshold_not_credit_rationed              |              False               |         Pooling          |           No            |        False         |   Does not matter   |         True         |        False        |
| test_not_profitable_above_assets_threshold_credit_rationed                  |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_not_profitable_above_assets_threshold_not_credit_rationed              |              False               |            No            |         Pooling         |         True         |        True         |        False         |        True         |
| test_not_profitable_below_assets_threshold_not_credit_rationed_unsuccessful |              False               |            No            |           No            |         True         |        False        |        False         |        False        |
| test_profitable_credit_rationed                                             |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_not_credit_rationed                                         |              False               |        Separating        |         Pooling         |         True         |        True         |        False         |        True         |
| test_profitable_not_credit_rationed_unsuccessful                            |              False               |        Separating        |           No            |         True         |        False        |        False         |        False        |

## TestIntermediateLateTakeoverAllowedMergerPolicyModel

| Name of test                                         | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed              |              False               |            No            |         Pooling         |         True         |        True         |        False         |        True         |
| test_not_profitable_not_credit_rationed_unsuccessful |              False               |            No            |           No            |         True         |        False        |        False         |        False        |
| test_not_profitable_credit_rationed                  |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_credit_rationed                      |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_not_credit_rationed                  |              False               |        Separating        |         Pooling         |         True         |        True         |        False         |        True         |
| test_profitable_not_credit_rationed_unsuccessful     |              False               |        Separating        |           No            |         True         |        False        |        False         |        False        |

## TestIntermediateLateTakeoverProhibitedMergerPolicyModel

This testcase tests, whether the implemented logic for a intermediate merger policy (late takeovers are prohibited) works as expected. The following tests are included:

| Name of test                                                   | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:---------------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_below_assets_threshold_not_credit_rationed |              False               |         Pooling          |           No            |        False         |   Does not matter   |         True         |        False        |
| test_not_profitable_above_assets_threshold_not_credit_rationed |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_profitable_above_assets_threshold_not_credit_rationed     |              False               |        Separating        |           No            |         True         |   Does not matter   |        False         |        False        |
| test_profitable_above_assets_threshold_credit_rationed         |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_below_assets_threshold_not_credit_rationed     |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_below_assets_threshold_credit_rationed         |               True               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |

## TestStrictMergerPolicyModel

This testcase tests, whether the implemented logic for a strict merger policy works as expected. The following tests are included:

| New Name of test                                           | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed                    |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_not_profitable_credit_rationed                        |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_below_assets_threshold_credit_rationed     |               True               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_below_assets_threshold_not_credit_rationed |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_above_assets_threshold_credit_rationed     |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_above_assets_threshold_not_credit_rationed |              False               |        Separating        |           No            |         True         |   Does not matter   |        False         |        False        |

## TestOptimalMergerPolicyModel

This testcase tests all possibilities for an optimal merger policy.

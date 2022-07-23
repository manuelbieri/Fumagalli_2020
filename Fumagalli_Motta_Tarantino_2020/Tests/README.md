[![CI](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml)
[![codecov](https://codecov.io/gh/manuelbieri/Fumagalli_2020/branch/master/graph/badge.svg?token=RRZ3PJI9U1)](https://codecov.io/gh/manuelbieri/Fumagalli_2020)

This file provides an overview of the available testcases. Check out the codecov.io report for the details about the coverage (click on the badge above).

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

## Fumagalli_Motta_Tarantino_2020.Tests.MockModels

MockModels provides a stub for the OptimalMergerPolicy - class, this is used to test classes for visualizations independently
of the implementation of the models.

## Fumagalli_Motta_Tarantino_2020.Tests.Test_Base
### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestCoreModel

This testcase test, whether Fumagalli_Motta_Tarantino_2020.Models.Base.CoreModel is set up in a valid way.

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestProperties

This testcase includes tests for the following matters:
- Test properties (public access for private variables)
- Test necessary conditions for correct values (see pre- and post-conditions)

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestMergerPolicy

This  testcase tests, whether Fumagalli_Motta_Tarantino_2020.Models.Base.MergerPolicy properly works.

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestLaissezFaireMergerPolicy

This testcase tests, whether the implemented logic for a laissez-faire merger policy works as expected. The following tests are included:

| Name of test                                                                | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) | Killer Acquisition? |
|:----------------------------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|:-------------------:|
| test_not_profitable_below_assets_threshold_not_credit_rationed              |              False               |         Pooling          |           No            |        False         |   Does not matter   |         True         |        False        |        True         |
| test_not_profitable_above_assets_threshold_credit_rationed                  |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |        False        |
| test_not_profitable_above_assets_threshold_not_credit_rationed              |              False               |            No            |         Pooling         |         True         |        True         |        False         |        True         |        False        |
| test_not_profitable_below_assets_threshold_not_credit_rationed_unsuccessful |              False               |            No            |           No            |         True         |        False        |        False         |        False        |        False        |
| test_profitable_credit_rationed                                             |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |        False        |
| test_profitable_not_credit_rationed                                         |              False               |        Separating        |         Pooling         |         True         |        True         |        False         |        True         |        False        |
| test_profitable_not_credit_rationed_unsuccessful                            |              False               |        Separating        |           No            |         True         |        False        |        False         |        False        |        False        |

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestIntermediateLateTakeoverAllowedMergerPolicy

This testcase tests, whether the implemented logic for an intermediate merger policy (late takeovers are allowed) works as expected. The following tests are included:

| Name of test                                         | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed              |              False               |            No            |         Pooling         |         True         |        True         |        False         |        True         |
| test_not_profitable_not_credit_rationed_unsuccessful |              False               |            No            |           No            |         True         |        False        |        False         |        False        |
| test_not_profitable_credit_rationed                  |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_credit_rationed                      |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_not_credit_rationed                  |              False               |        Separating        |         Pooling         |         True         |        True         |        False         |        True         |
| test_profitable_not_credit_rationed_unsuccessful     |              False               |        Separating        |           No            |         True         |        False        |        False         |        False        |

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestIntermediateLateTakeoverProhibitedMergerPolicy

This testcase tests, whether the implemented logic for an intermediate merger policy (late takeovers are prohibited) works as expected. The following tests are included:

| Name of test                                                   | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:---------------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_below_assets_threshold_not_credit_rationed |              False               |         Pooling          |           No            |        False         |   Does not matter   |         True         |        False        |
| test_not_profitable_above_assets_threshold_not_credit_rationed |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_profitable_above_assets_threshold_not_credit_rationed     |              False               |        Separating        |           No            |         True         |   Does not matter   |        False         |        False        |
| test_profitable_above_assets_threshold_credit_rationed         |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_below_assets_threshold_not_credit_rationed     |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_below_assets_threshold_credit_rationed         |               True               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestStrictMergerPolicy

This testcase tests, whether the implemented logic for a strict merger policy works as expected. The following tests are included:

| New Name of test                                           | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed                    |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_not_profitable_credit_rationed                        |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_below_assets_threshold_credit_rationed     |               True               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_below_assets_threshold_not_credit_rationed |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_above_assets_threshold_credit_rationed     |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_above_assets_threshold_not_credit_rationed |              False               |        Separating        |           No            |         True         |   Does not matter   |        False         |        False        |

Additionally, the recalculations of the model after changed properties are tested.

### Fumagalli_Motta_Tarantino_2020.Tests.Test_Base.TestOptimalMergerPolicy

This testcase tests all possibilities for an optimal merger policy in Fumagalli_Motta_Tarantino_2020.Models.Base.OptimalMergerPolicy.

## Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended
### Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended.TestCournotCompetition

This testcase tests the adjustments made for the Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.CournotCompetition, which is largely based on the OptimalMergerPolicyModel.

### Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended.TestPerfectInformation

This testcase tests, whether the implemented logic in Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation works as expected.

### Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended.TestStrictPerfectInformation

This testcase tests, whether the implemented logic in Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation for a strict merger policy works as expected. The following tests are included:

| Name of test                            | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:----------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_not_profitable_credit_rationed     |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_not_credit_rationed     |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_profitable_credit_rationed         |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |

### Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended.TestIntermediatePerfectInformation

This testcase tests, whether the implemented logic in Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation for an intermediate merger policy (late takeovers are allowed) works as expected. The following tests are included:

| Name of test                                         | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed              |              False               |            No            |         Pooling         |        False         |        True         |        False         |        True         |
| test_not_profitable_not_credit_rationed_unsuccessful |              False               |            No            |           No            |        False         |        False        |        False         |        False        |
| test_not_profitable_credit_rationed                  |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_not_credit_rationed                  |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_credit_rationed                      |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |

### Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended.TestLaissezFairePerfectInformation

This testcase tests, whether the implemented logic in Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation for a laissez-faire merger policy works as expected. The following tests are included:

| Name of test                            | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:----------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_not_profitable_not_credit_rationed |              False               |         Pooling          |           No            |        False         |   Does not matter   |         True         |        False        |
| test_not_profitable_credit_rationed     |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_profitable_not_credit_rationed     |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_profitable_credit_rationed         |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |

### Fumagalli_Motta_Tarantino_2020.Tests.Test_BaseExtended.TestEquityContract

This testcase tests, whether the implemented logic in Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.Equity works as expected.

## Fumagalli_Motta_Tarantino_2020.Tests.Test_Extension

Includes tests for Fumagalli_Motta_Tarantino_2020.Models.Extension.ProCompetitive and Fumagalli_Motta_Tarantino_2020.Models.Extension.ResourceWaste.

## Fumagalli_Motta_Tarantino_2020.Tests.Test_Visualize

This testcase test the plots in Fumagalli_Motta_Tarantino_2020.Visualizations made with mock objects. The plots are tested by eye, since currently no method exists, to write
stable unitest for matplotlib. 

## Fumagalli_Motta_Tarantino_2020.Tests.Test_Configurations

Includes tests for Fumagalli_Motta_Tarantino_2020.Configurations.LoadConfig and Fumagalli_Motta_Tarantino_2020.Configurations.FindConfig.


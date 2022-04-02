# Explanations about the Unittests

In this file the different Test cases used, are explained.

### TestBaseModel

This testcase includes tests for the following matters:
- Test properties (public access for private variables)
- Test necessary conditions for correct values (see pre- and post-conditions)

### TestMergerPolicyModel

This  testcase tests, whether the default model properly works.

### TestLaissezFaireMergerPolicyModel

This testcase tests, whether the implemented logic for a laissez-faire merger policy works as expected. The following tests are included:

| Name of test                                                          | Is the start-up credit rationed? |  Early bidding type (t=1)  | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:----------------------------------------------------------------------|:--------------------------------:|:--------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_laissez_faire_default_outcome                                    |              False               |          Pooling           |           No            |        False         |   Does not matter   |         True         |        False        |
| **test_laissez_faire_pooling_bid_shelving**                           |               True               |          Pooling           |           No            |        False         |   Does not matter   |         True         |        False        |
| test_laissez_faire_no_early_takeover_credit_rationed                  |               True               |             No             |           No            |        False         |   Does not matter   |        False         |        False        |
| test_laissez_faire_no_early_takeover_not_credit_rationed              |              False               |             No             |         Pooling         |         True         |        True         |        False         |        True         |
| test_laissez_faire_no_early_takeover_not_credit_rationed_unsuccessful |              False               |             No             |           No            |         True         |        False        |        False         |        False        |
| test_laissez_faire_early_takeover_credit_rationed                     |               True               |         Separating         |           No            |         True         |   Does not matter   |         True         |        False        |
| test_laissez_faire_early_takeover_not_credit_rationed                 |              False               |         Separating         |         Pooling         |         True         |        True         |        False         |        True         |
| test_laissez_faire_early_takeover_not_credit_rationed_unsuccessful    |              False               |         Separating         |           No            |         True         |        False        |        False         |        False        |

### TestIntermediateLateTakeoverAllowedMergerPolicyModel


### TestIntermediateLateTakeoverProhibitedMergerPolicyModel

This testcase tests, whether the implemented logic for a intermediate merger policy (late takeovers are prohibited) works as expected. The following tests are included:

| Name of test                                                                             | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_intermediate_late_takeover_prohibited_default                                       |              False               |         Pooling          |           No            |        False         |   Does not matter   |         True         |        False        |
| **test_intermediate_late_takeover_prohibited_not_profitable_no_takeover**                |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| **test_intermediate_late_takeover_prohibited_profitable_separating_bid**                 |              False               |        Separating        |           No            |         True         |   Does not matter   |        False         |        False        |
| **test_intermediate_late_takeover_prohibited_profitable_separating_bid_credit_rationed** |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| **test_intermediate_late_takeover_prohibited_profitable_pooling_bid**                    |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| **test_intermediate_late_takeover_prohibited_profitable_pooling_bid_credit_rationed**    |               True               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |

### TestStrictMergerPolicyModel

This testcase tests, whether the implemented logic for a strict merger policy works as expected. The following tests are included:

| Name of test                                                     | Is the start-up credit rationed? | Early bidding type (t=1) | Late bidding type (t=2) | Development attempt? | Development success | Early takeover (t=1) | Late takeover (t=2) |
|:-----------------------------------------------------------------|:--------------------------------:|:------------------------:|:-----------------------:|:--------------------:|:-------------------:|:--------------------:|:-------------------:|
| test_strict_merger_policy_default                                |              False               |            No            |           No            |         True         |   Does not matter   |        False         |        False        |
| test_strict_merger_policy_credit_rationed                        |               True               |            No            |           No            |        False         |   Does not matter   |        False         |        False        |
| test_strict_merger_policy_pooling_bid                            |               True               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| **test_strict_merger_policy_pooling_bid_not_credit_rationed**    |              False               |         Pooling          |           No            |         True         |   Does not matter   |         True         |        False        |
| test_strict_merger_policy_separating_bid                         |               True               |        Separating        |           No            |         True         |   Does not matter   |         True         |        False        |
| **test_strict_merger_policy_separating_bid_not_credit_rationed** |              False               |        Separating        |           No            |         True         |   Does not matter   |        False         |        False        |

import Fumagalli_Motta_Tarantino_2020.Tests.Test_Base as Test
import Fumagalli_Motta_Tarantino_2020 as FMT20


class TestProCompetitive(Test.TestOptimalMergerPolicy):
    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.ProCompetitive(**kwargs)

    def test_tolerated_harm_strict(self):
        self.setupModel()
        self.assertEqual(0, self.model.tolerated_harm)

    def test_tolerated_harm_intermediate_late_takeover_prohibited(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
        )
        self.assertTrue(
            self.are_floats_equal(
                0.019840426, self.model.tolerated_harm, tolerance=10**-8
            )
        )

    def test_tolerated_harm_intermediate_late_takeover_allowed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed
        )
        self.assertEqual(0, self.model.tolerated_harm)

    def test_laissez_faire_optimal_merger_policy(self):
        self.setupModel()
        self.assertFalse(self.model.is_laissez_faire_optimal())

    def test_intermediate_optimal_merger_policy(self):
        self.setupModel()
        self.assertFalse(self.model.is_intermediate_optimal())

    def test_strict_optimal_merger_policy(self):
        self.setupModel()
        self.assertTrue(self.model.is_strict_optimal())


class TestStrictProCompetitive(TestProCompetitive):
    def test_not_profitable(self):
        self.setUpConfiguration(config_id=30)
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestIntermediateLateTakeoverProhibitedProCompetitive(TestProCompetitive):
    def test_not_profitable_above_threshold(self):
        self.setUpConfiguration(
            config_id=30,
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_below_threshold(self):
        self.setUpConfiguration(
            config_id=31,
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertTrue(self.model.is_killer_acquisition())


class TestIntermediateLateTakeoverAllowedProCompetitive(TestProCompetitive):
    def test_not_profitable_above_threshold_not_credit_rationed(self):
        self.setUpConfiguration(
            config_id=30,
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.late_bidding_type)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_not_profitable_above_threshold_not_credit_rationed_unsuccessful(self):
        self.setUpConfiguration(
            config_id=30,
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            development_success=False,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_above_threshold_credit_rationed(self):
        self.setUpConfiguration(
            config_id=32,
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_below_threshold(self):
        self.setUpConfiguration(
            config_id=31,
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertTrue(self.model.is_killer_acquisition())


class TestResourceWaste(TestProCompetitive):
    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.ResourceWaste(**kwargs)

    def test_tolerated_harm_intermediate_late_takeover_prohibited(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
        )
        self.assertEqual(0, self.model.tolerated_harm)

    def test_string_representation(self):
        pass

    def test_not_profitable_above_threshold(self):
        self.setUpConfiguration(config_id=41)
        self.assertEqual(
            FMT20.MergerPolicies.Strict,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_below_threshold(self):
        self.setUpConfiguration(config_id=40)
        self.assertEqual(
            FMT20.MergerPolicies.Strict,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertTrue(self.model.is_killer_acquisition())

    def test_intermediate_optimal_merger_policy(self):
        self.setUpConfiguration(config_id=42)
        self.assertTrue(self.model.is_intermediate_optimal())
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.get_optimal_merger_policy(),
        )

    def test_laissez_faire_optimal_merger_policy(self):
        self.setupModel()
        self.assertTrue(self.model.is_laissez_faire_optimal())

    def test_strict_optimal_merger_policy(self):
        self.setupModel()
        self.assertFalse(self.model.is_strict_optimal())

    def test_strict_optimal_merger_policy_summary(self):
        self.setupModel()
        summary: FMT20.OptimalMergerPolicySummary = self.model.summary()
        self.assertNotEqual(FMT20.MergerPolicies.Strict, summary.optimal_policy)

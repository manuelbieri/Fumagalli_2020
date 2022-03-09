import abc
import unittest

import scipy.stats
import Fumagalli_Motta_Tarantino_2020.CDF


class TestAbstractCDF(abc.ABC, unittest.TestCase):
    tolerance: float = 10**-8

    def setUp(self) -> None:
        self.test_cdf = self.setUpCDF()

    @abc.abstractmethod
    def getIdealFA(self, A: float) -> float:
        pass

    @abc.abstractmethod
    def setUpCDF(self) -> Fumagalli_Motta_Tarantino_2020.CDF.AbstractCDF:
        pass

    @staticmethod
    def isEqualFloat(float_1, float_2) -> bool:
        return abs(float_1-float_2) < TestAbstractCDF.tolerance

    def test_isEqualFloat_true(self):
        a: float = 1
        b: float = a + TestAbstractCDF.tolerance/2
        self.assertTrue(self.isEqualFloat(a, b))

    def test_random_draw(self):
        a_test, f_a_test = self.test_cdf.draw()
        f_a_ideal = self.getIdealFA(a_test)
        self.assertTrue(self.isEqualFloat(f_a_test, f_a_ideal))

    def test_draw(self):
        a_test, f_a_test = self.test_cdf.draw(0.5)
        self.assertEqual(a_test, 0.5)
        f_a_ideal = self.getIdealFA(a_test)
        self.assertTrue(self.isEqualFloat(f_a_test, f_a_ideal))


class TestNormCDF(TestAbstractCDF):
    def getIdealFA(self, A: float) -> float:
        return float(scipy.stats.norm.cdf(A))

    def setUpCDF(self) -> Fumagalli_Motta_Tarantino_2020.CDF.AbstractCDF:
        return Fumagalli_Motta_Tarantino_2020.CDF.NormCDF()
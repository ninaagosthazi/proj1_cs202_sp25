import unittest
from proj1 import *
# proj1.py should contain your data class and function definitions
# these do not contribute positively to your grade.
# but your grade will be lowered if they are missing


class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(lo_lat=10.0, hi_lat=20.0, west_long=30.0, east_long=40.0)
        self.region = Region(rect=self.rect, name="Testland", terrain="other")
        self.rc = RegionCondition(region=self.region, year=2025, pop=1000, ghg_rate=5000.0)

        self.zero_pop_rc = RegionCondition(region=self.region, year=2025, pop=0, ghg_rate=5000.0)

        self.wrap_rect = GlobeRect(lo_lat=0.0, hi_lat=10.0, west_long=170.0, east_long=-170.0)

        self.small_rect = GlobeRect(lo_lat=0.0, hi_lat=1.0, west_long=0.0, east_long=1.0)
        self.large_rect = GlobeRect(lo_lat=0.0, hi_lat=10.0, west_long=0.0, east_long=10.0)

        self.dense_region = Region(rect=self.small_rect, name="Denseville", terrain="other")
        self.sparse_region = Region(rect=self.large_rect, name="Sparseville", terrain="forest")

        self.dense_rc = RegionCondition(region=self.dense_region, year=2025, pop=1000000, ghg_rate=10000.0)
        self.sparse_rc = RegionCondition(region=self.sparse_region, year=2025, pop=1000, ghg_rate=500.0)

        self.ocean_region = Region(rect=self.rect, name="Ocean Zone", terrain="ocean")
        self.mountain_region = Region(rect=self.rect, name="Mountain Zone", terrain="mountains")
        self.forest_region = Region(rect=self.rect, name="Forest Zone", terrain="forest")
        self.other_region = Region(rect=self.rect, name="Other Zone", terrain="other")

        self.ocean_rc = RegionCondition(region=self.ocean_region, year=2025, pop=10000, ghg_rate=20000.0)
        self.mountain_rc = RegionCondition(region=self.mountain_region, year=2025, pop=10000, ghg_rate=20000.0)
        self.forest_rc = RegionCondition(region=self.forest_region, year=2025, pop=10000, ghg_rate=20000.0)
        self.other_rc = RegionCondition(region=self.other_region, year=2025, pop=10000, ghg_rate=20000.0)

    def test_data_classes_exist(self):
        self.assertIsInstance(self.rect, GlobeRect)
        self.assertIsInstance(self.region, Region)
        self.assertIsInstance(self.rc, RegionCondition)

    def test_emissions_per_capita_basic(self):
        result = emissions_per_capita(self.rc)
        self.assertAlmostEqual(result, 5.0, places=4)

    def test_emissions_per_capita_zero_population(self):
        result = emissions_per_capita(self.zero_pop_rc)
        self.assertEqual(result, 0.0)

    def test_area_basic(self):
        result = area(self.rect)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0.0)

    def test_area_wraparound(self):
        result = area(self.wrap_rect)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0.0)

    def test_emissions_per_square_km_basic(self):
        result = emissions_per_square_km(self.rc)
        expected = self.rc.ghg_rate / area(self.rc.region.rect)
        self.assertAlmostEqual(result, expected, places=4)

    def test_emissions_per_square_km_zero_area(self):
        zero_area_rect = GlobeRect(lo_lat=10.0, hi_lat=10.0, west_long=20.0, east_long=20.0)
        zero_area_region = Region(rect=zero_area_rect, name="Flat", terrain="other")
        zero_area_rc = RegionCondition(region=zero_area_region, year=2025, pop=1000, ghg_rate=5000.0)

        result = emissions_per_square_km(zero_area_rc)
        self.assertEqual(result, 0.0)

    def test_densest_single(self):
        result = densest([self.rc])
        self.assertEqual(result, "Testland")

    def test_densest_multiple(self):
        result = densest([self.sparse_rc, self.dense_rc])
        self.assertEqual(result, "Denseville")

    def test_project_condition_year(self):
        projected = project_condition(self.rc, 5)
        self.assertEqual(projected.year, 2030)

    def test_project_condition_same_region(self):
        projected = project_condition(self.rc, 3)
        self.assertEqual(projected.region, self.rc.region)

    def test_project_condition_zero_years(self):
        projected = project_condition(self.rc, 0)
        self.assertEqual(projected, self.rc)

    def test_project_condition_ocean_growth(self):
        projected = project_condition(self.ocean_rc, 1)
        self.assertEqual(projected.pop, int(10000 * 1.0001))

    def test_project_condition_mountains_growth(self):
        projected = project_condition(self.mountain_rc, 1)
        self.assertEqual(projected.pop, int(10000 * 1.0005))

    def test_project_condition_forest_growth(self):
        projected = project_condition(self.forest_rc, 1)
        self.assertEqual(projected.pop, int(10000 * 0.99999))

    def test_project_condition_other_growth(self):
        projected = project_condition(self.other_rc, 1)
        self.assertEqual(projected.pop, int(10000 * 1.0003))

    def test_project_condition_zero_population(self):
        zero_pop_projected = project_condition(self.zero_pop_rc, 4)
        self.assertEqual(zero_pop_projected.pop, 0)
        self.assertEqual(zero_pop_projected.ghg_rate, 0.0)

    def test_project_condition_emissions_scaled(self):
        projected = project_condition(self.rc, 1)
        expected_ghg = self.rc.ghg_rate * (projected.pop / self.rc.pop)
        self.assertAlmostEqual(projected.ghg_rate, expected_ghg, places=4)


if __name__ == '__main__':
    unittest.main()
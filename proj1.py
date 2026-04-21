import sys
import unittest
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)

# Task 1: Dataclasses
@dataclass(frozen = True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen = True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str

@dataclass(frozen = True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

# Task 2: Region Conditions

# LA
la_rect: GlobeRect = GlobeRect(33.5, 34.5, -119.0, -117.0)
la_region: Region = Region(la_rect, "Los Angeles", "other")
la_condition: RegionCondition = RegionCondition(la_region, 2025, 10000000, 50000000.0)

# Tokyo
tokyo_rect: GlobeRect = GlobeRect(35.0, 36.0, 139.0, 140.5)
tokyo_region: Region = Region(tokyo_rect, "Tokyo", "other")
tokyo_condition: RegionCondition = RegionCondition(tokyo_region, 2025, 37000000, 80000000.0)

# Pacific Ocean
pacific_rect: GlobeRect = GlobeRect(-10.0, 10.0, -150.0, -130.0)
pacific_region: Region = Region(pacific_rect, "Pacific Ocean Region", "ocean")
pacific_condition: RegionCondition = RegionCondition(pacific_region, 2025, 1000, 200000.0)

# SLO
slo_rect: GlobeRect = GlobeRect(35.0, 35.5, -121.0, -120.0)
slo_region: Region = Region(slo_rect, "San Luis Obispo", "other")
slo_condition: RegionCondition = RegionCondition(slo_region, 2025, 50000, 100000.0)

region_conditions: list[RegionCondition] = [la_condition, tokyo_condition, pacific_condition, slo_condition]

# Task 3: Functions
def emissions_per_capita(rc: RegionCondition) -> float:
    """
    Purpose: Computes CO2 emissions per person per year.
    Parameters: rc (RegionCondition): A RegionCondition object containing population and greenhouse gas emissions data.
    Returns: float: The emissions per capita (returns 0.0 if population is 0).
    Preconditions: rc is not None, rc.pop is an integer >= 0, and rc.ghg_rate is a float >= 0
    Postconditions: The function returns a non-negative float representing emissions per person.
    """
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate / rc.pop

def area(gr: GlobeRect) -> float:
    """
    Purpose: Calculates the surface area of a rectangular region on Earth in square kilometers.
    Parameters: gr (GlobeRect): A GlobeRect object that represents geographic bounds.
    Returns: float: The estimated surface area (in km^2)
    Preconditions: gr in not None, latitude values are between -90 and 90, and longitude values are between -180 and 180
    Postconditions: The function returns a non-negative float representing area.
    """
    R: float = 6378.1

    lam1: float = math.radians(gr.west_long)
    lam2: float = math.radians(gr.east_long)
    phi1: float = math.radians(gr.lo_lat)
    phi2: float = math.radians(gr.hi_lat)

    dist_lam: float = lam2 - lam1

    if dist_lam < 0:
        dist_lam += 2 * math.pi

    A: float = (R ** 2) * abs(dist_lam) * abs(math.sin(phi2) - math.sin(phi1))

    return A

def emissions_per_square_km(rc: RegionCondition) -> float:
    """
    Purpose: Computes CO2 emissions per square kilometer for a region.
    Parameters: rc (RegionCondition): A RegionCondition object that contains emissions data.
    Returns: float: Emissions per square kilometer (returns 0.0 if the area is 0)
    Preconditions: rc is not None, and rc.region.rect defines a valid geographic region
    Postconditions: The function returns a non-negative float that represents emission density.
    """
    a = area(rc.region.rect)

    if a == 0:
        return 0.0

    return rc.ghg_rate / a


def densest(rc_list: list[RegionCondition]) -> str:
    """
    Purpose: Determines the name of the region with the highest population density.
    Parameters: rc_list (list[RegionCondition]): A non-empty list of RegionCondition objects.
    Returns: str: The name of the region with the highest population density
    Preconditions: rc_list is not empty, and all elements in rc_list are valid RegionCondition objects
    Postconditions: The function returns the name of a region from the list.
    """
    if len(rc_list) == 1:
        return rc_list[0].region.name

    first: RegionCondition = rc_list[0]
    rest_best_name: str = densest(rc_list[1:])

    rest_best_rc: RegionCondition =_find_by_name(rc_list[1:], rest_best_name)

    if _density(first) >= _density(rest_best_rc):
        return first.region.name
    else:
        return rest_best_name


def _density(rc: RegionCondition) -> float:
    """densest() helper: calculates population density"""
    a = area(rc.region.rect)

    if a == 0:
        return 0.0

    return rc.pop / a

def _find_by_name(rc_list: list[RegionCondition], name: str) -> RegionCondition:
    """densest() helper: finds RegionCondition by name (recursive)"""
    if rc_list[0].region.name == name:
        return rc_list[0]

    return _find_by_name(rc_list[1:], name)

# Task 4: project_condition() function
def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    """
    Purpose: Projects the future condition of a region after a give number of years.
    Parameters: rc (RegionCondition): the current state of the region, and years (int): number of years to project
    Returns: RegionCondition: a new RegionCondition representing the future state
    Preconditions: rc is not None, and years is an integer >= 0
    Postconditions: Returns a new RegionCondition object (original rc object isn't modified), year increases by "years",
                    population changes based on terrain growth rate, and emissions scale proportionally with population
    """
    rate: float = _growth_rate(rc.region.terrain)

    new_pop: int = _project_population(rc.pop, rate, years)

    if rc.pop == 0:
        new_ghg: float = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(rc.region, rc.year + years, new_pop, new_ghg)

def _growth_rate(terrain: str) -> float:
    """project_condition() helper: returns growth rate based on terrain"""
    if terrain == "ocean":
        return 0.0001

    if terrain == "mountains":
        return 0.0005

    if terrain == "forest":
        return -0.00001

    else:
        return 0.0003

def _project_population(pop: int, rate: float, years: int) -> int:
    """project_condition() helper: recursively computes population growth"""
    if years == 0:
        return pop

    new_pop = int(pop * (1 + rate))

    return _project_population(new_pop, rate, years - 1)
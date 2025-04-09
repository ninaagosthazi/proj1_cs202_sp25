## 🌍 CSC 202 – Assignment 1: Modeling and Projecting the Earth's Surface

### Overview

In this assignment, we’re building a system to **rank and analyze regular slices of the Earth’s surface**. Your job is to design the data structures, create example data, and implement functions that help reason about climate-related changes over time.

Your work will be organized into **four tasks**.

You must use:
- `@dataclass(frozen=True)` for all your data definitions  
- **External functions only** (no class methods)  
- **Recursive functions** for list processing  
- **Correct type hinting** for all functions and data structures  
  > ✅ *We recommend using a VS Code extension like* `Pylance` *or* `Pyright` *to check type hints and catch errors early*

---

## ⚠️ Important Setup Step Before You Begin

If you are using **GitHub Codespaces**, make sure to run the following command in the terminal **before you start coding**:

```bash
git pull --no-rebase
```

This ensures you have the most up-to-date files (like `basic-tests.py`) from the starter repository before making any edits.

---

## ✅ Task 1: Define the Data Classes

Define **three immutable data classes** using `@dataclass(frozen=True)`. These will model the basic geographic and environmental information about regions on Earth.

---

### `GlobeRect`

Represents a rectangular region of the globe. It should contain the following attributes:

- `lo_lat`: the lower latitude in degrees (between -90 and 90 inclusive)
- `hi_lat`: the upper latitude in degrees (greater than `lo_lat`)
- `west_long`: the western longitude in degrees (between -180 and 180)
- `east_long`: the eastern longitude in degrees (between -180 and 180)

> Note: `west_long` may be greater than `east_long` for regions crossing the international date line.

---

### `Region`

Describes the identity and terrain of a region. It should contain:

- `rect`: a `GlobeRect` object describing the physical boundaries
- `name`: a string with the name of the region (e.g., `"Tokyo"`)
- `terrain`: a string representing the terrain type — one of:
  - `"ocean"`
  - `"mountains"`
  - `"forest"`
  - `"other"`

---

### `RegionCondition`

Describes the current state of a region in a specific year. It should include:

- `region`: a `Region` object
- `year`: the year of observation (as an integer)
- `pop`: the population in that year (as an integer)
- `ghg_rate`: the greenhouse gas emissions for that year (as a float, in tons of CO₂-equivalent per year)

---

## ✅ Task 2: Create Example Data

Create **four instances** of `RegionCondition`. These will be used to test your functions in later tasks.

Store them in a list called:

```python
region_conditions = [...]
```

Your list must include:
1. A major metropolitan area from anywhere in the world
2. A second major metro from a different continent
3. A substantial ocean region (not a whole ocean)
4. A region that includes Cal Poly, but excludes:
   - San Jose
   - Santa Barbara
   - Bakersfield
   - and too much ocean

> Use rough estimates. Approximate within:
> - ~5% for latitude/longitude  
> - Factor of 10 for population or emissions  
> Don’t spend more than 5–10 minutes researching numbers.

---

## ✅ Task 3: Implement External Functions (with Design Recipe)

You must implement **external functions only** (do not define any methods inside the classes).  
Functions that process lists **must be recursive**.

### 🧪 Before you write any function logic:
For each function below, you must:
1. **Write your tests first** in a file called `test_student.py`
2. Write at least **1 test per function**
3. Confirm your test(s) pass before continuing

> Your code will be evaluated using **hidden test cases**, so feel confident that your implementation handles **edge cases, invalid input, and boundary conditions**.

---

### 🔹 Subtask 3.1: `emissions_per_capita(rc)`

Takes a `RegionCondition` and returns the tons of CO₂-equivalent **emitted per person** in the region per year. Avoid division by zero — return `0.0` if population is zero.

---

### 🔹 Subtask 3.2: `area(gr)`

Takes a `GlobeRect` and returns the estimated **area in square kilometers**.  
Ignore Earth's curvature — treat the region as a flat rectangle.  
Each degree of latitude and longitude ≈ 111 km.

---

### 🔹 Subtask 3.3: `emissions_per_square_km(rc)`

Takes a `RegionCondition` and returns the **tons of CO₂-equivalent per square kilometer**.

> Hint: Use the `area` function.

---

### 🔹 Subtask 3.4: `densest(rc_list)`

Takes a list of `RegionCondition` values and returns the **name** of the region with the highest population density, calculated as:

```
population / area
```

> This function must be **recursive**.  
> Do not use `max`, `for`, `while`, or list comprehensions.

---

## ✅ Task 4: Simulate Future Projections

Now we’ll simulate how regions change over time based on terrain-specific population growth.

### 🧪 Before you write any logic:
Follow the same process as Task 3:
1. Write at least one test in `test_student.py`
2. Use your test case to guide your implementation

---

### 🔹 Subtask 4.1: `project_condition(rc, years)`

Takes a `RegionCondition` and a number of years.  
Returns a **new RegionCondition** representing the projected state of the region after the given number of years.

#### Rules:
- Population grows exponentially based on the terrain type’s growth rate
- Emissions scale proportionally with population
- The region and terrain stay the same
- The `year` field increases by `years`

| Terrain     | Annual Growth Rate |
|-------------|--------------------|
| `"ocean"`     | +0.0001           |
| `"mountains"` | +0.0005           |
| `"forest"`    | -0.00001          |
| `"other"`     | +0.0003           |

> You are encouraged to define **helper functions** for population growth, emissions scaling, etc.  
> Do **not mutate** the original `RegionCondition` — return a new one.

---

## 🔧 Setup and Restrictions

Use the following imports only:

```python
import sys
import unittest
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)
```

You must:
- Use **recursion** for all list processing
- Avoid all loops and comprehensions
- Write **all behavior as external functions** — no class methods
- Use **correct type hinting** throughout your code  
  > ✅ *We recommend using a VS Code extension like* `Pylance` *or* `Pyright` *to check type hints and catch errors early*
- Follow the **design recipe**:
  1. Purpose statement  
  2. Type comment  
  3. One or more examples/tests  
  4. Function definition

---

## 📤 Handin Instructions

You must commit and push the following files to your GitHub Classroom repository:

- `lab1.py` – your main implementation file  
- `test_1.py` – your test suite with at least one test per function  

A file called `test_1.py` is included to check that:
- Function names match
- Argument counts and return types are correct

### ✅ Reminder:
- Do **not edit** `test_1.py`
- Ensure both `lab1.py` and `test_student.py` are committed and pushed
- Push your code to GitHub — verify your changes appear on the GitHub website
- You won't see a green check mark, look at the action workflow auto-grader output. 

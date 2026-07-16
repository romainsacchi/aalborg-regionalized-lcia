# Course Schedule

The schedule below maps each time block to specific notebooks.
Break durations and time can be adjusted during the course.
Each day starts at 09:00. Lunch is planned from 12:30 to 13:45.

## PRIOR TO ARRIVAL

Complete:
- [INSTRUCTIONS.MD](INSTRUCTIONS.MD)
- [tutorials/00_SETUP/00 - Setup and First Checks.ipynb](tutorials/00_SETUP/00%20-%20Setup%20and%20First%20Checks.ipynb)
- check [reading material](READING_MATERIAL.md)

## How to open the jupyter notebooks listed below
- Open your shell: `Terminal` on Mac or `Miniforge Prompt` on Windows for the preferred conda route. Use `PowerShell` on Windows only if you followed the alternate venv/pip route.
- Activate the `bw` environment with the preferred conda route:

```bash
conda activate bw
```

If conda is blocked and you used the alternate venv/pip route on macOS or Linux:

```bash
source .venv-bw/bin/activate
```

If conda is blocked and you used the alternate venv/pip route on Windows PowerShell:

```powershell
.\.venv-bw\Scripts\Activate.ps1
```

- Start Jupyter Lab:

```bash
jupyter lab
```

- Open the notebook we are working on.


## DAY 1 (Wednesday, September 16, 2026) - `brightway` Foundations

### 09:00 - 09:30
Welcome, setup check, course roadmap
- [D1-01 Python and Jupyter minimum refresher](tutorials/DAY%201/D1-01%20Python%20and%20Jupyter%20minimum%20refresher.ipynb)

### 09:30 - 10:30
`brightway` architecture and core data model
- [D1-02 `brightway` architecture and data model](tutorials/DAY%201/D1-02%20Brightway%20architecture%20and%20data%20model.ipynb)

### 10:30 - 11:00
Coffee break

### 11:00 - 12:30
Manual matrix LCA, `brightway` first LCA, BAFU:2025 import, and `ecoinvent` import overview
- [D1-03 Manual LCA with `numpy` matrices - Heijungs and Suh 2002 vs `brightway`](tutorials/DAY%201/D1-03%20Manual%20LCA%20with%20NumPy%20matrices%20-%20Heijungs%20and%20Suh%202002%20vs%20Brightway.ipynb)
- [D1-04 First LCA from demand to score in `brightway`](tutorials/DAY%201/D1-04%20First%20LCA%20from%20demand%20to%20score%20in%20Brightway.ipynb)

### 12:30 - 13:45
Lunch break

### 13:45 - 14:15
BAFU:2025 import and `ecoinvent` import overview, continued
- [D1-04 First LCA from demand to score in `brightway`](tutorials/DAY%201/D1-04%20First%20LCA%20from%20demand%20to%20score%20in%20Brightway.ipynb)

### 14:15 - 15:45
Uncertainty and Monte Carlo
- [D1-05 Uncertainty and Monte Carlo basics](tutorials/DAY%201/D1-05%20Uncertainty%20and%20Monte%20Carlo%20basics.ipynb)

### 15:45 - 16:15
Coffee break

### 16:15 - 18:15
Data QA/linking workflow and contribution analysis
- [D1-06 Data quality checks and linking workflow](tutorials/DAY%201/D1-06%20Data%20quality%20checks%20and%20linking%20workflow.ipynb)
- [D1-07 Contribution analysis and result visualization](tutorials/DAY%201/D1-07%20Contribution%20analysis%20and%20result%20visualization.ipynb)

### Optional Day 1 extensions, if time allows
Advanced `brightway` import, uncertainty, and parameter workflows
- [D1-08 Optional - ecoinvent import and Brightway recap](tutorials/DAY%201/D1-08%20Optional%20-%20ecoinvent%20import%20and%20Brightway%20recap.ipynb)
- [D1-09 Optional - Foreground and background uncertainty split](tutorials/DAY%201/D1-09%20Optional%20-%20Foreground%20and%20background%20uncertainty%20split.ipynb)
- [D1-10 Optional - Database-level parameters and Monte Carlo](tutorials/DAY%201/D1-10%20Optional%20-%20Database-level%20parameters%20and%20Monte%20Carlo.ipynb)
- [D1-11 Optional - Sea-floor transformation flows and custom LCIA method](tutorials/DAY%201/D1-11%20Optional%20-%20Additional%20biosphere%20database%20and%20custom%20LCIA%20method.ipynb)
- [D1-12 Optional - Correlated water balances in Monte Carlo](tutorials/DAY%201/D1-12%20Optional%20-%20Correlated%20water%20balances%20in%20Monte%20Carlo.ipynb)

## DAY 2 (Thursday, September 17, 2026) - Regionalised LCIA

### 09:00 - 10:00
Day 1 recap and environment checks
- [D2-01 Day 1 recap and readiness checks](tutorials/DAY%202/D2-01%20Day%201%20recap%20and%20readiness%20checks.ipynb)

### 10:00 - 11:00
`edges` fundamentals
- [D2-02 `edges` fundamentals and regionalisation concepts](tutorials/DAY%202/D2-02%20Edges%20fundamentals%20and%20regionalisation%20concepts.ipynb)

### 11:00 - 11:15
Coffee break

### 11:15 - 12:30
`edges` workflow, spatial matching, and regionalised methods
- [D2-03 Introduction to `edges` workflow and API](tutorials/DAY%202/D2-03%20Introduction%20to%20edges%20workflow%20and%20API.ipynb)
- [D2-04 Spatial matching and fallback logic](tutorials/DAY%202/D2-04%20Spatial%20matching%20and%20fallback%20logic.ipynb)
- [D2-05 Regionalised methods across impact categories](tutorials/DAY%202/D2-05%20Regionalised%20methods%20across%20impact%20categories.ipynb)

### 12:30 - 13:45
Lunch break

### 13:45 - 14:15
Regionalised methods across impact categories, continued
- [D2-05 Regionalised methods across impact categories](tutorials/DAY%202/D2-05%20Regionalised%20methods%20across%20impact%20categories.ipynb)

### 14:15 - 15:45
Variability and uncertainty in regionalised LCIA
- [D2-06 Variability and uncertainty in regionalised LCIA](tutorials/DAY%202/D2-06%20Variability%20and%20uncertainty%20in%20regionalised%20LCIA.ipynb)

### 15:45 - 16:15
Coffee break

### 16:15 - 18:15
Case study: regionalised hydrogen pathways
- [D2-07 Case study - Regionalised hydrogen pathways](tutorials/DAY%202/D2-07%20Case%20study%20-%20Regionalised%20hydrogen%20pathways.ipynb)

## DAY 3 (Friday, September 18, 2026) - Scenario LCIA and Inventory Flow Assessment

### 09:00 - 10:00
Day 2 recap and Day 3 readiness checks
- [D3-01 Day 2 recap and Day 3 readiness checks](tutorials/DAY%203/D3-01%20Day%202%20recap%20and%20Day%203%20readiness%20checks.ipynb)

### 10:00 - 11:00
Scenario-based LCIA with parameterised CFs
- [D3-02 Parameterised characterization factors with edges](tutorials/DAY%203/D3-02%20Parameterised%20characterization%20factors%20with%20edges.ipynb)
- [D3-03 Time and scenario integration workflow](tutorials/DAY%203/D3-03%20Time%20and%20scenario%20integration%20workflow.ipynb)

### 11:00 - 11:15
Coffee break

### 11:15 - 12:15
Scenario-based LCIA with parameterised CFs
- [D3-02 Parameterised characterization factors with edges](tutorials/DAY%203/D3-02%20Parameterised%20characterization%20factors%20with%20edges.ipynb)
- [D3-03 Time and scenario integration workflow](tutorials/DAY%203/D3-03%20Time%20and%20scenario%20integration%20workflow.ipynb)

### 12:15 - 12:30
Inventory flow assessment I
- [D3-04 Inventory flow assessment I - tracing intermediates](tutorials/DAY%203/D3-04%20Inventory%20flow%20assessment%20I%20-%20tracing%20intermediates.ipynb)

### 12:30 - 13:45
Lunch break

### 13:45 - 14:15
Inventory flow assessment I, continued
- [D3-04 Inventory flow assessment I - tracing intermediates](tutorials/DAY%203/D3-04%20Inventory%20flow%20assessment%20I%20-%20tracing%20intermediates.ipynb)

### 14:15 - 15:15
Inventory flow assessment II
- [D3-05 Inventory flow assessment II - criticality factors](tutorials/DAY%203/D3-05%20Inventory%20flow%20assessment%20II%20-%20criticality%20factors.ipynb)

### 15:15 - 15:30
Coffee break

### 15:30 - 17:15
Capstone dual case study and wrap-up
- [D3-06 Capstone dual case study](tutorials/DAY%203/D3-06%20Capstone%20dual%20case%20study.ipynb)

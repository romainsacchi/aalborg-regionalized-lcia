# BW Cheatsheet — verification report

Every command block on **`BW Cheatsheet_kt_2026.pptx`** (version 3, Aug 2026) was executed against
the pinned course environment:

| package | version |
|---|---|
| `bw2data` | 4.7 |
| `bw2calc` | 2.5.0 |
| `bw2io` | 0.9.17 |
| `bw2analyzer` | 0.11.7 |
| `wurst` | 0.5.3 |
| `polyviz` | 1.0.4 |
| Python | 3.11 |

Working proof for every item is in
[`BW Cheatsheet in practice - PV panel case study.ipynb`](BW%20Cheatsheet%20in%20practice%20-%20PV%20panel%20case%20study.ipynb),
which runs top to bottom with zero errors.

---

## A. Broken — will not run as printed

### A1. `MultiLCA` (slide: "Calculating LCIA results for multiple activities/methods")

The whole block is the Brightway **2** API. `bw2calc 2.x` rewrote `MultiLCA` completely.

```python
# ON THE CHEATSHEET — raises TypeError
FU = [{x: 1} for x in acts]
bd.calculation_setups["setupname"] = {"inv": FU, "ia": methods}
mLCA = bc.MultiLCA("setupname")
mLCA.results
```

```
TypeError: MultiLCA.__init__() missing 2 required positional arguments:
'method_config' and 'data_objs'
```

```python
# WORKS on bw2calc 2.5
demands = {label: {act.id: 1} for label, act in activities.items()}
config = {"impact_categories": methods}

data_objs = bd.get_multilca_data_objs(functional_units=demands, method_config=config)

mlca = bc.MultiLCA(demands=demands, method_config=config, data_objs=data_objs)
mlca.lci()
mlca.lcia()

# results are a dict keyed (method_tuple, fu_label) — NOT an array
df = pd.Series(mlca.scores).unstack(level=0)
```

Two traps worth calling out on the slide:

- `bd.calculation_setups[...] = {...}` **still succeeds silently**. Only the `bc.MultiLCA("name")`
  line raises, so the error appears one line after the actual problem.
- `mLCA.results` no longer exists; it is `mlca.scores`, and it is a **dict**, not an array. The
  cheatsheet's `data=mLCA.results.T` therefore has no replacement — build the DataFrame from
  `.scores` as above.

### A1b. The appendix repeats it, with a second error (slide: "Command window / Git")

The appendix slide of the 5-slide deck carries another version of the same block:

```python
# ON THE CHEATSHEET (appendix) — AttributeError
bw2calc.multi_lca.calculation_setups["PVs"] = {"inv": FU, "ia": method}
```

`bw2calc.multi_lca` has **no `calculation_setups` attribute at all** — that dictionary lives in
`bw2data`, never in `bw2calc`:

```python
>>> hasattr(bw2calc.multi_lca, "calculation_setups")
False
>>> hasattr(bw2data, "calculation_setups")
True
```

So this line fails even before the `MultiLCA` call does. Delete it and use the A1 replacement.

The appendix's `FU = [...]` comprehension itself is fine, but note it builds a list of
`{Activity: 1}` dicts, whereas the 2.5 `MultiLCA` wants `{label: {id: amount}}`.

### A2. `bd.projects.copy_projects(...)` (slide: "Project management")

No such method. It is singular:

```python
bd.projects.copy_project("newname", switch=True)
```

### A3. Misplaced bracket in the unlinked check (slide: "Import databases")

```python
# ON THE CHEATSHEET — raises TypeError
if len(list(ei311imp.unlinked) == 0):

# CORRECT
if len(list(ei311imp.unlinked)) == 0:
```

The closing bracket sits after `unlinked` rather than after the `list(...)` call, so Python
evaluates `list(...) == 0` first — comparing a list to an integer gives `False` — and then calls
`len()` on that bool:

```
TypeError: object of type 'bool' has no len()
```

It fails this way whether or not there are unlinked exchanges, so the import simply stops here.

### A4. `bd.Method(ilcd).metadata` (slide: "Checking the content of the dbs")

`ilcd` is the **list** produced by the comprehension on the line above. `bd.Method` needs one
tuple:

```
TypeError: unhashable type: 'list'
```

```python
# CORRECT
bd.Method(ilcd[0]).metadata
bd.Method(ilcd[0]).metadata["unit"]
```

The slide's prose already says "choose a list element with e.g. `[1]`" — the code line just does
not do it.

### A5. En-dashes in the conda commands (slides: "Installing…", "Project management")

PowerPoint autocorrects `-c` to `–c`. Pasted into a prompt, conda fails with an unrecognised
argument. Every hyphen in every conda line must be retyped as ASCII `-`. This is the most common
"the cheatsheet doesn't work" report and is invisible on the slide.

### A6. Environment export is missing its redirect (slide: "Project management")

```bash
# ON THE CHEATSHEET — --export takes no filename argument
conda list -n envname --export C:\yourpath\envname_20240401.yml

# CORRECT — redirect, and .txt, because --export is not YAML
conda list -n envname --export > C:\yourpath\envname_20240401.txt

# or, for a real YAML file that `conda env create -f` accepts
conda env export -n envname > C:\yourpath\envname_20240401.yml
```

Note the cheatsheet's restore line (`conda env create -f …yml`) only works with the **second**
form. `--export` output must be restored with `conda create -n newenv --file …txt`.

---

## B. Outdated or unsafe — runs, but should be changed

### B1. "Copy the project to rename it" (slide: "Project management")

Since `bw2data 4.x` there is a direct in-place rename:

```python
bd.projects.rename_project("newname")
```

### B2. Editing the background database in place (slide: "Manipulating datasets/databases")

The snippet is Brightway 2 (`import brightway2 as bw`) and, more importantly, mutates `ei35`
directly. That change is irreversible without a re-import and silently invalidates every result
already calculated in the project.

Use a foreground database instead — see §12 of the notebook:

```python
fg = bd.Database("pv-scenarios")
fg.register()

new = base_activity.copy(code="s1", database="pv-scenarios", name="… scenario 1")
for e in new.technosphere():
    if "Electricity, medium voltage" in e.input["name"]:
        e.input = replacement_activity
        e.save()
```

### B3. `e.get('location')` on an exchange (slide: "Checking the content of the dbs")

This *works* — an `Exchange` proxy falls through to its input node for keys it does not carry —
but it reads as though the exchange has a location. Prefer the explicit form:

```python
e.input["location"]
e.input["unit"]
```

### B4. Plotting all impact categories on one axis (slide: "Plotting results")

`df.plot.bar(...)` runs, but with EF v3.1 the values span `1e-8` (CTUh) to `1e+3`
(m³ water-eq), so every series except the largest collapses onto the axis. Either plot one
indicator per chart, or normalise first — the cheatsheet's own
`df = (df.T / df.abs().max(axis=1)).T` line does this, it is just placed after the plotting call
rather than before it. §9 of the notebook shows both.

---

## B5. Repeated calculations — what 2.5 actually offers

Not on the cheatsheet, and the most useful thing to add. Building a fresh `bc.LCA` for every
run re-factorises the technosphere matrix each time, which is where nearly all the time goes.

**The loop LCA** — build once, factorise once, then swap demand and method:

```python
lca = bc.LCA({first_act: 1}, methods[0])
lca.lci(factorize=True)          # factorise ONCE
lca.lcia()

for act in acts:
    lca.redo_lci({act.id: 1})    # NOTE: .id, not the Activity object
    for m in methods:
        lca.switch_method(m)
        lca.lcia()               # switch_method does NOT recalculate
        print(act["name"], m[1], lca.score)
```

Two traps: `bc.LCA({act: 1}, ...)` accepts an Activity object, but `redo_lci()` requires the
integer `.id` (otherwise `KeyError`); and `switch_method()` only swaps the characterisation
matrix — you must call `lcia()` after it.

**Measured** on BAFU, 7 activities x 4 methods (`aalborg-rlcia-2026`, all four agreeing to
machine precision):

| approach | seconds | speed-up |
|---|---|---|
| fresh `bc.LCA` every time | 3.41 | 1.0x |
| one LCA + `factorize=True` + `redo_lci` | 0.21 | **16.6x** |
| `bc.MultiLCA` | 0.14 | **23.9x** |
| `bc.FastScoresOnlyMultiLCA` | 1.76 | 1.9x |

**Which to recommend:**

- `MultiLCA` when the functional units are known up front — fastest, and it keeps
  `supply_arrays` / `inventories` / `characterized_inventories` per functional unit.
- The loop LCA when functional units are decided inside the loop, or you want one `lca` object to
  introspect between runs. This is also the pattern underneath Monte Carlo and scenario loops.
- `bc.FastScoresOnlyMultiLCA` is built for very large or dense systems (chunked solves,
  pre-multiplied characterisation). On BAFU it is **slower** than `MultiLCA` at 25, 100 and 400
  functional units, so benchmark rather than assume. It has **no `lci()`/`lcia()`** — they raise
  `NotImplementedError`; call `.calculate()`, which returns an `xarray.DataArray`
  (dims `LCIA` x `processes`), not a dict.
- **`bc.CachingLCA` is broken in `bw2calc 2.5.0`** — do not put it on the cheatsheet. Its supply
  cache calls `ResultCache.add(key, ...)` with a scalar id where a list is expected, so any
  single-activity functional unit — the normal case — raises:

  ```
  TypeError: object of type 'int' has no len()
  ```

---

## C. Verified working as printed

| Slide | Commands |
|---|---|
| Working on projects | `set_current`, `create_project`, `delete_project`, `projects.dir`, `projects.report()`, `projects.current`, `list(bd.projects)` |
| Manage databases | `list(bd.databases)`, `del bd.databases[...]`, `Database.copy()`, `Database.rename()` |
| Checking db content | `len()`, `type()`, `.random()`, `.as_dict()`, `list(act.keys())`, `.technosphere()`, `.biosphere()`, `.production()`, `.exchanges()` |
| Searching | `db.search(...)`, `bio.search(..., filter={...})`, all list-comprehension patterns, `set(f['categories'] for f in bio)` |
| Import databases | `bi.bw2setup()`, `bi.SingleOutputEcospold2Importer`, `bi.import_ecoinvent_release`, `bi.ExcelImporter`, `apply_strategies`, `match_database`, `statistics`, `write_database`, `write_excel`, `drop_unlinked` |
| 1 activity & 1 method | `bc.LCA({act: 1}, method)`, `.lci()`, `.lcia()`, `.score` |
| Contribution analysis | `polyviz.utils.calculate_supply_chain`, including the 10-column DataFrame layout |
| Project management | `bi.backup_project_directory`, `bi.restore_project_directory` |
| Method vs methods | `bd.Method(...)` / `bd.methods`, `bd.Database(...)` / `bd.databases`, `.metadata`, `.random()` |
| Wurst | `wurst.extract_brightway2_databases`, `ws.contains / either / exclude / equals`, `write_brightway2_database` |

---

## D. Suggested additions

The cheatsheet marks four topics **"To be filled"**. Three of them are now demonstrated in the
notebook and could be lifted onto the slides:

| Topic | Notebook section | One-line summary for the slide |
|---|---|---|
| Uncertainty analysis | §13 | `bc.MultiLCA(..., use_distributions=True, seed_override=42)`, then `next(mlca)` per iteration — **paired** sampling, so functional units stay comparable |
| Scenario analysis | §12 | Copy into a foreground database, swap exchanges, recalculate |
| Regionalisation | Day 2 notebooks | `edges` 1.4.0 is in the course environment |
| Parametrisation | `D1-10` | `bw2parameters` is installed |

Two further additions worth a line each:

- **`bw2analyzer`** is not on the cheatsheet at all, but `ba.print_recursive_calculation(act, method,
  max_level=3, cutoff=0.05)` is the fastest possible "where does this score come from" and needs no
  extra package. `ContributionAnalysis().annotated_top_processes(lca)` and
  `.annotated_top_emissions(lca)` give the same thing as ranked tables.
- **`lca.switch_method(other_method)`** recalculates a second indicator without re-solving the
  technosphere system — much faster than building a new `bc.LCA` per method.
- **`db.nodes_to_dataframe()`** / **`db.edges_to_dataframe()`** turn a whole database into pandas in
  one call, which beats looping for exploratory filtering.

---

## E. One environment note

If `bc.LCA(...).lci()` fails on Windows with

```
OSError: [WinError -1066598273] Windows Error 0xc06d007f
```

the environment's MKL DLLs are not on `PATH`. This happens when Python is launched **without
activating the conda environment** (for example by calling `envs\bw\python.exe` directly, or from
an IDE configured with the raw interpreter path). Always start from an activated environment:

```bash
conda activate bw
jupyter lab
```

This is not a Brightway bug and the cheatsheet's "always start from the conda prompt" advice is
exactly the mitigation — it may be worth stating the symptom explicitly, since the error message
gives no hint.

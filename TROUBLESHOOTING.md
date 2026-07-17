# Troubleshooting Guide

Use this guide when a setup command or notebook cell fails. 
Start with the first section that matches the symptom, make one change at a time, 
and rerun the smallest relevant check.

If you still need help, send the diagnostic information in [What to send the instructors](#what-to-send-the-instructors) instead of only sending a screenshot.

## First: identify where the failure occurs

- **Terminal failure:** commands such as `conda`, `python`, `git`, or `jupyter` are not found. Work through the installation and activation checks below.
- **Notebook import failure:** Jupyter opens, but `import bw2data`, `import bw2calc`, or `import edges` fails. Check the active kernel.
- **Notebook state failure:** an error such as `NameError`, `KeyError`, or `StopIteration` appears after some cells have run. Check cell order and the active Brightway project.
- **File failure:** an error mentions a missing `.xlsx` or `.json` file. Check where Jupyter was launched and the path printed by `Path.cwd()`.
- **Calculation failure:** imports work, but `lci()`, `lcia()`, or `EdgeLCIA` fails. Preserve the full traceback and check the project/database prerequisites before changing packages.

## Collect a quick environment snapshot

Run these commands in the same terminal used to launch Jupyter:

```bash
python --version
python -c "import sys; print(sys.executable)"
jupyter --version
git status --short
```

Conda users should also run:

```bash
conda env list
conda info
```

Inside a notebook, run:

```python
import sys
from pathlib import Path

print("Python:", sys.version)
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())
```

The Python executable should belong to the `bw` conda environment or `.venv-bw` fallback environment.

## `conda` is not found

- Close and reopen the terminal after installing Miniforge.
- On Windows, use **Miniforge Prompt** for the setup commands.
- On macOS, run `conda init`, close Terminal, and open it again if the installer did not initialize the shell.
- Use the venv/pip route in [INSTRUCTIONS.MD](INSTRUCTIONS.MD) only if your institution blocks conda or Miniforge.

Do not install a second Python distribution merely to fix one missing command; this often makes the Jupyter-kernel problem harder to diagnose.

## Jupyter is using the wrong kernel

Typical symptoms include `ModuleNotFoundError`, an unexpected Python version, or packages being available in the terminal but not in the notebook.

1. Activate the course environment before launching Jupyter:

   ```bash
   conda activate bw
   jupyter lab
   ```

2. In Jupyter, use **Kernel → Change Kernel** and select the kernel belonging to `bw`.
3. Rerun the environment snapshot cell in the setup notebook.

For the venv/pip route, select the `Python (bw)` kernel installed by the command in [INSTRUCTIONS.MD](INSTRUCTIONS.MD).

## A core import fails

Run the import outside Jupyter first:

```bash
python -c "import bw2data, bw2calc, bw2io, edges; print('Course imports: OK')"
```

- If this succeeds in the terminal but fails in Jupyter, the kernel is wrong.
- If this fails in both places, confirm that `bw` is active and that the environment creation command completed without errors.
- If environment creation stopped partway through, save the full terminal output. Recreating the environment from the repository YAML is usually safer than installing missing packages one by one.

## Sparse-solver or `scikit-umfpack` warning

A warning is not necessarily a failed calculation. Continue if the later LCA cell completes.

On Apple Silicon with the conda environment, a `pkg_resources` or `scikits.umfpack` import failure can indicate that `setuptools` drifted beyond the version expected by the environment:

```bash
conda activate bw
conda install "setuptools<81"
python -c "import scikits.umfpack; print('UMFPACK import: OK')"
```

For venv/pip users, an optimized solver might not be available. Continue with the fallback solver unless an actual calculation fails.

## A bundled file is not found

The usual cause is launching Jupyter from a different folder or running a notebook after moving it out of the repository.

- Launch `jupyter lab` from the repository root.
- Keep the notebook in its original course folder.
- Use the working-folder snapshot above to see where relative paths start.
- Confirm that the BAFU workbook exists at `data/lci-bafu.xlsx`.
- Run `git status --short` before pulling updates so you do not overwrite your notebook work.

## `NameError`: a variable does not exist

The defining cell has not run in the current kernel, or the kernel was restarted.

- Read upward to find the cell that creates the named variable.
- Run the notebook from the start in order.
- Do not skip setup or data-selection cells merely because their output looks familiar.
- If you changed a model input, rerun every downstream cell that depends on it.

## `KeyError`, `StopIteration`, or an activity is not found

These errors often mean that a notebook is using the wrong Brightway project, the BAFU database has not been imported, or an exact activity name no longer matches the expected data.

Inside the notebook, inspect:

```python
import bw2data as bd

print("Current project:", bd.projects.current)
print("Databases:", list(bd.databases))
```

For the live course notebooks, the project should be `aalborg-rlcia-2026` and `bafu` should be listed after completing the Day 1 import. Later notebooks depend on that state. Do not delete or recreate the project unless an instructor asks you to.

## A `brightway` or `edges` calculation fails

Check these points before changing any code:

- the notebook cells were run from the beginning and in order;
- the functional-unit activity, database, and LCIA method printed by the notebook are the expected ones;
- Day 1 created `aalborg-rlcia-2026` and imported `bafu`;
- the local JSON asset path exists for methods loaded from `assets/`;
- the method is being evaluated with the same scenario names, years, or parameters shown in the notebook.

For an `edges` mapping problem, keep the generated match or characterization-factor table. It is usually more informative than only reporting the final score.

## A live API section fails

The external PM2.5 example in `D3-02` requires internet access and a responsive third-party service. A timeout or HTTP error does not mean that the local Brightway installation is broken.

- Confirm that ordinary websites are reachable from the same network.
- Retry once after a short interval.
- Keep the HTTP status or exception text.
- Continue with the non-API sections if the service remains unavailable.

## Jupyter appears stuck or a cell runs for a long time

- Look for a `[*]` execution marker and wait for calculations explicitly described as Monte Carlo or supply-chain traversal.
- Do not repeatedly start the same expensive cell.
- Use **Kernel → Interrupt Kernel** if the cell is clearly unresponsive.
- After an interrupt, rerun the notebook from the last clean setup point because partially created variables may be inconsistent.

## `git pull` reports local changes or conflicts

Your notebook work is local and should be preserved before updating. Follow the backup workflow in [INSTRUCTIONS.MD](INSTRUCTIONS.MD#10-updating-the-repository-during-the-course). Do not use `git reset --hard`, and do not discard a notebook through GitHub Desktop unless a separate copy of your work exists.

## What to send the instructors

Email [Romain Sacchi](mailto:romain.sacchi@psi.ch) or [Karin Treyer](mailto:karin.treyer@psi.ch) with:

- operating system and chip type;
- conda or venv/pip installation route;
- output of the environment snapshot commands above;
- notebook name and the section or cell that failed;
- the full traceback as text, including the first and last lines;
- what you expected to happen and what happened instead;
- any change you made immediately before the failure.

This information usually reveals whether the problem is installation, notebook state, file location, or model logic.

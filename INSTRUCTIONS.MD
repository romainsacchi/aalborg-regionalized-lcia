# INSTRUCTIONS BEFORE ARRIVAL

Please complete these steps before the course starts.
The goal is to spend Day 1 learning, not debugging installations.

In case of issue, first refer to the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide. 

If the problem remains, contact: `romain.sacchi@psi.ch`


## Minimum hardware

- Minimum: `16 GB` RAM
- Preferred: `24 GB` RAM

## Before you start

- A stable internet connection is needed to install Git, Miniforge, and the Python packages in the preferred `bw` conda environment.
- If your institution does not allow Anaconda, conda, or Miniforge, use the alternate Python 3.11 + venv/pip route below.
- On Day 1, the notebooks also download a prepared Brightway project archive the first time it is installed into your local Brightway workspace.
- No separate database download is required for the course BAFU workbook; `data/lci-bafu.xlsx` is already included in this repository.

## What these mentioned tools are for

- `Git`: downloads and updates this course repository.
- `Miniforge` / `conda`: installs Python packages in an isolated environment. This is the recommended route.
- `venv` / `pip`: standard Python environment tools. Use this alternate route only if your institution does not allow Anaconda, conda, or Miniforge.
- `Jupyter Lab`: runs the tutorial notebooks.
- `brightway`: is the main Python framework used in the course for LCA modeling and calculation.
- `edges`: runs exchange-based and regionalised LCIA workflows used in Day 2 and Day 3.

## If you are new to Python

If you are completely new to Python, we recommend spending a few hours on a beginner tutorial before the course.
We suggest the University of Helsinki's online tutorial, which requires no installation:

- https://programming-25.mooc.fi/part-1/1-getting-started

For this course, the `Introduction to Programming` section is sufficient.
You do not need to complete the `Advanced Course in Programming` section.

This will make the Day 1 Python and Jupyter refresher much easier to follow.

## 1) Install Git and Miniforge


### Git installation

Note: if you already have `git` installed on your computer, you can skip this step.

Mac users, in a terminal using `brew`:

```bash
brew install git
```

Windows users:

Download and install from: https://git-scm.com/downloads


### Miniforge installation

Note: if you already have `conda`, `miniconda` or `mamba` or other `conda`-like 
environment managers installed on your computer, you can skip this step. 

Mac users, in a terminal:

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-$(uname -m).sh"
bash Miniforge3-MacOSX-$(uname -m).sh
```


Windows users:

- Download and install `Miniforge3-Windows-x86_64.exe`
- After installation, open the **Miniforge Prompt** from the Start Menu. This is the recommended terminal for using `conda` on Windows.


Check that both tools are available.
On Mac, use `Terminal`.
On Windows, use `Miniforge Prompt`.

In that terminal, type:

```bash
git --version
conda --version
```

If `conda` is not found:

- On Mac, close and reopen `Terminal`, then try again.
- On Windows, make sure you are in `Miniforge Prompt`. If you want to use another shell later, run `conda init`, close the shell, and reopen it.

### Alternate route if you cannot use Anaconda, conda, or Miniforge

Install Python `3.11` instead:
- Python: https://www.python.org/downloads/

During Python installation on Windows, enable **Add python.exe to PATH** if your institution allows it.

Check that both tools are available in your terminal:

```bash
git --version
python --version
```

On Windows, if `python --version` does not show Python 3.11, try:

```bash
py -3.11 --version
```

## 2) Open a terminal and understand your location

These commands help you navigate folders:

```bash
pwd        # shows your current folder
ls         # for Mac, lists files/folders in the current folder
dir        # for Windows, lists files/folders in the current folder
cd ..      # go one level up
cd <name>  # go into folder <name>
```

Recommended shell:

- Mac: `Terminal`
- Windows with the preferred conda route: `Miniforge Prompt`

Example: go to `Documents` before cloning:

```bash
cd Documents
```

## 3) Clone this repository

At this point, you might want to create a folder containing your cloned projects. 
Otherwise, they will be listed directly under "Documents".

In your terminal:

```bash
mkdir GitHub
cd GitHub
```
This creates a folder named "GitHub", and you enter it with cd. 

Now, we clone the course repo and enter it:

```bash
git clone https://github.com/romainsacchi/aalborg-regionalized-lcia.git
cd aalborg-regionalized-lcia
```

`git clone` creates a local copy of the course material on your computer (in the GitHub folder created above).
The repository URL above ends with `.git`, which is the standard clone URL shown on the GitHub page.

## 4) Create the course environment (`bw`)

### Recommended route: Miniforge / conda

From the repository root (where you should be from the previous step), go to `envs`:

```bash
cd envs
```

Choose one command, depending on your machine:

- Mac Apple Silicon (M1/M2/M3/M4):

```bash
conda env create -f bw_env_osxARM.yaml
```

- Windows or Mac Intel:

```bash
conda env create -f bw_env_win64.yaml
```

Then verify that the environment exists:

```bash
conda env list
```

You should see `bw` in the list.

### Alternate route: venv / pip

Use this route only if your institution does not allow Anaconda, conda, or Miniforge.
The course notebooks should work with this environment, but some optimized sparse solvers are easier to install with conda.
If a solver warning appears during `brightway` calculations, continue unless a later cell actually fails.

From the repository root:

macOS or Linux:

```bash
python3.11 -m venv .venv-bw
source .venv-bw/bin/activate
python -m pip install --upgrade "pip<26" "setuptools<81" wheel
python -m pip install -r envs/requirements_venv.txt
python -m ipykernel install --user --name bw --display-name "Python (bw)"
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv-bw
.\.venv-bw\Scripts\Activate.ps1
python -m pip install --upgrade "pip<26" "setuptools<81" wheel
python -m pip install -r envs\requirements_venv.txt
python -m ipykernel install --user --name bw --display-name "Python (bw)"
```

If PowerShell blocks the activation script, run this in the same PowerShell window and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

The venv requirements mirror the course `bw` environment as closely as pip can, including the Activity Browser/PySide packages.
The main difference is the optional native sparse solver stack, which is more reliable through conda.
If a GitHub package install is blocked by your institution, send the error log before the course.

## 5) Activate `bw` and run a quick check

Activate in the same shell.

Miniforge / conda:

```bash
conda activate bw
```

Alternate venv / pip route on macOS or Linux:

```bash
source .venv-bw/bin/activate
```

Alternate venv / pip route on Windows PowerShell:

```powershell
.\.venv-bw\Scripts\Activate.ps1
```

Quick checks:

```bash
python --version
python -c "import bw2data, bw2calc, bw2io; print('Brightway core import: OK')"
```

There should be no error messages, and the last line should print `Brightway core import: OK`.


### Apple Silicon note about the sparse solver warning

On Apple Silicon, `bw2calc` may print a warning about missing `scikit-umfpack`.
In a venv/pip setup, you may also see a warning about missing optional optimized solvers.
These warnings usually mean calculations may use a slower fallback solver.

If this happens in the conda environment on Apple Silicon, it usually means the `bw` environment drifted 
and `setuptools` became too new, which breaks the legacy `scikits.umfpack` import.

For conda users, run:

```bash
conda activate bw
conda install "setuptools<81"
```

Then verify:

```bash
python -c "import scikits.umfpack; print('UMFPACK import: OK')"
```


## 6) We will use the BAFU:2025 database imported from an inventory file

This course uses the **BAFU:2025** open-access LCA database as a
`brightway`-compatible Excel inventory file.

Database page:
- https://nexus.openlca.org/database/BAFU

The Brightway-compatible Excel file is already included in this repository:
- `data/lci-bafu.xlsx`

You do **not** need to download the database from the website above for this course.
The link is provided as a reference and for the terms of use.

## 7) Launch Jupyter Lab and run setup notebook

From the *repository root* (you might still be in `envs/` after creating the conda environment, so go back up one level, using `cd ..`):

```bash
# Activate bw first: conda activate bw, or activate .venv-bw.
jupyter lab
```

Then open and run all cells in:

- `tutorials/00_SETUP/00 - Setup and First Checks.ipynb`

The final section runs a tiny LCA in an isolated Brightway project. 

Keep the same `bw` environment for the full course.


## 8) Before the course starts

Please complete:
- [READING_MATERIAL.md](READING_MATERIAL.md)
- [tutorials/00_SETUP/00 - Setup and First Checks.ipynb](tutorials/00_SETUP/00%20-%20Setup%20and%20First%20Checks.ipynb)

Your readiness check is complete when the notebook prints `READINESS CHECK: PASS`.


## 9) Terms of use and citation requirements (BAFU:2025)

The Swiss Federal Administration provides its eco-inventory data free of charge and with few restrictions.
Anyone wishing to use the data must first accept the terms of use.

Requirements:
- The data may not be resold.
- The source of the data must be cited as:
  `Database of the Swiss Federal Administration, FOEN:20XY, Federal Office for the Environment, 2025.`
- The Swiss Federal Administration cannot be held responsible for the published data.
- It is recommended that specialists be consulted for the implementation of life cycle assessments and the analysis of the results.

## 10) If something fails or if you are stuck, email this information

Send to `romain.sacchi@psi.ch`:

- Operating system and chip type (`Windows`, `Mac Intel`, `Mac Apple Silicon`)
- Environment route used (`conda` or `venv/pip`)
- Output of `conda env list` if you used conda
- Output of `python --version`
- Full error message from terminal or notebook

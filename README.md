# Plot Figure Experiment

This directory is a local GitHub Pages project site for:

`https://github.com/hamster111111/plot-figure-experiment`

The published project URL will be:

`https://hamster111111.github.io/plot-figure-experiment/`

It publishes the HTML files currently stored under `D:\Code\autoReaserch\web`.

It follows the same high-level pattern you asked about:

- edit source pages locally
- sync them into a publish directory
- generate `index.html`
- push `main`
- let GitHub Actions deploy Pages

## Directory Layout

```text
plot-figure-experiment/
├── .github/workflows/deploy.yml
├── scripts/
│   ├── gen_index.py
│   └── sync_from_workspace.py
└── work/
    ├── index.html
    └── ...
```

`work/` is the published site root.

## Local Usage

From this directory:

```powershell
python scripts/sync_from_workspace.py
python scripts/gen_index.py
```

Or just run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update_site.ps1
```

By default, the sync script copies from `../web` into `./work`.

## GitHub Usage

After local setup:

```powershell
git init
git add .
git commit -m "Initial Pages site"
git branch -M main
git remote add origin https://github.com/hamster111111/plot-figure-experiment.git
git push -u origin main
```

## Notes

- GitHub Actions only regenerates `work/index.html`.
- The actual page files in `work/` are committed to git.
- When `D:\Code\autoReaserch\web` changes, rerun the sync script locally, commit,
  and push again.

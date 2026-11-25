# HY-562 Project B: SumQA

Semantic graph summaries as schema context for LLM-generated SPARQL. This
repository uses the professor's November data update: ORKG/SciQA and DBLP/DBLP-QuAD.
The update announcement is preserved in [kit/DATA_UPDATE.md](kit/DATA_UPDATE.md).

## Start the environment

From the repository root:

```powershell
docker compose -f 04_Environment/04_Environment/docker-compose.yml up -d
docker exec -w /home/jovyan/work/kit hy562-spark-lab python -m pip install -r requirements.txt
```

Open http://localhost:8888/lab?token=hy562 and work in `kit/`. The course image
contains Spark 4.2.0, Java 17 and JupyterLab. Reinstall the kit requirements if
the container is recreated.

This machine runs Ollama on port **11435**, with models in `kit/cache/ollama`.
Restart it from PowerShell in the repository root:

```powershell
New-Item -ItemType Directory -Force kit/cache/ollama | Out-Null
$env:OLLAMA_MODELS = (Resolve-Path kit/cache/ollama).Path
$env:OLLAMA_HOST = '0.0.0.0:11435'
ollama serve
```

The container reaches it at `http://host.docker.internal:11435`. Teammates using
Ollama's default port should set that address to port 11434 in Compose.

## Data and verification

Follow [kit/SETUP.md](kit/SETUP.md) for the current commands. Active graph IDs are
`orkg2023` and `dblp2022`. Raw downloads, stores, Parquet and model files are ignored
by Git; the source and checksum manifest [MANIFEST.tsv](kit/data/kg/MANIFEST.tsv)
is included for comparison across teams.

Both graph folders include tracked setup metadata:
[DBLP](kit/data/kg/dblp2022/README.md) and
[ORKG](kit/data/kg/orkg2023/README.md). Their `counts.json` and
`schema_elements.jsonl` files are included in Git. A clone still needs the raw
data, query stores and Parquet: follow the setup commands to download/build them,
or copy the complete prepared folders from a teammate using shared storage.

[SETUP_REPORT.txt](kit/SETUP_REPORT.txt) records the latest checks. The short model
run is saved in [setup_smoke.jsonl](kit/results/setup_smoke.jsonl) and
[setup_smoke.csv](kit/results/setup_smoke.csv). Gold and dropped-question files
are kept alongside each converted benchmark in `kit/data/benchmarks/`.

Verified on 22 November 2026:

- All setup checks pass for ORKG and DBLP.
- SciQA: 463 questions retained, 50 dropped (40 empty results, 10 syntax errors).
- DBLP-QuAD: 270 questions retained, 30 dropped.
- Toy pipeline: 12/12 correct; the updated starter notebook runs successfully.
- Model smoke test: 3/10 correct, with 8.50 seconds per uncached response on average.
- Regression tests pass for local-query timeouts and long RDF literals.

The professor requests `MANIFEST.tsv` in the Project B forum. Include
`kit/data/benchmarks/sciqa_test.dropped.jsonl` too, since 50 questions were dropped.

The toy fixture belongs in `kit/data/toy/`. `B1` in the supplied toy examples is
a sample identifier; use the team's assigned identifier for full experiments.

Regression tests cover local-query timeouts and long RDF literals:

```powershell
docker exec -w /home/jovyan/work/kit hy562-spark-lab python -m unittest discover -s tests -v
```

The grading work beyond setup is the baseline grid, the team's summary variant,
the ablation on 40 SciQA questions, the presentation and the final report.

# Project B setup: ORKG/SciQA and DBLP

These are the active instructions after the November data update. The original
announcement and amended experiment protocol are in [DATA_UPDATE.md](DATA_UPDATE.md).
Run Python commands below from `kit/` inside the course container. Keep the data
on a local disk outside cloud-synced folders.

## 1. Environment and model

From the repository root on the host:

```powershell
docker compose -f 04_Environment/04_Environment/docker-compose.yml up -d
docker exec -w /home/jovyan/work/kit hy562-spark-lab python -m pip install -r requirements.txt
```

Open http://localhost:8888/lab?token=hy562. Install and start Ollama on the host,
then pull `qwen2.5-coder:7b`. This repository's Compose configuration reaches
Ollama at `http://host.docker.internal:11435`; see the root README to start it
with the project model folder. Reinstall requirements after container recreation.

## 2. Toy validation

```bash
export TOY_ENDPOINT=file:data/toy/kg.nt
python -m sumqa.gold --bench data/toy/toy_test.jsonl --endpoint "$TOY_ENDPOINT"
python -m sumqa.run --bench data/toy/toy_test.gold.jsonl --kg toy --context retrieval --budget 150 --model mock:gold --team B1
python -m sumqa.score runs/B1/toy_test__retrieval__150__mock-gold.jsonl
```

Accuracy must be 1.0. Run `ProjectB_starter.ipynb` from top to bottom once.

## 3. Downloads and manifest

```bash
python get_data.py check
python get_data.py projectB
bash scripts/download_benchmarks.sh
```

The source check must show four OK lines. Downloads resume and are checksum
verified; `data/kg/MANIFEST.tsv` records URLs, byte counts and MD5 values.
The manifest is tracked even though the graph files are ignored.

## 4. Graph preparation

```bash
python -m sumqa.kgstore --store data/kg/orkg2023/store data/kg/orkg2023/raw/*.nt
python -m sumqa.kgstats --out data/kg/orkg2023/counts.json --parquet data/kg/orkg2023/parquet "data/kg/orkg2023/raw/*.nt"
python -m sumqa.build_schema --counts data/kg/orkg2023/counts.json --labels-store data/kg/orkg2023/store --out data/kg/orkg2023/schema_elements.jsonl
```

For DBLP, reuse an already verified store, counts, Parquet and schema. Otherwise:

```bash
python -m sumqa.kgstore --store data/kg/dblp2022/store data/kg/dblp2022/raw/dblp.nt.gz
python -m sumqa.kgstats --out data/kg/dblp2022/counts.json --parquet data/kg/dblp2022/parquet --driver-memory 8g data/kg/dblp2022/raw/dblp.nt.gz
curl -fL -o data/kg/dblp2022/raw/schema.ttl https://dblp.org/rdf/schema.ttl
python -m sumqa.build_schema --ontology data/kg/dblp2022/raw/schema.ttl --counts data/kg/dblp2022/counts.json --out data/kg/dblp2022/schema_elements.jsonl
```

DBLP processing is large and can take hours. A gzip stream is not splittable by
Spark; for faster parsing, decompress it into temporary N-Triples chunks and
give those paths to `sumqa.kgstats` (the triples are unchanged):

```bash
mkdir -p /tmp/sumqa-dblp
gzip -dc data/kg/dblp2022/raw/dblp.nt.gz | split -l 1000000 -d -a 4 --additional-suffix=.nt - /tmp/sumqa-dblp/part-
python -m sumqa.kgstats --out data/kg/dblp2022/counts.json --parquet data/kg/dblp2022/parquet --driver-memory 8g "/tmp/sumqa-dblp/*.nt"
```

## 5. Gold answers

Compose sets both endpoints. In another environment, export them explicitly:

```bash
export ORKG_ENDPOINT=oxigraph:data/kg/orkg2023/store
export DBLP_ENDPOINT=oxigraph:data/kg/dblp2022/store
python -m sumqa.gold --bench data/benchmarks/sciqa_test.jsonl --endpoint "$ORKG_ENDPOINT"
python -m sumqa.gold --bench data/benchmarks/dblpquad_test.jsonl --endpoint "$DBLP_ENDPOINT"
```

Inspect each `*.dropped.jsonl`. SciQA test has 513 input questions. The professor
asks teams to post the dropped list in the forum if more than a few dozen fail.

## 6. Model smoke test and report

```bash
python -m sumqa.run --bench data/benchmarks/sciqa_test.gold.jsonl --kg orkg2023 --context retrieval --budget 1000 --model ollama:qwen2.5-coder:7b --team setup --limit 10 --out results/setup_smoke.jsonl
python -m sumqa.score results/setup_smoke.jsonl --results results/setup_smoke.csv
python scripts/check_setup.py
```

Review `SETUP_REPORT.txt`, the manifest and smoke-test results, then commit them.
The professor also requests the manifest in the Project B forum thread. Use your
assigned team identifier for full experiments. The update replaces the primary
benchmark with SciQA, including the 40-question ablation; DBLP-QuAD is unchanged.

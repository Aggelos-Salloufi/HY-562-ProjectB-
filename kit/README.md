# Project B kit: SumQA

HY562 / CS-562 Fall 2026. This kit runs English question to SPARQL experiments
with local language models. Start with [SETUP.md](SETUP.md); the professor's
data-update announcement is [DATA_UPDATE.md](DATA_UPDATE.md).

## Active data

| Graph | Version | Benchmark |
|---|---|---|
| Open Research Knowledge Graph | 14 February 2023 dump | SciQA: 1,795 train, 513 test questions |
| dblp | 1 August 2022 dump | DBLP-QuAD: 7,000 train, 300 sampled test questions |
| Supplied toy graph | Kit fixture | 12 questions |

`python get_data.py projectB` downloads the official files, verifies published
checksums and writes `data/kg/MANIFEST.tsv`. Commit the manifest and setup report.
Each graph folder's README, counts and schema are included in Git. Large graph
files and model weights stay outside Git; teammates download/build them with the
setup commands or copy the complete prepared graph folders through shared storage.

## Pipeline

- `sumqa.kgstore` loads the RDF files into a local Oxigraph store.
- `sumqa.kgstats` computes class/property counts with Spark and writes Parquet.
- `sumqa.build_schema` writes schema elements for the baselines. Use
  `--labels-store` for ORKG so opaque predicate codes have readable labels.
- `sumqa.prepare_benchmarks` converts SciQA and DBLP-QuAD into the shared format.
- `sumqa.gold` executes reference queries and saves kept and dropped questions.
- `sumqa.run` generates and executes model queries; `sumqa.score` scores them.
- `sumqa.ablation` removes context blocks to measure their contribution.

## Experiments

Use `--kg orkg2023 --bench data/benchmarks/sciqa_test.gold.jsonl` for the primary
graph, and `--kg dblp2022 --bench data/benchmarks/dblpquad_test.gold.jsonl` for the
second graph. Both settings provide the same entity links across context methods.
SciQA often identifies resources through labels, so its entity list can be empty.

The common contexts are `ontology` (schema ordered by usage) and `retrieval`
(BM25). Your variant uses `summary` or question-specific `lines`. Context budgets
are 500, 1,000 and 2,000 tokens. Keep the supplied prompt, examples and scorer.
The common model is `ollama:qwen2.5-coder:7b`; use the prescribed second model
at budget 1,000 for the later experiments.

Every scored full run should append to `results/results_B.csv`. Keep its run
file, report summary construction time and size, and inspect the dropped-question
lists. A 10-question setup smoke test checks connectivity and timing, not the full
experiment grid. Follow the updated minimum runs in `DATA_UPDATE.md`.

## Implementation notes

`common.py`, benchmark conversion and ORKG label lookup come from the professor's
update. Local Oxigraph queries run in a subprocess so the configured timeout is
enforced. The Spark literal regex uses possessive repetition to handle long ORKG
abstracts without a Java regex stack overflow. Regression tests are in `tests/`.

Summary JSON contains graph/team identifiers, nodes with classes or properties,
and counted edges. See `sumqa/context.py` for the format and serialization rules.

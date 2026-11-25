# ORKG setup files

This folder holds the local ORKG RDF dump of 14 February 2023 and its derived files.
Source URL, archive size and MD5 are recorded in [MANIFEST.tsv](../MANIFEST.tsv).

Included in Git:

- `counts.json`: class and property counts computed by Spark.
- `schema_elements.jsonl`: schema context with readable labels for ORKG codes.
- This README.

Created locally by [SETUP.md](../../../SETUP.md):

- `raw/`: the checksum-verified archive and unpacked N-Triples.
- `store/`: the Oxigraph query database used for SciQA.
- `parquet/`: triples used by the team's Spark summary code.

A Git clone includes the setup metadata. Run `python get_data.py projectB` from
`kit/`, then follow the ORKG preparation commands to obtain the full local graph.
To reuse an existing prepared setup, copy this complete folder from a teammate
through shared storage while no process is writing to the store.

# DBLP setup files

This folder holds the local DBLP RDF dump of 1 August 2022 and its derived files.
Source URL, archive size and MD5 are recorded in [MANIFEST.tsv](../MANIFEST.tsv).

Included in Git:

- `counts.json`: class and property counts computed by Spark.
- `schema_elements.jsonl`: schema context for the baselines.
- This README.

Created locally by [SETUP.md](../../../SETUP.md):

- `raw/`: the compressed RDF dump and schema ontology.
- `store/`: the Oxigraph query database.
- `parquet/`: triples used by the team's Spark summary code.

A Git clone includes the setup metadata. Run `python get_data.py projectB` from
`kit/`, then follow the DBLP preparation commands to obtain the full local graph.
To reuse an existing prepared setup, copy this complete folder from a teammate
through shared storage while no process is writing to the store.

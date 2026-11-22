# Active benchmark and graph sources

| Data | Source | License |
|---|---|---|
| ORKG dump, 14 February 2023 | https://zenodo.org/records/7744048 | CC BY 4.0 |
| SciQA: 1,795 training and 513 test questions | https://zenodo.org/records/7744048 | CC BY 4.0 |
| DBLP RDF, 1 August 2022 | https://zenodo.org/records/7638511 | CC BY 4.0 |
| DBLP-QuAD: 7,000 train, 1,000 validation, 2,000 test | https://zenodo.org/records/7643971 and https://huggingface.co/datasets/awalesushil/DBLP-QuAD | CC BY 4.0 |

`kit/get_data.py` is the professor's November updater. It verifies the ORKG and
SciQA ZIP checksums and writes URLs, byte counts and MD5 values to
`data/kg/MANIFEST.tsv`. The DBLP dump's published MD5 is
`8194e6e98fef690ba3d24afe488fa2d8`.

`sumqa.prepare_benchmarks` adds SciQA prefixes and extracts the shared entity links.
It retains all SciQA test questions and uses the supplied fixed-seed sample of
300 DBLP-QuAD test questions. Gold answers are computed on the local stores;
kept and dropped records are saved separately.

Cite S. Auer, D. A. C. Barone, C. Bartz, et al., "The SciQA Scientific Question
Answering Benchmark for Scholarly Knowledge", Scientific Reports 13, 7240 (2023),
and D. Banerjee, S. Awale, R. Usbeck, C. Biemann, "DBLP-QuAD: A Question Answering
Dataset over the DBLP Scholarly Knowledge Graph", arXiv:2303.13351 (2023).

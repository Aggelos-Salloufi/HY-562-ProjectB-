"""Load a KG into a local Oxigraph store (an embedded SPARQL engine, `pip install pyoxigraph`).

    python -m sumqa.kgstore --store data/kg/orkg2023/store data/kg/orkg2023/raw/*.nt
    python -m sumqa.kgstore --store data/kg/dblp2022/store data/kg/dblp2022/raw/dblp.nt.gz

Then use the endpoint `oxigraph:data/kg/orkg2023/store` in every command of the kit
(for example `export ORKG_ENDPOINT=oxigraph:data/kg/orkg2023/store`).
No server, no Docker: the store is a folder on disk that the kit opens read-only.

Files may be .nt, .ttl, .nq, plain or compressed (.bz2, .gz). Malformed triples are
skipped (lenient mode). Large graphs can need many GB of disk and long loading
times. Run it once per team member machine (or copy the prepared folder).
"""
import argparse
import bz2
import gzip
import os
import time


def _open(path):
    if path.endswith(".bz2"):
        return bz2.open(path, "rb")
    if path.endswith(".gz"):
        return gzip.open(path, "rb")
    return open(path, "rb")


def _format(path):
    import pyoxigraph as ox
    base = path.removesuffix(".bz2").removesuffix(".gz")
    if base.endswith(".nq"):
        return ox.RdfFormat.N_QUADS
    if base.endswith(".nt"):
        return ox.RdfFormat.N_TRIPLES
    return ox.RdfFormat.TURTLE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    import pyoxigraph as ox
    os.makedirs(a.store, exist_ok=True)
    store = ox.Store(a.store)
    for f in a.files:
        t0 = time.time()
        print(f"loading {f} ...", flush=True)
        with _open(f) as fh:
            store.bulk_load(fh, _format(f), lenient=True)
        print(f"  done in {time.time() - t0:.0f}s", flush=True)
    store.optimize()
    n = next(iter(store.query("SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }")))[0]
    print(f"{n.value} triples in {a.store}")


if __name__ == "__main__":
    main()

import tomllib
from pathlib import Path

import geopandas as gpd
import pandas as pd


def _last_mtime(_dir):
    return max(f.stat().st_mtime for f in _dir.iterdir() if f.is_file())


def _read_layers(filename, columns, layers):
    if not layers:
        layers = gpd.list_layers(filename)["name"]

    for layer in layers:
        df = gpd.read_file(filename, columns=columns, layer=layer)
        df.insert(0, "gdb_layer", layer)
        yield df.to_crs(epsg=4326)


def main():
    _dir = Path(__file__).parent

    try:
        with open(_dir / "config.toml", "rb") as f:
            config = tomllib.load(f)

        conversions = config.pop("conversion", None)
        assert isinstance(conversions, list), "Unexpected type: conversion"
        assert not config, f"Unexpected keys: {', '.join(config)}"
    except Exception as e:
        raise RuntimeError(f"[config.toml] Error: {e}")

    for i, conv in enumerate(conversions, start=1):
        try:
            _from = conv.pop("from", None)
            to = conv.pop("to", None)

            layers = conv.pop("layers", None)
            columns = conv.pop("columns", None)

            assert isinstance(_from, str), 'Missing from = "..."'
            assert isinstance(to, str), 'Missing to = "..."'

            if layers is not None:
                assert isinstance(layers, list), "Unexpected type: layers"

            if columns is not None:
                assert isinstance(columns, list), "Unexpected type: columns"

            assert not conv, f"Unexpected keys: {', '.join(conv)}"

            _from = Path(_from)
            to = Path(to)

            if not _from.is_absolute():
                _from = (_dir / _from).resolve()

            if not to.is_absolute():
                to = (_dir / to).resolve()

            print(f"[Conversion {i}] {_from} -> {to}")

            if to.exists() and to.stat().st_mtime >= _last_mtime(_from):
                print(f"[Conversion {i}] GeoJSON is newer than Geodatabase")
                print(f"[Conversion {i}] Skipped")
                continue

            pd.concat(_read_layers(_from, columns, layers)).to_file(to)

            print(f"[Conversion {i}] Done")
        except Exception as e:
            print(f"[Conversion {i}] Error: {e}")
            print(f"[Conversion {i}] Skipped")


if __name__ == "__main__":
    main()

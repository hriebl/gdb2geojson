import tomllib
from pathlib import Path

import geopandas as gpd


def main():
    directory = Path(__file__).parent

    try:
        with open(directory / "config.toml", "rb") as f:
            config = tomllib.load(f)

        conversions = config.pop("conversion", None)
        assert isinstance(conversions, list), "Unexpected type: conversion"
        assert not config, f"Unexpected keys: {', '.join(config)}"
    except Exception as e:
        raise RuntimeError(f"[config.toml] Error: {e}")

    for i, d in enumerate(conversions, start=1):
        try:
            _from = d.pop("from", None)
            to = d.pop("to", None)

            layer = d.pop("layer", None)
            columns = d.pop("columns", None)

            assert isinstance(_from, str), 'Missing from = "..."'
            assert isinstance(to, str), 'Missing to = "..."'

            if columns is not None:
                assert isinstance(columns, list), "Unexpected type: columns"

            assert not d, f"Unexpected keys: {', '.join(d)}"

            _from = Path(_from)
            to = Path(to)

            if not _from.is_absolute():
                _from = (directory / _from).resolve()

            if not to.is_absolute():
                to = (directory / to).resolve()

            if layer is not None:
                print(f"[Conversion {i}] {_from} (Layer: {layer}) -> {to}")
            else:
                print(f"[Conversion {i}] {_from} (First Layer) -> {to}")

            df = gpd.read_file(_from, columns=columns, layer=layer)
            df = df.to_crs(epsg=4326)
            df.to_file(to)

            print(f"[Conversion {i}] Done")
        except Exception as e:
            print(f"[Conversion {i}] Error: {e}")
            print(f"[Conversion {i}] Skipped")


if __name__ == "__main__":
    main()

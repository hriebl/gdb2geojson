import tomllib
from pathlib import Path

import geopandas as gpd


def main():
    directory = Path(__file__).parent

    try:
        with open(directory / "config.toml", "rb") as f:
            config = tomllib.load(f)

        conversions = config.pop("convert", None)
        assert isinstance(conversions, list), "Only [[convert]] entries allowed"
        assert not config, "Only [[convert]] entries allowed"
    except Exception as e:
        raise RuntimeError(f"Invalid config.toml: {e}")

    for c in conversions:
        try:
            _from = c.get("from", None)
            to = c.get("to", None)

            assert isinstance(_from, str), '[[convert]] entry needs from = "..."'
            assert isinstance(to, str), '[[convert]] entry needs to = "..."'

            _from = Path(_from)
            to = Path(to)

            if not _from.is_absolute():
                _from = (directory / _from).resolve()

            if not to.is_absolute():
                to = (directory / to).resolve()

            layer = c.get("layer", None)

            if layer is not None:
                print(f"Converting {_from} to {to} (layer {layer})")
            else:
                print(f"Converting {_from} to {to} (first layer)")

            df = gpd.read_file(_from, layer=layer)
            df = df.to_crs(epsg=4326)
            df.to_file(to)

            print("Done!")
        except Exception as e:
            print(f"Conversion failed: {e}")
            print("Skipped!")


if __name__ == "__main__":
    main()

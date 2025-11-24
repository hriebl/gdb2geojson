import tomllib

import geopandas as gpd


def main():
    try:
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)

        conversions = config.pop("convert", None)
        assert isinstance(conversions, list), "Only [[convert]] entries allowed"
        assert not config, "Only [[convert]] entries allowed"
    except Exception as e:
        print(f"Invalid config.toml: {e}")
        raise SystemExit(1)

    for c in conversions:
        try:
            _from = c.get("from", None)
            to = c.get("to", None)

            assert isinstance(_from, str), '[[convert]] entry needs from = "..."'
            assert isinstance(to, str), '[[convert]] entry needs to = "..."'

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

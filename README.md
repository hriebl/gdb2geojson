# gdb2geojson

Convert multiple Geodatabases to GeoJSON.

### Usage

Edit config.toml and run main.py. Make sure that the geopandas package for Python is installed (`pip install geopandas`).

### Configuration

Here is an example config.toml. Add more `[[convert]]` entries as needed.

```
[[convert]]
from = "NRS.gdb"
to = "NRS.geojson"
layer = "Niederrhein_Schollen"
```

### License of NRS.gdb

NRS.gdb is provided as an example Geodatabase. The data originally comes from "Niederrheinische Schollen @ Geologischer Dienst NRW" and is licensed under [Datenlizenz Deutschland Namensnennung 2.0](https://www.govdata.de/dl-de/by-2-0). It may be downloaded from [here](https://www.opengeodata.nrw.de/produkte/geologie/geologie/WGD/NRS).

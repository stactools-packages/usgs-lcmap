# stactools-usgs-lcmap

[![PyPI](https://img.shields.io/pypi/v/stactools-usgs-lcmap)](https://pypi.org/project/stactools-usgs-lcmap/)

- Name: usgs-lcmap
- Package: `stactools.usgs_lcmap`
- [stactools-usgs-lcmap on PyPI](https://pypi.org/project/stactools-usgs-lcmap/)
- Owner: @pjhartzell
- [Dataset homepage](https://www.usgs.gov/special-topics/lcmap)
- STAC extensions used:
  - [classification](https://github.com/stac-extensions/classification)
  - [file](https://github.com/stac-extensions/file)
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [proj](https://github.com/stac-extensions/projection/)
  - [raster](https://github.com/stac-extensions/raster)
  - [scientific](https://github.com/stac-extensions/scientific)
  - [table](https://github.com/stac-extensions/table)
- Extra fields:
  - `usgs_lcmap:collection`: LCMAP Collection
  - `usgs_lcmap:horizontal_tile`: LCMAP (Landsat ARD) horizontal tile number
  - `usgs_lcmap:vertical_tile`: LCMAP (Landsat ARD) vertical tile number
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/usgs-lcmap/main/examples/catalog.json)

## Summary

The [Land Change Monitoring, Assessment, and Projection (LCMAP)](https://www.usgs.gov/special-topics/lcmap) project provides an integrated suite of annual land cover and land surface change products for the conterminous United States and Hawaii based on time series data from the Landsat record. LCMAP Science Products are based on the USGS implementation of the [Continuous Change Detection and Classification (CCDC)](https://doi.org/10.1016/j.rse.2014.01.011) algorithm.

This stactools package provides tooling for creating STAC Collections and Items for USGS LCMAP products that are tiled to match [Landsat ARD](https://www.usgs.gov/landsat-missions/landsat-us-analysis-ready-data) tiles. An LCMAP tile consists of a TAR archive and an XML metadata file. The TAR archive contains [COGs](https://www.cogeo.org/) and XML files for the 10 LCMAP products, a "browse" COG, and a text file containing Landsat observation dates used as input to the CCDC algorithm.

Creating a STAC Item will cause the TAR archive contents to be extracted to a new directory that sits alongside the TAR archive and XML metadata file, or expects this extraction to already have been performed. Note that the STAC Items do not simply describe the COGs in their extracted form. The COGs are reprocessed to correct the projection (WGS84 spheroid parameters), add nodata values to some of the COGs, and add overviews. This extraction and reprocessing can be turned off, but will result in a STAC Item that does not correctly describe the data, unless the TAR archive was previously extracted and the COGs reprocessed.

## STAC Examples

- CONUS
  - [Collection](examples/usgs-lcmap-conus/collection.json)
  - [Item](examples/usgs-lcmap-conus/LCMAP_CU_001004_1999_V13_CCDC/LCMAP_CU_001004_1999_V13_CCDC.json)
- Hawaii
  - [Collection](examples/usgs-lcmap-hawaii/collection.json)
  - [Item](examples/usgs-lcmap-hawaii/LCMAP_HI_000000_2020_V10_CCDC/LCMAP_HI_000000_2020_V10_CCDC.json)

The example Collections and Items in the `examples` directory can be created by running `./scripts/create_examples.py`.

## Installation

```shell
pip install git+https://github.com/stactools-packages/usgs-lcmap
```

## Command-line Usage

To create a collection:

```shell
stac usgs-lcmap create-collection <CONUS|Hawaii> collection.json
```

To create an Item:

```shell
stac usgs-lcmap create-item <path-to-tar> item.json
```

Use `stac usgs-lcmap --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```

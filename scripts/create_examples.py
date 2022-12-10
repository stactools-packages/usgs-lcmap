#!/usr/bin/env python3

"""Creates the example STAC and COGs"""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from pystac import Catalog, CatalogType

from stactools.usgs_lcmap import constants, stac

root = Path(__file__).parent.parent
examples = root / "examples"
data_files = root / "tests" / "data-files"

description = (
    "The LCMAP project provides an integrated suite of annual land cover and "
    "land surface change products for the conterminous United States and "
    "Hawaii based on time series data from the Landsat record. LCMAP Science "
    "Products are based on the USGS implementation of the Continuous Change "
    "Detection and Classification (CCDC) algorithm."
)

with TemporaryDirectory() as tmp_dir:
    catalog = Catalog("usgs-lcmap", description, "USGS LCMAP Science Products")

    print("Creating CONUS collection...")
    conus = stac.create_collection(constants.Region.CU)
    conus_item = stac.create_item(
        str(data_files / "CU" / "LCMAP_CU_001004_1999_20220723_V13_CCDC.tar")
    )
    conus_item.properties.pop("created")
    conus.add_item(conus_item)
    catalog.add_child(conus)

    print("Creating Hawaii collection...")
    hawaii = stac.create_collection(constants.Region.HI)
    hawaii_item = stac.create_item(
        str(data_files / "HI" / "LCMAP_HI_000000_2020_20211130_V10_CCDC.tar")
    )
    hawaii_item.properties.pop("created")
    hawaii.add_item(hawaii_item)
    catalog.add_child(hawaii)

    print("Saving catalog...")
    catalog.normalize_hrefs(str(examples))
    shutil.rmtree(examples)
    for item in catalog.get_all_items():
        item.make_asset_hrefs_relative()
    catalog.save(catalog_type=CatalogType.SELF_CONTAINED)

    print("Done!")

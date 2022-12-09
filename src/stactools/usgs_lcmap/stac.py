import logging
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import pystac
from pystac import Item
from pystac.extensions.projection import ProjectionExtension
from stactools.core.io import ReadHrefModifier

from stactools.usgs_lcmap import cog, constants, utils

logger = logging.getLogger(__name__)


def create_item(tar_path: str, recog: bool = True) -> Item:
    """Create a STAC Item from a local TAR file. The contents of the TAR will be
    extracted and placed alongside the TAR. The existing TIF files will be
    overwritten with reprocessed COGs if `recog` is True.

    Args:
        tar_path (str): Local path to a TAR archive
        recog (bool): Flag to reprocess the COGs. Default is True.

    Returns:
        Item: STAC Item object
    """
    with tarfile.open(tar_path) as tar:
        tar.extractall(path=Path(tar_path).parent)

    asset_list = Path(tar_path).parent.glob("*.*")
    asset_list = [f.as_posix() for f in asset_list]
    if recog:
        for tif in [f for f in asset_list if Path(f).suffix == ".tif"]:
            cog.recog(tif)

    return create_item_from_asset_list(asset_list)


def create_item_from_asset_list(
    asset_list: List[str], read_href_modifier: Optional[ReadHrefModifier] = None
) -> None:
    asset_dict = utils.get_asset_dict(asset_list)
    metadata = utils.Metadata.from_cog(
        asset_dict["lcpri"].href, read_href_modifier
    )

    item = Item(
        id=metadata.id,
        geometry=metadata.geometry,
        bbox=metadata.bbox,
        datetime=None,
        properties={
            "start_datetime": metadata.start_datetime,
            "end_datetime": metadata.end_datetime,
            "usgs-lcmap:collection": metadata.lcmap_collection,
            "usgs-lcmap:horizontal_tile": metadata.horizontal_tile,
            "usgs-lcmap:vertical_tile": metadata.vertical_tile,
            "usgs-lcmap:production_datetime": metadata.production_datetime
        }
    )
    item.common_metadata.created = datetime.now(tz=timezone.utc)
    item.common_metadata.title = metadata.title

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = None
    projection.wkt2 = metadata.proj_wkt2
    projection.shape = metadata.proj_shape
    projection.transform = metadata.proj_transform

    for key, value in asset_dict.items():
        item.add_asset(key, value)

    item.stac_extensions.append(constants.RASTER_EXTENSION_V11)
    item.stac_extensions.append(constants.CLASSIFICATION_EXTENSION_V11)

    # TODO: update the geometry with stactools raster footprint?

    return item


def create_collection(region: constants.Region) -> pystac.Collection:
    """Create a STAC Collection for CONUS or Hawaii.

    Returns:
        Collection: STAC Collection object.
    """
    if region is constants.Region.CU:
        collection = pystac.Collection(**constants.COLLECTION_CONUS)
        collection.add_links([constants.ABOUT_LINK_CONUS, constants.LICENSE_LINK_CONUS])
    else:
        collection = pystac.Collection(**constants.COLLECTION_HAWAII)
        collection.add_links(
            [constants.ABOUT_LINK_HAWAII, constants.LICENSE_LINK_HAWAII]
        )

    collection.providers = [constants.PROVIDER]

    # TODO: item_assets
    # TODO: stac extensions
    # TODO: summaries?

    return collection


if __name__ == "__main__":
    tar_path = "/Users/pjh/dev/usgs-lcmap/tests/data-files/LCMAP/CONUS/LCMAP_CU_002004_2021_20220723_V13_CCDC.tar"
    item = create_item(tar_path=tar_path, recog=False)
    import json
    print(json.dumps(item.to_dict(), indent=4))

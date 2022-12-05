import logging
from datetime import datetime, timezone

import pystac
from pystac import Asset, Item, MediaType
from pystac.extensions.projection import ProjectionExtension

from stactools.usgs_lcmap import constants

logger = logging.getLogger(__name__)


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

    # item_assets
    # stac extensions
    # summaries?

    return collection


def create_item(asset_href: str) -> Item:
    """Create a STAC Item

    This function should include logic to extract all relevant metadata from an
    asset, metadata asset, and/or a constants.py file.

    See `Item<https://pystac.readthedocs.io/en/latest/api.html#item>`_.

    Args:
        asset_href (str): The HREF pointing to an asset associated with the item

    Returns:
        Item: STAC Item object
    """

    properties = {
        "title": "A dummy STAC Item",
        "description": "Used for demonstration purposes",
    }

    demo_geom = {
        "type": "Polygon",
        "coordinates": [[[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]],
    }

    # Time must be in UTC
    demo_time = datetime.now(tz=timezone.utc)

    item = Item(
        id="my-item-id",
        properties=properties,
        geometry=demo_geom,
        bbox=[-180, 90, 180, -90],
        datetime=demo_time,
        stac_extensions=[],
    )

    # It is a good idea to include proj attributes to optimize for libs like stac-vrt
    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = 4326
    proj_attrs.bbox = [-180, 90, 180, -90]
    proj_attrs.shape = [1, 1]  # Raster shape
    proj_attrs.transform = [-180, 360, 0, 90, 0, 180]  # Raster GeoTransform

    # Add an asset to the item (COG for example)
    item.add_asset(
        "image",
        Asset(
            href=asset_href,
            media_type=MediaType.COG,
            roles=["data"],
            title="A dummy STAC Item COG",
        ),
    )

    return item

import logging
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from pystac import Collection, Item
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.scientific import ScientificExtension
from stactools.core.io import ReadHrefModifier
from stactools.core.utils.raster_footprint import update_geometry_from_asset_footprint

from stactools.usgs_lcmap import cog, constants, utils

logger = logging.getLogger(__name__)


class MissingXML(Exception):
    ...


def create_item(tar_path: str, recog: bool = True) -> Item:
    """Create a STAC Item from a local TAR file and sidecar XML metadata file.

    If `recog` is True, the contents of the TAR will be extracted and placed in
    a new directory alongside the TAR file and the extracted COGs overwritten
    with new COGs containing: a corrected SRS, overviews, and (for some COGs) a
    nodata value. If `recog` is False, the extraction and COG re-processing is
    assumed to have previously been completed.

    Args:
        tar_path (str): Local path to a TAR archive
        recog (bool): Flag to reprocess the COGs. Default is True. This should
        only be set to False when the COGs have already been extracted from
        the TAR file and reprocessed.

    Returns:
        Item: STAC Item object
    """
    sidecar_xml = Path(tar_path).with_suffix(".xml")
    if not sidecar_xml.exists():
        raise MissingXML(f"Sidecar XML not found for tarfile '{tar_path}'")

    if recog:
        with tarfile.open(tar_path) as tar:
            tar.extractall(path=Path(tar_path).with_suffix(""))

    asset_list = [str(f) for f in Path(tar_path).with_suffix("").glob("*.*")]
    asset_list.append(tar_path)
    asset_list.append(str(sidecar_xml))

    if recog:
        for tif in [f for f in asset_list if Path(f).suffix == ".tif"]:
            cog.recog(tif)

    return create_item_from_asset_list(asset_list)


def create_item_from_asset_list(
    asset_list: List[str], read_href_modifier: Optional[ReadHrefModifier] = None
) -> Item:
    """Create a STAC Item from a list of asset HREFs.

    Args:
        asset_list (List[str]): List of HREFs to the set of TAR, TIF, XML, and
            TXT file assets.
        read_href_modifier (Optional[ReadHrefModifier]): An optional function
            to modify an HREF, e.g., to add a token to a URL.

    Returns:
        Item: STAC Item object
    """
    if len(asset_list) != 24:
        raise ValueError(
            f"Incorrect number of asset HREFs supplied. Expected 24, supplied "
            f"{len(asset_list)}"
        )

    asset_dict = utils.get_asset_dict(asset_list)
    metadata = utils.Metadata.from_cog(asset_dict["lcpri"].href, read_href_modifier)

    item = Item(
        id=metadata.id,
        geometry=metadata.geometry,
        bbox=metadata.bbox,
        datetime=None,
        properties={
            "start_datetime": metadata.start_datetime,
            "end_datetime": metadata.end_datetime,
            "usgs_lcmap:collection": metadata.lcmap_collection,
            "usgs_lcmap:horizontal_tile": metadata.horizontal_tile,
            "usgs_lcmap:vertical_tile": metadata.vertical_tile,
            "grid:code": (
                f"LARD-{metadata.horizontal_tile:03}{metadata.vertical_tile:03}"
            ),
        },
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
    item.stac_extensions.append(constants.FILE_EXTENSION_V21)
    item.stac_extensions.append(constants.GRID_EXTESION_V10)

    update_geometry_from_asset_footprint(
        item=item,
        asset_names=["lcpri"],
        simplify_tolerance=constants.FOOTPRINT_SIMPLIFICATION,
    )

    item.validate()

    return item


def create_collection(region: constants.Region) -> Collection:
    """Create a STAC Collection for CONUS or Hawaii.

    Returns:
        Collection: STAC Collection object.
    """
    if region is constants.Region.CU:
        collection = Collection(**constants.COLLECTION_CONUS_V13)
        collection.add_links([constants.ABOUT_LINK_CONUS, constants.LICENSE_LINK_CONUS])
    else:
        collection = Collection(**constants.COLLECTION_HAWAII_V10)
        collection.add_links(
            [constants.ABOUT_LINK_HAWAII, constants.LICENSE_LINK_HAWAII]
        )

    scientific = ScientificExtension.ext(collection, add_if_missing=True)
    if region is constants.Region.CU:
        scientific.publications = [
            constants.PUBLICATION_COMMON,
            constants.PUBLICATION_CONUS,
        ]
        scientific.doi = constants.DATA_CONUS["doi"]
        scientific.citation = constants.DATA_CONUS["citation"]
    else:
        scientific.publications = [constants.PUBLICATION_COMMON]

    collection.providers = [constants.PROVIDER]

    item_assets_dicts = utils.load_static_asset_info()
    for key, value in item_assets_dicts.items():
        item_assets_dicts[key] = AssetDefinition(value)
    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = item_assets_dicts

    collection.stac_extensions.append(constants.RASTER_EXTENSION_V11)
    collection.stac_extensions.append(constants.CLASSIFICATION_EXTENSION_V11)
    collection.stac_extensions.append(constants.FILE_EXTENSION_V21)

    return collection

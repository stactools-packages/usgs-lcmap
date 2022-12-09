import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import pkg_resources
import rasterio
from pystac import Asset
from pystac.utils import make_absolute_href
from rasterio.warp import transform_geom
from shapely.geometry import box, mapping, shape
from stactools.core.io import ReadHrefModifier

from . import constants


def parse_href(href: str) -> Dict[str, Any]:
    regex = (
        r"LCMAP_(?P<region>[A-Z]{2})_(?P<htile>\d{3})(?P<vtile>\d{3})"
        r"_(?P<year>\d{4})_(?P<production>\d{8})_V(?P<version>\d{2})_"
        r"(?P<product>[A-Z]+)\.(?P<ext>[a-z]{3})$"
    )
    regex_txt = (
        r"LCMAP_(?P<region>[A-Z]{2})_(?P<htile>\d{3})(?P<vtile>\d{3})"
        r"_(?P<production>\d{8})_V(?P<version>\d{2})_"
        r"(?P<product>[A-Z]+)\.(?P<ext>[a-z]{3})$"
    )

    name = Path(href).name
    parsed = re.compile(regex).match(name) or re.compile(regex_txt).match(name)
    if not parsed:
        raise ValueError(f"Can not parse. Unexpected file name: '{name}.")

    return parsed.groupdict()


def get_asset_dict(asset_list: List[str]) -> Dict[str, Any]:
    static_asset_info = load_static_asset_info()
    variable_asset_info = get_variable_asset_info(asset_list)
    assets = {}
    for key, value in static_asset_info.items():
        asset_dict = value
        asset_dict["href"] = make_absolute_href(variable_asset_info[key]["href"])
        asset_dict["created"] = variable_asset_info[key]["production"]
        assets[key] = Asset.from_dict(asset_dict)
    return assets


def get_variable_asset_info(asset_list: List[str]) -> Dict[str, Dict[str, str]]:
    variable: Dict[str, Dict[str, str]] = {}
    for href in asset_list:
        parsed = parse_href(href)
        product = parsed["product"].lower()
        ext = parsed["ext"]

        if product == "ccdc":
            if ext == "tar":
                key = "tar"
            elif ext == "xml":
                key = "tar_metadata"
            elif ext == "tif":
                key = "browse"
        elif ext == "tif":
            key = product
        elif ext == "xml":
            key = f"{product}_metadata"
        elif ext == "txt":
            key = "dates"
        else:
            raise ValueError(f"Unexpected file found: '{href}.")

        variable[key] = {}
        variable[key]["href"] = href
        variable[key]["production"] = (
            f"{parsed['production'][0:4]}-{parsed['production'][4:6]}-"
            f"{parsed['production'][6:8]}T00:00:00Z"
        )

    return variable


def load_static_asset_info() -> Any:
    """Loads a dictionary of item_assets entries for the collection.
    Returns:

        Any: A dictionary of item_asset dictionaries
    """
    try:
        with pkg_resources.resource_stream(
            "stactools.usgs_lcmap.utils",
            "assets/assets.json",
        ) as stream:
            return json.load(stream)
    except FileNotFoundError as e:
        raise e


@dataclass
class Metadata:
    id: str
    title: str
    geometry: Dict[str, Any]
    bbox: List[float]
    start_datetime: str
    end_datetime: str
    horizontal_tile: int
    vertical_tile: int
    lcmap_collection: str
    proj_wkt2: str
    proj_shape: List[int]
    proj_transform: List[float]

    @classmethod
    def from_cog(
        cls, href: str, read_href_modifier: Optional[ReadHrefModifier]
    ) -> "Metadata":
        if read_href_modifier:
            modified_href = read_href_modifier(href)
        else:
            modified_href = href
        with rasterio.open(modified_href) as dataset:
            source_crs = dataset.crs
            source_bbox = dataset.bounds
            source_geometry = mapping(box(*source_bbox))
            source_shape = dataset.shape
            source_transform = list(dataset.transform)[0:6]

        geometry = transform_geom(source_crs, "EPSG:4326", source_geometry)
        bbox = list(shape(geometry).bounds)

        parsed = parse_href(href)
        id = (
            f"LCMAP_{parsed['region']}_{parsed['htile']}{parsed['vtile']}_"
            f"{parsed['year']}_V{parsed['version']}_CCDC"
        )
        start_datetime = f"{parsed['year']}-01-01T00:00:00Z"
        end_datetime = f"{parsed['year']}-12-31T23:59:59Z"
        region = constants.Region[parsed["region"]].value
        lcmap_collection = f"{region} {float(parsed['version']) / 10}"
        title = (
            f"LCMAP {region} Collection {float(parsed['version']) / 10} Land "
            f"Cover and Land Change Products for Tile {parsed['htile']}"
            f"{parsed['vtile']}, Year {parsed['year']}"
        )

        return Metadata(
            id=id,
            title=title,
            geometry=geometry,
            bbox=bbox,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            horizontal_tile=int(parsed["htile"]),
            vertical_tile=int(parsed["vtile"]),
            lcmap_collection=lcmap_collection,
            proj_wkt2=source_crs.to_wkt(),
            proj_shape=source_shape,
            proj_transform=source_transform,
        )

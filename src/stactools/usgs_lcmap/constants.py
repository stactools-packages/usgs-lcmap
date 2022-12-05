import enum
from datetime import datetime, timezone
from typing import Any, Dict

import pystac


class Region(str, enum.Enum):
    CU = "CONUS"
    HI = "Hawaii"


PROVIDER = pystac.Provider(
    name="United States Geological Survey",
    roles=[
        pystac.ProviderRole.PRODUCER,
        pystac.ProviderRole.PROCESSOR,
        pystac.ProviderRole.LICENSOR,
        pystac.ProviderRole.HOST,
    ],
    url="https://www.usgs.gov/special-topics/lcmap",
)

LICENSE_LINK_CONUS = pystac.Link(
    rel="license",
    target="https://www.usgs.gov/special-topics/lcmap/collection-13-conus-science-products",
    title="Use of LCMAP CONUS Science Products",
    media_type="text/html",
)
LICENSE_LINK_HAWAII = pystac.Link(
    rel="license",
    target="https://www.usgs.gov/special-topics/lcmap/collection-1-hawaii-science-products",
    title="Use of LCMAP Hawaii Science Products",
    media_type="text/html",
)
ABOUT_LINK_CONUS = pystac.Link(
    rel="about",
    target="https://www.usgs.gov/special-topics/lcmap/collection-13-conus-science-products",
    title="LCMAP CONUS Science Products",
    media_type="text/html",
)
ABOUT_LINK_HAWAII = pystac.Link(
    rel="about",
    target="https://www.usgs.gov/special-topics/lcmap/collection-1-hawaii-science-products",
    title="LCMAP Hawaii Science Products",
    media_type="text/html",
)

KEYWORDS = ["USGS", "LCMAP", "Land Cover", "Land Cover Change", "United States"]

EXTENTS_CONUS = pystac.Extent(
    pystac.SpatialExtent([[-180.0, 90.0, 180.0, -90.0]]),  # UPDATE!
    pystac.TemporalExtent(
        [
            [
                datetime(1985, 1, 1, tzinfo=timezone.utc),
                datetime(2021, 12, 31, tzinfo=timezone.utc),
            ]
        ]
    ),
)
EXTENTS_HAWAII = pystac.Extent(
    pystac.SpatialExtent([[-180.0, 90.0, 180.0, -90.0]]),  # UPDATE!
    pystac.TemporalExtent(
        [
            [
                datetime(2000, 1, 1, tzinfo=timezone.utc),
                datetime(2020, 12, 31, tzinfo=timezone.utc),
            ]
        ]
    ),
)

COLLECTION_CONUS: Dict[str, Any] = {
    "id": "usgs-lcmap-conus",
    "title": "USGS Land Change Monitoring, Assessment, and Projection (LCMAP) for CONUS",
    "description": (
        "Land cover mapping and change monitoring from the U.S. Geological Survey's "
        "Earth Resources Observation and Science (EROS) Center. LCMAP Science Products "
        "are developed by applying time-series modeling to U.S. Landsat Analysis Ready "
        "Data (ARD) to detect change. An application of the Continuous. All available "
        "clear U.S. Landsat ARD observations are fit to a harmonic model to predict "
        "future Landsat-like surface reflectance. Where Landsat surface reflectance "
        "observations differ significantly from those predictions, a change is "
        "identified. Attributes of the resulting model sequences (e.g., start/end "
        "dates, residuals, model coefficients) are then used to produce a set of "
        "land surface change products and as inputs to the subsequent classification "
        "to thematic land cover. CONUS Collection 1.3 was released in August 2022 "
        "for years 1985-2021."
    ),
    "license": "proprietary",
    "keywords": KEYWORDS,
    "extent": EXTENTS_CONUS,
}
COLLECTION_HAWAII: Dict[str, Any] = {
    "id": "usgs-lcmap-hawaii",
    "title": "USGS Land Change Monitoring, Assessment, and Projection (LCMAP) for Hawaii",
    "description": (
        "Land cover mapping and change monitoring from the U.S. Geological Survey's "
        "Earth Resources Observation and Science (EROS) Center. LCMAP Science Products "
        "are developed by applying time-series modeling to U.S. Landsat Analysis Ready "
        "Data (ARD) to detect change. An application of the Continuous. All available "
        "clear U.S. Landsat ARD observations are fit to a harmonic model to predict "
        "future Landsat-like surface reflectance. Where Landsat surface reflectance "
        "observations differ significantly from those predictions, a change is "
        "identified. Attributes of the resulting model sequences (e.g., start/end "
        "dates, residuals, model coefficients) are then used to produce a set of "
        "land surface change products and as inputs to the subsequent classification "
        "to thematic land cover. LCMAP Hawaii Collection 1.0 products were released "
        "in January 2022 for years 2000-2020."
    ),
    "license": "proprietary",
    "keywords": KEYWORDS,
    "extent": EXTENTS_HAWAII,
}

ITEM_ASSETS = ""

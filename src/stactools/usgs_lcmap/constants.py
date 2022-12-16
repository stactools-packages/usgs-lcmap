import enum
from datetime import datetime, timezone
from typing import Any, Dict

import pystac
from pystac.extensions.scientific import Publication


class Region(str, enum.Enum):
    CU = "CONUS"
    HI = "Hawaii"


FOOTPRINT_SIMPLIFICATION = 0.00045  # about 1.5 pixels (45 meters)

RASTER_EXTENSION_V11 = "https://stac-extensions.github.io/raster/v1.1.0/schema.json"
CLASSIFICATION_EXTENSION_V11 = (
    "https://stac-extensions.github.io/classification/v1.1.0/schema.json"  # noqa
)
FILE_EXTENSION_V21 = "https://stac-extensions.github.io/file/v2.1.0/schema.json"

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

KEYWORDS = ["USGS", "LCMAP", "Land Cover", "Land Cover Change"]

LICENSE_LINK_CONUS = pystac.Link(
    rel="license",
    target="https://www.usgs.gov/special-topics/lcmap/collection-13-conus-science-products",
    title="Proprietary, Unrestricted",
    media_type="text/html",
)
LICENSE_LINK_HAWAII = pystac.Link(
    rel="license",
    target="https://www.usgs.gov/special-topics/lcmap/collection-1-hawaii-science-products",
    title="Proprietary, Unrestricted",
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

PUBLICATION_COMMON = Publication(
    doi="10.1016/j.rse.2019.111356",
    citation="Brown, J.F., Tollerud, H.J., Barber, C.P., Zhou, Q., Dwyer, J.L., Vogelmann, J.E., Loveland, T.R., Woodcock, C.E., Stehman, S.V., Zhu, Z., Pengra, B.W., Smith, K., Horton, J.A., Xian, G., Auch, R.F., Sohl, T.L., Sayler, K.L., Gallant, A.L., Zelenak, D., Reker, R.R., and Rover, J., 2020, Lessons learned implementing an operational continuous United States national land change monitoring capability—The Land Change Monitoring, Assessment, and Projection (LCMAP) approach: Remote Sensing of Environment, v. 238, article 111356",  # noqa
)
PUBLICATION_CONUS = Publication(
    doi="10.1016/j.rse.2014.01.011",
    citation="Zhu, Z., and Woodcock, C.E., 2014, Continuous change detection and classification of land cover using all available Landsat data: Remote Sensing of Environment, v. 144, p. 152-171",  # noqa
)
DATA_CONUS = {
    "doi": "10.5066/P9C46NG0",
    "citation": "U.S. Geological Survey (USGS), 2022, Land Change Monitoring, Assessment, and Projection (LCMAP) Collection 1.3 Science Products for the Conterminous United States: USGS data release",  # noqa
}

EXTENTS_CONUS = pystac.Extent(
    pystac.SpatialExtent([[-129.277320, 21.805095, -63.118430, 52.921720]]),
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
    pystac.SpatialExtent([[-161.275770, 18.505136, -154.058649, 22.624478]]),
    pystac.TemporalExtent(
        [
            [
                datetime(2000, 1, 1, tzinfo=timezone.utc),
                datetime(2020, 12, 31, tzinfo=timezone.utc),
            ]
        ]
    ),
)
SUMMARIES_CONUS = pystac.Summaries(
    {
        "usgs_lcmap:horizontal_tile": pystac.RangeSummary(1, 32),
        "usgs_lcmap:vertical_tile": pystac.RangeSummary(0, 20),
    }
)
SUMMARIES_HAWAII = pystac.Summaries(
    {
        "usgs_lcmap:horizontal_tile": pystac.RangeSummary(0, 4),
        "usgs_lcmap:vertical_tile": pystac.RangeSummary(0, 2),
    }
)

COLLECTION_CONUS_V13: Dict[str, Any] = {
    "id": "usgs-lcmap-conus-v13",
    "title": "USGS LCMAP CONUS 1.3",
    "description": (
        "Land Change Monitoring, Assessment, and Projection (LCMAP) from the U.S. "
        "Geological Survey's Earth Resources Observation and Science Center. LCMAP "
        "Science Products are developed by applying time-series modeling to U.S. "
        "Landsat Analysis Ready Data (ARD) to detect change. All available "
        "clear U.S. Landsat ARD observations are fit to a harmonic model to predict "
        "future Landsat-like surface reflectance. Where Landsat surface reflectance "
        "observations differ significantly from those predictions, a change is "
        "identified. Attributes of the resulting model sequences (e.g., start/end "
        "dates, residuals, model coefficients) are then used to produce a set of "
        "land surface change products and as inputs to the subsequent classification "
        "to thematic land cover. LCMAP Collection 1.3 for CONUS was released in "
        "August 2022 for years 1985-2021."
    ),
    "license": "proprietary",
    "keywords": KEYWORDS + ["CONUS"],
    "extent": EXTENTS_CONUS,
    "summaries": SUMMARIES_CONUS,
}
COLLECTION_HAWAII_V10: Dict[str, Any] = {
    "id": "usgs-lcmap-hawaii-v10",
    "title": "USGS LCMAP Hawaii 1.0",
    "description": (
        "Land Change Monitoring, Assessment, and Projection (LCMAP) from the U.S. "
        "Geological Survey's Earth Resources Observation and Science Center. LCMAP "
        "Science Products are developed by applying time-series modeling to U.S. "
        "Landsat Analysis Ready Data (ARD) to detect change. All available "
        "clear U.S. Landsat ARD observations are fit to a harmonic model to predict "
        "future Landsat-like surface reflectance. Where Landsat surface reflectance "
        "observations differ significantly from those predictions, a change is "
        "identified. Attributes of the resulting model sequences (e.g., start/end "
        "dates, residuals, model coefficients) are then used to produce a set of "
        "land surface change products and as inputs to the subsequent classification "
        "to thematic land cover. LCMAP Collection 1.0 for Hawaii was released "
        "in January 2022 for years 2000-2020."
    ),
    "license": "proprietary",
    "keywords": KEYWORDS + ["Hawaii"],
    "extent": EXTENTS_HAWAII,
    "summaries": SUMMARIES_HAWAII,
}

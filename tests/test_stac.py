from stactools.usgs_lcmap.stac import create_item
from tests import test_data


def test_custom_field_names() -> None:
    infile = test_data.get_path(
        "data-files/CU/LCMAP_CU_001004_1999_20220723_V13_CCDC.tar"
    )
    item = create_item(infile)
    assert item.properties.pop("usgs_lcmap:collection", None) is not None
    assert item.properties.pop("usgs_lcmap:horizontal_tile", None) is not None
    assert item.properties.pop("usgs_lcmap:vertical_tile", None) is not None

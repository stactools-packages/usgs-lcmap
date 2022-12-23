from stactools.usgs_lcmap import constants
from stactools.usgs_lcmap.stac import create_collection, create_item
from stactools.usgs_lcmap.utils import get_variable_asset_info
from tests import test_data


def test_custom_field_names() -> None:
    infile = test_data.get_path(
        "data-files/CU/LCMAP_CU_001004_1999_20220723_V13_CCDC.tar"
    )
    item = create_item(infile)
    assert item.properties.pop("usgs_lcmap:collection", None) is not None
    assert item.properties.pop("usgs_lcmap:horizontal_tile", None) is not None
    assert item.properties.pop("usgs_lcmap:vertical_tile", None) is not None


def test_malformed_date_txt_filename() -> None:
    bad_filename = ["LCMAP_CU_0020220723_V13_ACQS.txt"]
    asset_info_dict = get_variable_asset_info(bad_filename)
    asset_info = asset_info_dict["dates"]
    assert asset_info.get("href", None) is not None
    assert asset_info.get("production", None) is not None


def test_notar_collection() -> None:
    collection = create_collection(constants.Region.CU, notar=True)
    assert "tar" not in collection.extra_fields["item_assets"]
    assert "tar_metadata" not in collection.extra_fields["item_assets"]

    collection = create_collection(constants.Region.CU, notar=False)
    assert "tar" in collection.extra_fields["item_assets"]
    assert "tar_metadata" in collection.extra_fields["item_assets"]


def test_notar_item() -> None:
    infile = test_data.get_path(
        "data-files/CU/LCMAP_CU_001004_1999_20220723_V13_CCDC.tar"
    )
    item = create_item(infile, notar=True)
    assert "tar" not in item.assets
    assert "tar_metadata" not in item.assets

import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.usgs_lcmap.commands import create_usgs_lcmap_command
from tests import test_data


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_usgs_lcmap_command]

    def test_create_collection(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "collection.json")
            result = self.run_command(
                f"usgs-lcmap create-collection CONUS {destination}"
            )
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            collection = pystac.read_file(destination)
            assert collection.id == "usgs-lcmap-conus"

            collection_dict = collection.to_dict()
            assert len(collection_dict["item_assets"]) == 24

            collection.validate()

    def test_create_conus_item(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            infile = test_data.get_path(
                "data-files/CU/LCMAP_CU_001004_1999_20220723_V13_CCDC.tar"
            )
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command(f"usgs-lcmap create-item {infile} {destination}")
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            item = pystac.read_file(destination)
            assert item.id == "LCMAP_CU_001004_1999_V13_CCDC"

            item_dict = item.to_dict()
            assert len(item_dict["assets"]) == 24

            item.validate()

    def test_create_conus_item_nocog(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            infile = test_data.get_path(
                "data-files/CU/LCMAP_CU_001004_1999_20220723_V13_CCDC.tar"
            )
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command(
                f"usgs-lcmap create-item {infile} {destination} -n"
            )
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            item = pystac.read_file(destination)
            assert item.id == "LCMAP_CU_001004_1999_V13_CCDC"

            item_dict = item.to_dict()
            assert len(item_dict["assets"]) == 24

            item.validate()

    def test_create_hawaii_item(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            infile = test_data.get_path(
                "data-files/HI/LCMAP_HI_000000_2020_20211130_V10_CCDC.tar"
            )
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command(f"usgs-lcmap create-item {infile} {destination}")
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            item = pystac.read_file(destination)
            assert item.id == "LCMAP_HI_000000_2020_V10_CCDC"

            item_dict = item.to_dict()
            assert len(item_dict["assets"]) == 24

            item.validate()

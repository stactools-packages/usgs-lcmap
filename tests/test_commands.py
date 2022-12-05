import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.usgs_lcmap.commands import create_usgs_lcmap_command


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
            collection.validate()

    def test_create_item(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-item command and validate

            # Example:
            infile = "/path/to/asset.tif"
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command(f"usgs-lcmap create-item {infile} {destination}")
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            item = pystac.read_file(destination)
            assert item.id == "my-item-id"
            # assert item.other_attr...

            item.validate()

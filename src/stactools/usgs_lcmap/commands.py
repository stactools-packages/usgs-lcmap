import click
import pystac
from click import Command, Group

from stactools.usgs_lcmap import constants, stac


def create_usgs_lcmap_command(cli: Group) -> Command:
    """Creates the stactools-usgs-lcmap command line utility."""

    @cli.group(
        "usgs-lcmap",
        short_help=("Commands for working with USGS LCMAP data"),
    )
    def usgs_lcmap() -> None:
        pass

    @usgs_lcmap.command("create-collection", short_help="Create a STAC collection")
    @click.argument("region", type=click.Choice([r.value for r in constants.Region]))
    @click.argument("destination")
    def create_collection_command(region: str, destination: str) -> None:
        """Creates a STAC Collection for the specified region.

        \b
        Args:
            region (str): Choice of 'CONUS' or 'Hawaii'
            destination (str): An HREF for the STAC Collection JSON
        """
        collection = stac.create_collection(constants.Region(region))
        collection.set_self_href(destination)
        collection.catalog_type = pystac.CatalogType.SELF_CONTAINED
        collection.validate()
        collection.save_object()

        return None

    @usgs_lcmap.command("create-item", short_help="Create a STAC item")
    @click.argument("tar_path")
    @click.argument("destination")
    @click.option(
        "-n",
        "--nocog",
        is_flag=True,
        default=False,
        show_default=True,
        help="Do not reprocess COGs",
    )
    def create_item_command(tar_path: str, destination: str, nocog: bool) -> None:
        """Creates a STAC Item and reprocesses all COGs found in the TAR archive
        to include overviews and a corrected SRS.

        \b
        Args:
            tar_path (str): Local path to a TAR archive
            destination (str): An HREF for the STAC Item JSON
            nocog (bool): Flag to turn off COG reprocessing. Only use if COGs
                sit alongside the TAR archive and have been reprocessed.
        """
        recog = not nocog
        item = stac.create_item(tar_path=tar_path, recog=recog)

        item.set_self_href(destination)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object(include_self_link=False)

        return None

    return usgs_lcmap

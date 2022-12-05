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

    @usgs_lcmap.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("region", type=click.Choice([r.value for r in constants.Region]))
    @click.argument("destination")
    def create_collection_command(region: str, destination: str) -> None:
        """Creates a STAC Collection

        \b
        Args:
            region (str): Choice of 'CONUS' or 'Hawaii'
            destination (str): An HREF for the Collection JSON
        """
        collection = stac.create_collection(constants.Region(region))
        collection.set_self_href(destination)
        collection.catalog_type = pystac.CatalogType.SELF_CONTAINED
        collection.validate()
        collection.save_object()

        return None

    @usgs_lcmap.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    def create_item_command(source: str, destination: str) -> None:
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Item
        """
        item = stac.create_item(source)

        item.save_object(dest_href=destination)

        return None

    return usgs_lcmap

import stactools.core
from stactools.cli.registry import Registry

from stactools.usgs_lcmap.stac import create_collection, create_item

__all__ = ["create_collection", "create_item"]

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    from stactools.usgs_lcmap import commands

    registry.register_subcommand(commands.create_usgs_lcmap_command)


__version__ = "0.1.0"

from pathlib import Path
from tempfile import TemporaryDirectory

import rasterio.shutil
from stactools.core.utils.subprocess import call

# Original TIF SRS definitions contain incorrect WGS84 semi-major and inverse
# flattening values. These new, correct SRS definitions are copied from the
# Landsat ARD TIFs (LCMAP is a derived product of Landsat ARD).
CONUS_SRS = 'PROJCS["AEA        WGS84",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["latitude_of_center",23],PARAMETER["longitude_of_center",-96],PARAMETER["standard_parallel_1",29.5],PARAMETER["standard_parallel_2",45.5],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'  # noqa
HAWAII_SRS = 'PROJCS["AEA        WGS84",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["latitude_of_center",3],PARAMETER["longitude_of_center",-157],PARAMETER["standard_parallel_1",8],PARAMETER["standard_parallel_2",18],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'  # noqa

COG_ARGS = {
    "compress": "deflate",
    "driver": "COG",
    "blocksize": 512,
}


def recog(tif_path: str) -> None:
    """Inserts corrected SRS, creates COG with overviews. Color table is
    retained.

    Args:
        tif_path (str): Path to existing GeoTIFF file.
    """
    srs = CONUS_SRS if "CU" in Path(tif_path).stem else HAWAII_SRS
    with TemporaryDirectory() as tmp_dir:
        temp_tif = Path(tmp_dir) / "tmp_gtiff"
        args = ["gdal_translate", "-of", "GTIFF", "-a_srs", srs]
        if Path(tif_path).stem.split("_")[-1][0:2] in ["LC", "CC"]:
            args += ["-a_nodata", "0"]
        args.append(tif_path)
        args.append(temp_tif)
        call(args)
        rasterio.shutil.copy(temp_tif, tif_path, **COG_ARGS)

    return None

import rioxarray
import xarray as xr

if __name__ == '__main__':
    xds = rioxarray.open_rasterio(
        'red.tif',
        masked=True,
    )

    geometries = [
        {
            'type': 'Polygon',
            'coordinates': [[
                [0,0],
                [100, 0],
                [100, 100],
                [0, 100],
                [0, 0],

            ]]
        }
    ]
    clipped = xds.rio.clip(geometries)

    pl = clipped.plot()
    pl.show()
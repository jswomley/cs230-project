import ee
ee.Initialize()
import numpy as np

rgb = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA').select(['B4', 'B3', 'B2']).filterDate('2020-06-05', '2020-09-01').filterMetadata('CLOUD_COVER', 'less_than', 15).median().visualize(**{'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.5})
elevation = ee.Image('CGIAR/SRTM90_V4')

X = np.linspace(-120,-106,71)
Y = np.linspace(35,49,71)

scale_factors = np.zeros(4167)

i = 0
for x in X:
    for y in Y:
        if i < 4167:

            region = ee.Geometry.Polygon([[[x, y+0.2], [x+0.2, y+0.2], [x, y], [x+0.2, y]]])

            rgb_task_config = {
            'scale': 30, 
            'region': region,
            'crs': 'EPSG:5070',
            'maxPixels': 1e13,
            'folder': 'RGB3'
            }

            elevation_task_config = {
            'scale': 30, 
            'region': region,
            'crs': 'EPSG:5070',
            'maxPixels': 1e13,
            'folder': 'Elevation3'
            }

            min_max = elevation.reduceRegion(
            reducer = ee.Reducer.minMax(),
            geometry = region,
            scale = 30,
            maxPixels = 1e13
            )

            min_i = min_max.getInfo()['elevation_min']
            max_i = min_max.getInfo()['elevation_max']

            rgb_task = ee.batch.Export.image(rgb, 'RGB_' + str(i), rgb_task_config)
            elevation_task = ee.batch.Export.image(\
                elevation.visualize(**{'bands': ['elevation'], 'min': min_i, 'max': max_i}), 'E_' + str(i), elevation_task_config)
            scale_factors[i] = (max_i - min_i)/255

            rgb_task.start()
            elevation_task.start()

        i += 1

np.save('scale_factors3_trial2.npy', scale_factors)

print(np.mean(scale_factors))
print((np.min(scale_factors), np.max(scale_factors)))
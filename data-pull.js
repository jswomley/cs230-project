// [MUST BE RUN IN GOOGLE EARTH ENGINE]

// Given a region, this script pulls the associated RGB and elevation data.
// For our purposes, we define many different regions and pass in 256x256pix
// cuts of the larger regions into our model 

// Define region (this one is ~3600 sq. miles in CO)
var region = ee.Geometry.Polygon(
  [[[-107.5, 39.5],
    [-106, 39.5],
    [-107.5, 38],
    [-106, 38]]]);

// Pull Landsat image with R/G/B wavelength bands (img selected for few clouds)
var image = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_038029_20180810')
            .visualize({bands: ['B4', 'B3', 'B2'], min: 0, max: 2500});

// Export image
Export.image.toDrive({
  image: image,
  description: 'image_export',
  folder: 'CS230-Project',
  region: region,
  scale: 30,
  crs: 'EPSG:5070',
  maxPixels: 1e13
})

// Define elevation using CGIAR image
var elevation = ee.Image('CGIAR/SRTM90_V4')
                .select(['elevation']);
                
// Create collection of elevation points in defined region        
samp_elev = elevation.sample({region: region, geometries: true});                

// Export elevation data
Export.table.toDrive({
  collection: samp_elev,
  description: 'elevation_sample',
  fileFormat: 'CSV',
  scale: 30
});

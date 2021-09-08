## Collect data:

### Hubs as Points in a map (EPSG:4326 - WGS 84 - Geographic) -> EPSG:20137 - Adindan / UTM zone 37N
Single Points
- not nullData: points should not have been deleted from map without having deleted them from the Attributes table
### Population density from HDX (Pregnant women from 15-49 in ethiopia)
- as points: Have to import from the .csv format. (Data Source Manager - Delimited Text)

### Google Hydrid Map / Open StreetMap for the World
- Shapefiles from the Ethiopian Administation (Region, Zone, Woredas)

## Clean Data
- Location Points has to be of Type Point and not MultiPoint and the points displayed on the map have to be consistent with the attributes table. Having deleted point in the map will not delete them from the attribute table automatically. This will lead to an error in the processing of the algorithm. with HC points -> only HCs in Limu Bilbilo
- By importing the data as a raster and displaying it on the map with different graduated colors help for the visual appreciation, but in order to count and weight the number of pregnant women in Bekoji, it is necessary to have this information as a points layer and not raster layer. Therefore, the import of the downloaded .cvs file is required.
- Displaying the background map for orientation is the first and basic step to do. First I downloaded the Google Hybrid Image Set, but it contains much more information about other aspects not relevant for the current research. On the other hand, the choice to use OpenStreetMap allows to see less information but provides a cleaner look to work on further layers.
- There was no need to clean or update these files, important is nonetheless to import the in the correct CRS, so that the units match and all the distances and areas of the layers are the right ones.
## Data analysis and processing
- Algorithm to define distances and areas around one hub. In my case, health centers. with HC points -> only HCs in Limu Bilbilo
- Women points -> only in Limu Bilbilo : Vector>Select Tools>Select by Location (check intersect, contain and overlap). From Selection create a new layer. This new layer contains the female population only in Limu Bilbilo.
- Create Polygons as grid areas for the extent of the layer being treated. We want to have all the area of Limu Bilbilo covered by hexagons. [Why? explain beforehand.] -> Vector>Research Tools>Create Grid
Horizontal Spacing : 0,00849 --> 1,01 km2
X Spacing, Project Units, Extent : Layer of Woreda.
- Count points in polygon with weighted sum, since the points have the number of women as attribute, we count the points multiplying them with the weighted sum of this attribute value.
- Now we have Hexagons with a PointsNUM attribute, which gives the number of women living in this 1km2 hexagon.
- Calculate the distance from the selected hubs, from the health centers to every center point of each polygon. A new points layer is produced, whose attributes contain the number of women living in Limu Bilbilo (PointsCOUNT), the distance from each polygon center to its nearest health center and the name of t

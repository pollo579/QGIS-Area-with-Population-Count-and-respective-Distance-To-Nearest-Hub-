# QGIS-Area-with-Population-Count-and-respective-Distance-To-Nearest-Hub-
This repository presents the Concept of Demand vs. Service Value

**Why**
- While researching into a new supply chain like healthcare, the aCar team needs to know where is the most need of help. For this reason, it is important to determine the aCar service value in relationship to the demand in a geographical aspect. The aim of this repository is to survey the geographical demand of a service and assess its value (service value) based on the proximity of a hub to a certain limited area. 

**Requiremenets:**
**layer <-> geometry**
- population density <-> points
- area map <-> raster
- Hub (e.g. Health Centers) distribution <-> points

**What we calulate:**
- How many points there is in a specific area and its distance to the nearest hub. 

**How we do it:**
Divide a map into smaller areas (e.g. hexagons), count the points in this dedicated area and calculate the distance from this area to the nearest hub.
From these steps we produce two heatmaps. The first one depicts the amount 

## Images

![Heatmap of distance based demand. Red areas are where extreme users need services](https://i.redd.it/8rvqwe8pw9m71.jpg)


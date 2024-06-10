import json
import argparse
from shapely.geometry import shape, MultiPolygon, mapping
from shapely.ops import unary_union

parser = argparse.ArgumentParser(description="Combine MultiPolygon zones in a GeoJSON file into a single MultiPolygon.")
parser.add_argument('--input', required=True, help="Input GeoJSON file")
parser.add_argument('--output', required=True, help="Output GeoJSON file")
args = parser.parse_args()

with open(args.input, 'r') as f:
    geojson_data = json.load(f)

# Collect all MultiPolygon geometries
multipolygons = []
for feature in geojson_data['features']:
    geometry = shape(feature['geometry'])
    if isinstance(geometry, MultiPolygon):
        multipolygons.append(geometry)
    elif geometry.geom_type == 'Polygon':  # Include single Polygons as well
        multipolygons.append(MultiPolygon([geometry]))

# Combine all MultiPolygon geometries into a single MultiPolygon
combined_multipolygon = unary_union(multipolygons)


# Prepare the combined geometry as a new GeoJSON feature
combined_feature = {
    "type": "Feature",
    "geometry": mapping(combined_multipolygon),
    "properties": {} 
}

# Create a new GeoJSON structure
combined_geojson = {
    "type": "FeatureCollection",
    "features": [combined_feature]
}

# Save the combined GeoJSON to the output file
with open(args.output, 'w') as f:
    json.dump(combined_geojson, f, indent=4, ensure_ascii=False)

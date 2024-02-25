import geopandas as gpd
import pandas as pd
from shapely.affinity import translate

def get_canary_geopandas_layer():
    root_canary_islands_layer = '../SHP_REGCAN95/recintos_provinciales_inspire_canarias_regcan95/recintos_provinciales_inspire_canarias_regcan95.shp'
    return gpd.read_file(root_canary_islands_layer)

def get_spain_geopandas_layer():
    root_spain_layer = '../SHP_ETRS89/recintos_provinciales_inspire_peninbal_etrs89/recintos_provinciales_inspire_peninbal_etrs89.shp'
    return gpd.read_file(root_spain_layer)

def change_layer_crs(layer, crs):
    return layer.to_crs(crs)

def move_layer_close_to_spain(layer):
    added_x = 18
    added_y = 8
    layer['geometry'] = layer['geometry'].apply(lambda geom: translate(geom, added_x, added_y))
    return layer

def merge_layers(layer_one, layer_two):
    return gpd.GeoDataFrame(pd.concat([layer_two, layer_one], ignore_index=True), crs=layer_one.crs)

def export_layer_to_geojson(exported_layer):
    spain_canary_root_exported = '../geojson/recintos_provinciales_canarias_desplazadas_spain.geojson'
    return exported_layer.to_file(spain_canary_root_exported)

canary_layer = get_canary_geopandas_layer()
spain_layer = get_spain_geopandas_layer()
canary_layer = change_layer_crs(canary_layer, spain_layer.crs)
canary_layer = move_layer_close_to_spain(canary_layer)
spain_canary_layer = merge_layers(spain_layer, canary_layer)
export_layer_to_geojson(spain_canary_layer)

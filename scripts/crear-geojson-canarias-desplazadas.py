import geopandas as gpd
import pandas as pd
from shapely.affinity import translate

def get_canary_geopandas_frame():
    root_canary_islands = '../SHP_REGCAN95/recintos_provinciales_inspire_canarias_regcan95/recintos_provinciales_inspire_canarias_regcan95.shp'
    return gpd.read_file(root_canary_islands)

def get_spain_geopandas_frame():
    root_spain = '../SHP_ETRS89/recintos_provinciales_inspire_peninbal_etrs89/recintos_provinciales_inspire_peninbal_etrs89.shp'
    return gpd.read_file(root_spain)

def change_canary_crs_to_spain_crs(canary_layer, spain_layer):
    return canary_layer.to_crs(spain_layer.crs)

def move_canary_close_to_spain(canary_layer):
    added_x = 18
    added_y = 8
    canary_layer['geometry'] = canary_layer['geometry'].apply(lambda geom: translate(geom, added_x, added_y))
    return canary_layer

def merge_spain_and_canary_frames(spain_layer, canary_layer):
    return gpd.GeoDataFrame(pd.concat([canary_layer, spain_layer], ignore_index=True), crs=spain_geopandas_frame.crs)

def export_spain_canary_frame_to_geojson(exported_layer):
    spain_canary_root_exported = '../geojson/recintos_provinciales_canarias_desplazadas_spain.geojson'
    return exported_layer.to_file(spain_canary_root_exported)

canary_geopandas_frame = get_canary_geopandas_frame()
spain_geopandas_frame = get_spain_geopandas_frame()
canary_geopandas_frame = change_canary_crs_to_spain_crs(canary_geopandas_frame, spain_geopandas_frame)
canary_geopandas_frame = move_canary_close_to_spain(canary_geopandas_frame)
spain_canary_frame = merge_spain_and_canary_frames(spain_geopandas_frame, canary_geopandas_frame)
export_spain_canary_frame_to_geojson(spain_canary_frame)



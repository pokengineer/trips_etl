from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from shapely import wkt
import geopandas as gpd

def ingest_trips( file='trips.csv' ):
    load_dotenv()
    params = os.environ

    # Connect to postgis
    engine = create_engine("postgresql+psycopg2://"+ params['DB_USER'] +":"+ params['DB_PASS']+ "@localhost:5432/test_db")

    # Extract
    gdf = gpd.read_file( file )

    # Transform coordinates into geometry objects
    gdf['origin_coord'] = gdf['origin_coord'].apply(wkt.loads)
    gdf = gdf.set_geometry('origin_coord')
    gdf['destination_coord'] = gdf['destination_coord'].apply(wkt.loads)
    gdf = gdf.set_geometry('destination_coord')

    # Append data into postgis
    gdf.to_postgis( params['TABLE_NAME'] ,if_exists='append', con=engine)  

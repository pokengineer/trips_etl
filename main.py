from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from shapely import wkt
import geopandas as gpd
from datetime import datetime

load_dotenv()

def ingest_trips( file='trips.csv' ):
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
    gdf['datetime'] = gdf['datetime'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%Y%V") )

    # Append data into postgis
    gdf.to_postgis( params['TABLE_NAME'] ,if_exists='append', con=engine)  

    
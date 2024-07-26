from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os
from shapely import wkt
import geopandas as gpd
from datetime import datetime
import pandas as pd
from threading import Thread
import cmd
import warnings

def tripETL( df, engine, i):
    print(f"starting thread {i}")
    # Extract
    gdf = gpd.GeoDataFrame( df )

    # Transform coordinates into geometry objects
    gdf['origin_coord'] = gdf['origin_coord'].apply(wkt.loads)
    gdf = gdf.set_geometry('origin_coord')
    gdf['destination_coord'] = gdf['destination_coord'].apply(wkt.loads)
    gdf = gdf.set_geometry('destination_coord')
    gdf['week_no'] = gdf['datetime'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%Y%V") )

    # Append data into postgis
    gdf.to_postgis( 'trips' ,if_exists='append', con=engine, chunksize=100000) 
    print(f"thread {i} finished")


def ingest_trips( file='trips.csv' ):
    params = os.environ
    # Connect to postgis
    engine = create_engine("postgresql+psycopg2://"+ params['DB_USER'] +":"+ params['DB_PASS']+ "@localhost:5432/test_db")

    threads = []
    reader = pd.read_csv(file, chunksize=100000) 
    i=0
    for chunk in reader:
        t = Thread(target=tripETL, args=(chunk,engine,i,))
        i+=1
        threads.append(t)
        t.start()
    for t in threads:
        t.join() 


def weekly_avg_by_region( region ):
    params = os.environ
    engine = create_engine("postgresql+psycopg2://"+ params['DB_USER'] +":"+ params['DB_PASS']+ "@localhost:5432/test_db")

    query = """select avg(no_trips)
        from ( select 
        week_no, count(id) as no_trips
        from trips t 
        where region = '""" + str(region) + """'
        group by week_no )"""
    with engine.connect() as connection:
        result = connection.execute(text(query))
    return result.fetchone().t[0]

def weekly_avg_by_box( xmin, ymin, xmax, ymax ):
    params = os.environ
    engine = create_engine("postgresql+psycopg2://"+ params['DB_USER'] +":"+ params['DB_PASS']+ "@localhost:5432/test_db")

    query = """select avg(no_trips)
        from ( select 
        week_no, count(id) as no_trips
        from trips t 
        where destination_coord && ST_MakeEnvelope( """ + ",".join([str(x) for x in [xmin, ymin, xmax, ymax]]) + """)
        group by week_no )"""
    with engine.connect() as connection:
        result = connection.execute(text(query))
    return result.fetchone().t[0]

class console_application(cmd.Cmd):
    """Simple command processor used to create proof of concept of trip data ingestion."""
    warnings.filterwarnings('ignore')

    def do_greet(self, line):
        print("hello " + line)
    
    def do_ETL(self,file):
        ingest_trips(file)
    
    def do_avg(self,region):
        a = weekly_avg_by_region(region)
        print( a )

    def do_avg_box(self,line):
        coords = [float(x) for x in line.split(" ")]
        a = weekly_avg_by_box( coords[0], coords[1], coords[2], coords[3] )
        print( a )
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    load_dotenv()
    console_application().cmdloop()
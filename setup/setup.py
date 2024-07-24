from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    params = os.environ
    engine = create_engine("postgresql+psycopg2://"+ params['DB_USER'] +":"+ params['DB_PASS']+ "@localhost:5432/test_db")

    table_creation_query = """
    CREATE TABLE trips (
        id BIGSERIAL,
        region varchar(255) NULL,
        origin_coord public.geometry(point),
        destination_coord public.geometry(point),
        datetime timestamp,
        week_no int,
        datasource varchar(255) NULL
    );
    COMMIT
    """
    with engine.connect() as con:
        con.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        con.execute(text(table_creation_query))
        con.commit()
    print('table succefully created')
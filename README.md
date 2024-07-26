# Data Engineering Challenge
The task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

## Install necesary requirements
Before running any code it is important to install libraries used in the project. You can install them using pip:
```
pip install -r requirements.txt
```

## Create the database
Mount Docker image for the development database, run the following commands to start the docker image for the database
```
cd setup
docker-compose up -d
python setup.py
```

## Test the application
The main script for the application loop is located inside the application folder. 
```
python main.py
```

Once the application is running the interface admits commands in the form command imput

### Ingest and store the data
For the main ingestion function the command ETL is used, followed by the path to the csv file.
```
ETL trips.csv
```

### Weekly average number of trips for an area
There are two commands to obtain the weekly average, if you wish to search average based on a region name, the command is avg and the parameter is the region: 
```
avg Turin
```
the other using a bounding box given by coordinates, where the parameters are 4 float values separated by a single space xmin ymin xmax ymax.
```
avg_box 10 40 15 50
```


## Perform the stress test
```
python stress-test.py
```

## Aditional queries
Aditionally there where two questions proposed as SQL exercise, the queries have been placed in the queries folder.
query1.sql answers the question "From the two most commonly appearing regions, which is the latest datasource?"
by creating a nested query for the most commonly appearing regions, and then a temporary table called latest_trips to get the latest datetime.

query2.sql is a much simpler query, and answers the question "What regions has the "cheap_mobile" datasource appeared in?" 
filtering the desired datasource in the where clause.
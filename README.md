# Data Engineering Challenge
The task is to build an automatic process to ingest geographical data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

## Design of the solution
The Challenge can be achieved using a wide variety of tools, in my project I chose to use Python for the main application and PostgreSQL to store the data. Given the type of data being handled I chose specific libraries and extensions that perform better when using geographic information and I know can be easily integrated with other GIS tools if needed for more complex later analysis.
Specifically, the decision was to handle data using [Geopandas](https://geopandas.org/) instead of a more easily scalable PySpark dataframe, in case some transformation of the geographical data is needed before storage. I also installed a PostgreSQL extension called [PostGis](https://postgis.net/) that is used for storing and querying geographical locations, maps and areas.
The only extra column added on the ETL process was a week number column, as it seems from the assignments that data partition by week is important for the analysis.

## Install necessary requirements
Before running any code it is important to have [Python](https://www.python.org/), [pip](https://pypi.org/project/pip/) and [Docker](https://www.docker.com/) installed, and then install the libraries used in the project. You can install them using pip:
```
cd setup
pip install -r requirements.txt
```

## Create the database
Also in the setup folder we will have to mount Docker image for the development database using the file docker-compose.yml, and  then run the python script to setup the creation of the main table used.
```
docker-compose up -d
python setup.py
```

## Test the application
The main script for the application loop is located inside the application folder. 
```
python main.py
```

Once the application is running the interface admits commands in the form command input

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
We can also perform a stress test of the solution, in the folder stress_test we can find the script that creates the file. Then we can call it from the main function as we did for trips.csv
```
python stress-test.py
```

## Additional queries
Additionally there were two questions proposed as SQL exercise, the queries have been placed in the queries folder.
### query1.sql 
answers the question "From the two most commonly appearing regions, which is the latest datasource?"
by creating a nested query for the most commonly appearing regions, and then a temporary table called latest_trips to get the latest datetime.
### query2.sql
is a much simpler query, and answers the question "What regions has the "cheap_mobile" datasource appeared in?" 
filtering the desired datasource in the where clause.

## Further analysis
After completing the features, it is proposed to sketch up how a cloud version of the project could be set up. I think the best strategy would be to split the functionalities to provide higher cohesion and lower coupling. Ideally I think all analytic tasks (like the region averages and the additional queries) could be easily migrated into serverless cloud functions (Google cloud functions / AWS Lambda) or a table view could be created if the query is always the same.
As for the main ETL process in situations similar to the stress test it would timeout a typical lambda function, so a containerized solution should be developed to handle the large volume of data. Given the timeframe provided for the challenge I chose to prioritize core functionalities, but I believe it would be advantageous to add more data validation steps (check for extra columns, data types, valid coordinates, etc. ) when extracting the data and when receiving user-inputs.

!["simple cloud diagram"](https://github.com/pokengineer/trips_etl/blob/main/misc/cloud_diagram.png)

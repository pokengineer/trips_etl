# Data Engineering Challenge
The task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

# Install necesary requirements
Before running any code it is important to install libraries used in the project. You can install them using pip:
> pip install -r requirements.txt

# Create the database
Mount Docker image for the development database, run the following commands to start the docker image for the database

>cd setup <br>
>docker-compose up -d <br>
>python setup.py <br>

# Perform the stress test

> python stress-test.py


# Aditional queries
Aditionally there where two questions proposed as SQL exercise, the queries have been placed in the queries folder.
query1.sql answers the question "From the two most commonly appearing regions, which is the latest datasource?"
by creating a nested query for the most commonly appearing regions, and then a temporary table called latest_trips to get the latest datetime.

query2.sql is a much simpler query, and answers the question "What regions has the "cheap_mobile" datasource appeared in?" 
filtering the desired datasource in the where clause.
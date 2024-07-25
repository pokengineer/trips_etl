# Data Engineering Challenge
The task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

# install necesary requirements
Before running any code it is important to install libraries used in the project. You can install them using pip:
> pip install -r requirements.txt

# create the database
Mount Docker image for the development database, run the following commands to start the docker image for the database

>cd setup <br>
>docker-compose up -d <br>
>python setup.py <br>

# Perform the stress test

> python stress-test.py

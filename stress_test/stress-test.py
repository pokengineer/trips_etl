import pandas as pd
import random

def create_dataframes():
    origin = [ 'POINT ('+ str(random.uniform(5, 20)) +' '+ str(random.uniform(45,55)) + ')' for a in range(50) ] 
    dest = [ 'POINT ('+ str(random.uniform(5, 20)) +' '+ str(random.uniform(45,55)) + ')' for a in range(50) ] 
    ds = random.choices(datasources,k=50)
    date = random.choices(some_dates,k=50)
    region = random.choices(regions,k=50,weights=[2, 5, 5])
    df = pd.DataFrame({'region':region, 'origin_coord':origin, 'destination_coord':dest, 'datetime':date,'datasource':ds})
    for i in range(14):
        df = pd.concat([df, df], axis=0)
    return df
    

if __name__ == '__main__':
    filename = "stress_test.csv"

    regions = ['Prague','Turin','Hamburg']
    datasources = ['funny_car','baba_car','cheap_mobile','bad_diesel_vehicles','pt_search_app']
    some_dates = ['2019-05-28 9:03:00','2019-06-20 9:03:00','2019-08-10 9:09:00','2019-03-10 9:09:00','2018-05-28 9:03:00','2018-06-20 9:03:00','2018-08-10 9:09:00','2018-03-10 9:09:00']
    df = create_dataframes()
    df.to_csv(filename, index=False)
    for n in range(1, 15):
        df = create_dataframes()
        df.to_csv( filename ,chunksize=100000, index=False, mode='a', header=False)


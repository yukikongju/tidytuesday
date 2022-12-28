import pandas as pd
import json


def download_stations_dataframe(download_path):
    """ 
    Function to download stations json file as dataframe
    """
    url = "https://gbfs.velobixi.com/gbfs/en/station_information.json"

    data = pd.read_json(url)['data']['stations']
    df = pd.DataFrame.from_dict(data)
    df.to_csv(download_path, index=False)


#  -----------------------------------------------------------------------



#  -----------------------------------------------------------------------

def main():
    download_stations_dataframe('bixi/data/stations.csv')
    

if __name__ == "__main__":
    main()

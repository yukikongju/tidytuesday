import pandas as pd
import json
import os

from tqdm import tqdm

STATIONS_CSV = 'bixi/data/stations.csv'

def download_stations_dataframe(download_path):
    """ 
    Function to download stations json file as dataframe
    """
    url = "https://gbfs.velobixi.com/gbfs/en/station_information.json"

    data = pd.read_json(url)['data']['stations']
    df = pd.DataFrame.from_dict(data)
    df.to_csv(download_path, index=False)


def standardize_deplacements_data(deplacement_dir_raw, new_deplacement_dir_path):
    """ 
    Function to standardize deplacements data. One csv file per year

    Columns: 
        - rental_id
        - start_date
        - start_station_code: (short_name)
        - end_station_code: (short_name)
        - duration_sec
        - is_member
    """
    # 1. create station id dictionary
    df_stations = pd.read_csv(STATIONS_CSV)
    stations_dict = dict(zip(df_stations.station_id, df_stations.short_name))
    #  print(stations_dict)


    # 2. concatenate year dataset
    if not os.path.exists(new_deplacement_dir_path):
        os.makedirs(new_deplacement_dir_path)
    for i, (subdir, dirs, files) in enumerate(os.walk(deplacement_dir_raw)):
        dataframes = []
        year = subdir.split('/')[-1]
        #  print(year, files)
        for file in tqdm(files):
            csv_path = os.path.join(subdir, file)
            if 'station' not in csv_path.lower() and int(year) > 2020:
                # convert
                df = pd.read_csv(csv_path)
                df['start_station_code'] = df['emplacement_pk_start'].apply(lambda x: stations_dict.get(x))
                df['end_station_code'] = df['emplacement_pk_end'].apply(lambda x: stations_dict.get(x))
                df.drop(columns=['emplacement_pk_start', 'emplacement_pk_end'])
                dataframes.append(df)
        # concat df
        if dataframes != []:
            save_csv_path = os.path.join(new_deplacement_dir_path, f'deplacements_{year}.csv')
            df_concat = pd.concat(dataframes, ignore_index=True)
            df_concat.to_csv(save_csv_path, index=False)



#  -----------------------------------------------------------------------



#  -----------------------------------------------------------------------

def main():
    #  download_stations_dataframe('bixi/data/stations.csv')
    standardize_deplacements_data('bixi/data/deplacements_raw', 'bixi/data/deplacements')
    

if __name__ == "__main__":
    main()

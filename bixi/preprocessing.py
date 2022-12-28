import pandas as pd
import json
import os
import datetime

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
    Function to standardize deplacements data. One csv file per year-month

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
    for i, (subdir, dirs, files) in enumerate(os.walk(deplacement_dir_raw)):
        dataframes = []
        year = subdir.split('/')[-1]
        print(year, files)
        for file in tqdm(files):
            csv_path = os.path.join(subdir, file)

            if 'station' not in csv_path.lower() and int(year) > 2021:
                #  convert
                df = pd.read_csv(csv_path)
                df['start_station_code'] = df['emplacement_pk_start'].apply(lambda x: stations_dict.get(x))
                df['end_station_code'] = df['emplacement_pk_end'].apply(lambda x: stations_dict.get(x))
                df.drop(columns=['emplacement_pk_start', 'emplacement_pk_end'])

                # save csv 
                year, month, _ = str(pd.to_datetime(str(df['start_date'][0])).date()).split('-')
                if not os.path.exists(os.path.join(new_deplacement_dir_path, year)):
                    os.makedirs(os.path.join(new_deplacement_dir_path, year))

                save_csv_path = os.path.join(new_deplacement_dir_path, year, f'OD_{year}-{month}.csv')
                df.to_csv(save_csv_path, index=False)
            #  elif 'station' not in csv_path.lower() and int(year) <= 2020:
            #      df = pd.read_csv(csv_path)
            #      dataframes.append(df)
        #  concat df
        #  if dataframes != []:
        #      save_csv_path = os.path.join(new_deplacement_dir_path, f'deplacements_{year}.csv')
        #      df_concat = pd.concat(dataframes, ignore_index=True)
        #      df_concat.to_csv(save_csv_path, index=False)

def split_csv_monthly(csv_path, new_csv_dir): # TODO
    """ 
    Fonction that split csv year file into month
    """
    # 0. reformat station code
    df = pd.read_csv(csv_path)
    df_stations = pd.read_csv(STATIONS_CSV)
    stations_dict = dict(zip(df_stations.station_id, df_stations.short_name))
    if 'emplacement_pk_start' in df.columns:
        df['start_station_code'] = df['emplacement_pk_start'].apply(lambda x: stations_dict.get(x))
        df.drop(columns=['emplacement_pk_start'])
    if 'emplacement_pk_end' in df.columns:
        df['end_station_code'] = df['emplacement_pk_end'].apply(lambda x: stations_dict.get(x))
        df.drop(columns=['emplacement_pk_end'])

    # 1. group the dataframe by month
    df['date'] = pd.to_datetime(df['start_date'])
    g = df.groupby(pd.Grouper(key='date', freq='M'), as_index=False)
    dfs = [group.reset_index() for _, group in g]

    # create year directory
    year, _, _ = str(pd.to_datetime(str(df['date'][0])).date()).split('-')
    if not os.path.exists(os.path.join(new_csv_dir, year)):
        os.mkdir(os.path.join(new_csv_dir, year))

    # 2. save monthly csv
    for i, df in enumerate(dfs):
        df = df.drop(columns=['index'])
        # get year and month
        date = str(pd.to_datetime(str(df['date'][0])).date())
        year, month, day = date.split('-')
        new_csv_path = os.path.join(new_csv_dir, year, f'OD_{year}-{month}.csv')
        print(new_csv_path)
        df.to_csv(new_csv_path, index=False)

    

#  -----------------------------------------------------------------------


def test_split_csv_monthly():
    #  split_csv_monthly('bixi/data/deplacements_raw/2020/OD_2020.csv', 'bixi/data/deplacements/')
    split_csv_monthly('bixi/data/deplacements_raw/2021/2021_donnees_ouvertes.csv', 'bixi/data/deplacements/')
    

#  -----------------------------------------------------------------------

def main():
    #  download_stations_dataframe('bixi/data/stations.csv')
    standardize_deplacements_data('bixi/data/deplacements_raw', 'bixi/data/deplacements')
    #  test_split_csv_monthly()
    #  print(pd.to_datetime('2020-04-15 06:00:04').date())
    

if __name__ == "__main__":
    main()

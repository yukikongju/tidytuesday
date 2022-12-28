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
    #  df = df.sort(by=['start_date']) # CHECK
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

    
def download_usage_by_month(csv_file):
    """ 
    groupby start_station_code

    Columns: 
        - month, year
        - station
        - count: is_user, not_user, total_users
    """
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['start_date'])
    if 'is_member' in df.columns:
        df = df[['date', 'start_station_code', 'is_member']].groupby([
                #  pd.Grouper(key='date', freq='M'), 
                pd.Grouper(key='date', freq='D'), 
                pd.Grouper('start_station_code'), 
                #  pd.Grouper('is_member')
            ]).agg(['count', 'sum']).droplevel(axis=1, level=0).reset_index()
        df['non_member_count'] = df['count'] - df['sum']
        df = df.rename(columns={'count': 'total_count', 'sum': 'member_count', })
    else: 
        df = df[['date', 'start_station_code', 'rental_id']].groupby([
                #  pd.Grouper(key='date', freq='M'), 
                pd.Grouper(key='date', freq='D'), 
                pd.Grouper('start_station_code'), 
            ]).agg(['count']).droplevel(axis=1, level=0).reset_index()
        df = df.rename(columns={'count': 'total_count'})

    # groupby station_code to create monthly usage dataset for each station
    g = df.groupby([
            pd.Grouper('start_station_code'),
            pd.Grouper(key='date', freq='M'), 
        ], as_index=False)
    dfs = [group for _, group in g]

    return dfs

def compute_station_daily_capacity_raw(deplacement_csv_path):
    """ 
    Given monthly deplacement, compute station capacity per 5 minutes

    Returns
    -------
    dfs: list of dataframes
        station daily capacity every 5 minutes

    """
    # 1. 
    df = pd.read_csv(deplacement_csv_path)
    df = df.astype({'start_station_code': 'int'})

    # 2. concatenate
    df_start = df[['start_date', 'start_station_code']]
    df_start['status'] = 'START'
    df_start = df_start.rename(columns={'start_date': 'timestamp', 'start_station_code': 'station_code'})
    df_end = df[['end_date', 'end_station_code']]
    df_end['status'] = 'END'
    df_end = df_end.rename(columns={'end_date': 'timestamp', 'end_station_code': 'station_code'})
    df_concat = pd.concat([df_start, df_end]).reset_index()
    df_concat['timestamp'] = pd.to_datetime(df_concat['timestamp'])
    df_concat = df_concat.pivot_table(index=['timestamp', 'station_code'], columns='status', aggfunc='count').droplevel(axis=1, level=0).reset_index()
    #  print(df_concat.head())

    # 3. count number of bixis that comes and go every 5 minutes
    df_concat = df_concat.groupby([
            pd.Grouper(key='timestamp', freq='5min'),
            pd.Grouper('station_code'),
        ]).agg(['count']).droplevel(axis=1, level=1).reset_index()

    # 4. split dataset into timestamp and station_code (one csv file per station code per day)
    g = df_concat.groupby([
            pd.Grouper(key='timestamp', freq='D'),
            pd.Grouper('station_code')
        ], as_index=False)
    dfs = [group for _, group in g]
    #  print(dfs[0])

    return dfs


#  -----------------------------------------------------------------------


def test_split_csv_monthly():
    #  split_csv_monthly('bixi/data/deplacements_raw/2020/OD_2020.csv', 'bixi/data/deplacements/')
    split_csv_monthly('bixi/data/deplacements_raw/2021/2021_donnees_ouvertes.csv', 'bixi/data/deplacements/')


def test_download_usage_by_month(deplacement_dir, usage_dir):
    #  download_usage_by_month('bixi/data/deplacements/2018/OD_2018-05.csv')

    for subdir, dirs, files in os.walk(deplacement_dir):
        year = subdir.split('/')[-1]
        for file in tqdm(files): 
            csv_path = os.path.join(subdir, file)
            #  print(csv_path)
            dfs = download_usage_by_month(csv_path)
            for df in tqdm(dfs): 
                year, month, _ = str(pd.to_datetime(str(df['date'].iloc[-1])).date()).split('-')
                station_code = str(df['start_station_code'].iloc[-1])
                new_subdir = os.path.join(usage_dir, year, month)
                if not os.path.exists(new_subdir):
                    os.makedirs(new_subdir)
                new_csv_path = os.path.join(new_subdir , f'usage_{year}_{month}_station_{station_code}.csv')
                df.to_csv(new_csv_path, index=False)


def test_get_daily_capacity(deplacement_dir, capacity_raw_dir):
    #  dfs = compute_station_daily_capacity_raw('bixi/data/deplacements/2017/OD_2017-06.csv')

    for subdir, dirs, files in os.walk(deplacement_dir):
        year = subdir.split('/')[-1]
        if year == '2022': # FIXME: 2022 station don't always have end station
            continue
        if not os.path.exists(os.path.join(capacity_raw_dir, year)):
            os.makedirs(os.path.join(capacity_raw_dir, year))
        for file in files: 
            csv_path = os.path.join(subdir, file)
            print(csv_path)
            dfs = compute_station_daily_capacity_raw(csv_path)
            for df in dfs:
                # get year, month, day, station_code
                year, month, day = str(pd.to_datetime(str(df['timestamp'][0])).date()).split('-')
                # check station code is valid
                try:
                    station_code = int(df['station_code'][0])
                except: 
                    continue

                # save csv
                capacity_subdir = os.path.join(capacity_raw_dir, year, month, day)
                if not os.path.exists(capacity_subdir):
                    os.makedirs(capacity_subdir)
                new_capacity_path = os.path.join(capacity_subdir, f'{year}_{month}_{day}_station_{station_code}.csv')
                df.to_csv(new_capacity_path, index=False)

    

#  -----------------------------------------------------------------------

def main():
    #  download_stations_dataframe('bixi/data/stations.csv')
    #  standardize_deplacements_data('bixi/data/deplacements_raw', 'bixi/data/deplacements')
    #  test_split_csv_monthly()
    #  print(pd.to_datetime('2020-04-15 06:00:04').date())
    test_download_usage_by_month('bixi/data/deplacements/', 'bixi/data/monthly_usage/')
    #  test_get_daily_capacity('bixi/data/deplacements/', 'bixi/data/capacity_raw/')
    

if __name__ == "__main__":
    main()

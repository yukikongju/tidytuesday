import yaml
import os
import sys
import logging
import joblib
import argparse
import pandas as pd

from sklearn.model_selection import train_test_split


def get_config_path(args):
    """ 
    Get config file name from arguments

    Parameters
    ----------
    args: parser arguments


    Returns
    -------
    config_path: string
        path to the config file

    Raises
    ------
    ArgumentError
        exit if the number of argument passed is not 1

    """
    # check if argument have been passed
    if len(vars(args)) != 1:
        raise argparse.ArgumentError("The only argument that need to be passed is the config file path")
        sys.exit(1)

    # get config_file_path
    return args.config_file


def load_check_config(config_file_path):
    """ 
    Load and check if config file path is valid and defines all required parameters

    Parameters
    ----------
    config_file_path: string
        configuration read from the config file

    Returns
    -------
    config: dict
        return yaml dict

    Raises
    ------
    FileNotFoundError
        exit program if config_file_path doesn't exist
    KeyError 
        return false if required parameters missing from config file

    """
    # load file
    try:
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        sys.exit(1)

    # check main components: data, model, metric (optimizer is optional)
    try:
        data = config['data']
        model = config['model']
        metric = config['metric']
    except KeyError as e:
        logging.error(f"'data', 'model' and 'metric' needs to be defined in config file: {e}")
        sys.exit(1)

    # check data: data_directory, data_file
    try: 
        data_dir = data['data_directory']
        data_file = data['data_file']
    except KeyError as e:
        logging.error(f"data_directory and data_file should be defined under 'data': {e}")
        sys.exit(1)

    # check model: class, type, pickle_file, pickle_dir
    try: 
        model_class = model['class']
        model_type = model['type']
        pickle_file = model['pickle_file']
        pickle_dir = model['pickle_dir']
    except KeyError as e:
        logging.error(f"type, data_file and data_directory should be defined under 'model': {e}")
        sys.exit(1)


    # check metric: name, lr 
    # TODO: check if metric name is valid based on model_type
    try: 
         metric_name = metric['name']
    except KeyError as e:
        logging.error(f"name should be defined under 'metric': {e}")
        sys.exit(1)

    # TODO: check optimizer if exists (optional)

    return config
    

def get_train_test_features_target(config):
    """ 
    Get x_train, x_test, y_train, y_test from config file

    Remarks
    -------

    Parameters
    ----------
    config: dict
        configuration read from the config file

    Returns
    -------
    x_train: pandas.DataFrame
    x_test: pandas.DataFrame
    y_train: pandas.DataFrame
    y_test: pandas.DataFrame

    Raises
    ------
    ValueError
        exit if file path is not csv file
    FileNotFoundError
        exit if csv file is not found

    """
    data_dir = config['data']['data_directory']
    data_file = config['data']['data_file']

    data_path = os.path.join(data_dir, data_file)

    # check if file is csv file
    if not data_file.endswith(".csv"):
        raise ValueError("data_file should be a csv file. Please check!")
        sys.exit(1)

    # check if path exists
    if not os.path.exists(data_path):
        raise FileNotFoundError("The csv file wasn't found")
        sys.exit(1)

    # loading the file
    try:
        df = pd.read_csv(data_path)
    except:
        logging.error("An error occured when loading the file")
        sys.exit(1)

    # splitting data to features and target 
    X = df.drop(config['model']['target'], axis=1)
    y = df[config['model']['target']]

    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=config['data']['test_size'],
            random_state=config['model']['random_state']
    )
    return X_train, X_test, y_train, y_test

    
def save_model(model, config):
    """ 
    Save model in directory and file defined in config file

    Parameters
    ----------
    config: dict
        configuration read from the config file

    Raises
    ------
    FileNotFoundError 
        exit if pickle_dir doesn't exist

    """
    pickle_dir = config['model']['pickle_dir']
    pickle_file = config['model']['pickle_file']
    try:
        joblib.dump(model, os.path.join(pickle_dir, pickle_file))
    except FileNotFoundError as e:
        logging.error("The pickle path specified in the config file is erroneous. Please check!")
        sys.exit(1)
    



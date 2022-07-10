import yaml
import os
import sys
import logging
import joblib

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def load_config(config_file_path):
    """
    Load config file

    Parameters
    ----------
    config_file_path: string
        path to config file (ex: "../config/tmp.cfg") [should be yaml]

    Returns
    -------
    config: dict
        return yaml dict

    Raises
    ------
    FileNotFoundError
        exit program if config_file_path doesn't exist

    Examples
    --------

    """
    try:
        config_name = sys.argv[1]
        with open(config_file_path) as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        sys.exit(1)

def check_config(config):
    """ 
    Verify if config file is well defined 

    Parameters
    ----------
    config: dict
        configuration read from the config file

    Returns
    -------
    flag: bool
        True if config file is well defined. Else false

    Raises
    ------
    KeyError 
        return false if required parameters missing from config file

    """
    # check main components: data, model, metric (optimizer is optional)
    try:
        data = config['data']
        model = config['model']
        metric = config['metric']
    except KeyError as e:
        logging.error(f"'data', 'model' and 'metric' needs to be defined in config file: {e}")
        return False

    # check data: data_directory, data_file
    try: 
        data_dir = data['data_directory']
        data_file = data['data_file']
    except KeyError as e:
        logging.error(f"data_directory and data_file should be defined under 'data': {e}")
        return False

    # check model: class, type, pickle_file, pickle_dir
    try: 
        model_class = model['class']
        model_type = model['type']
        pickle_file = model['pickle_file']
        pickle_dir = model['pickle_dir']
    except KeyError as e:
        logging.error(f"type, data_file and data_directory should be defined under 'model': {e}")
        return False


    # check metric: name, lr 
    # TODO: check if metric name is valid based on model_type
    try: 
         metric_name = metric['type']
         lr = metric['lr']
    except KeyError as e:
        logging.error(f"name and lr should be defined under 'metric': {e}")
        return False

    # TODO: check optimizer if exists (optional)

    return True
    

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

    """
    df = pd.read_csv(os.path.join(config['data']['data_directory'], 
        config['data']['data_file']))

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
    



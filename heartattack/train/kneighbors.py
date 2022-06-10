import pandas as pd
import yaml
import os
import sys
import joblib

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# Executing the script: python3 % kneighbors.yaml


### 1. Load Config file

# set current dir as root
abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname)

CONFIG_PATH = '../config'

# loading the config file 
try:
    config_name = sys.argv[1]
    with open(os.path.join(CONFIG_PATH, config_name)) as f:
        config = yaml.safe_load(f)
except:
    print(f"Couldn't load the config file")
    sys.exit(1)

### 2. Load and split the data into train and test

df = pd.read_csv(os.path.join(config['data']['data_directory'], 
    config['data']['data_file']))

X = df.drop(config['model']['target'], axis=1)
y = df[config['model']['target']]

X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config['model']['test_size'],
        random_state=config['model']['random_state']
)


### 3. creating and testing the model

classifier = KNeighborsClassifier(
        n_neighbors=config['model']['n_neighbors'],
        weights=config['model']['weights'],
        metric=config['model']['metric'],
)

classifier.fit(X_train, y_train)

predictions = classifier.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(accuracy)

### 4. Save model

joblib.dump(classifier, os.path.join(config['model']['model_directory'], 
    config['model']['model_name']))




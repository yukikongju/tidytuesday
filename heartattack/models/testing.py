import argparse

from classifier import ClassifierModel
from utils import load_check_config, save_model, get_train_test_features_target, get_config_path

""" 
Executing file: python3 % 'heartattack/config/kneighbors.cfg'
"""


# Step 0: define parser
parser = argparse.ArgumentParser(description="Train and Test model on data defined in config file")
parser.add_argument('config_file', metavar='f', help="path to config file")
args = parser.parse_args()

# Step 1: get config_path
config_file_path = get_config_path(args)


# Step 2: get config from config file
config = load_check_config(config_file_path)
print(config)

# Step 3: Get data from config_file
X_train, X_test, y_train, y_test = get_train_test_features_target(config)


# Step 4: Define Model
model = ClassifierModel(config).get_model()

# Step 5: train model
model.fit(X_train, y_train)


# Step 6: Get model accuracy scores
predictions = model.predict(X_test)
scores = model.get_metric_score(predictions, y_test)


# Step 7: save model
save_model(model, config)


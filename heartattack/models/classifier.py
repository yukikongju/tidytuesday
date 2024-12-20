import sys

from model import SklearnModel
from sklearn.metrics import accuracy_score


class ClassifierModel(SklearnModel):

    def __init__(self, config):
        super().__init__(config)

    def get_model(config):
        """ 
        Return sklearn classifier defined in config file

        Parameters
        ----------
        config: dict
            configuration read from the config file

        Returns
        -------
        classifier: sklearn classifier

        Raises
        ------
        TypeError
            exit program if model_class is not classifier
        NotImplementedError
            exit program because classifier hasn't been defined

        """
        #  TODO: fix error: model not suscriptable
        model_class = config['model']['class']

        # check if model is a classifier 
        if model_class != 'classifier':
            raise TypeError("The model defined in the config file is not a classifier. Please check!")
            sys.exit(1)

        # get classifier
        model_type = config['model']['type']
        if model_type == 'KNeighborsClassifier':
            # check if parameters are defined in config file
            try:
                n_neighbors = config['model']['n_neighbors']
                weights = config['model']['weights']
                metric = config['model']['metric']
            except KeyError as e:
                logging.error(f"n_neighbors, weights, metric missing from model. Please check!")

            return KNeighborsClassifier(
                n_neighbors=config['model']['n_neighbors'],
                weights=config['model']['weights'],
                metric=config['model']['metric'],
            )
        else:
            raise NotImplementedError("This classifier hasn't been implemented yet")
            sys.exit(1)

    def get_metric_score(self, y_pred, y_true):
        """ 
        Get metric from config file

        Parameters
        ----------
        y_pred: list
            values predicted by classifier
        y_true: list
            true values

        Returns
        -------
        metric score:
            
        Raises
        ------
        ValueError
            exit program if metric_name is not a classifier metric
        NotImplementedError
            exit program because the metric wasn't implemented 
        """
        # check if the metric defined is a classifier metric
        metric_name = self.config['metric']['name']
        if metric_name not in ['accuracy_score']:
            raise ValueError("The metric defined in the config file is not a classifier metric. \
                    Should be one of the following: 'accuracy_score'. Please check!")
            sys.exit(1)

        # get metric score
        if metric_name == 'accuracy_score':
            return accuracy_score(y_true, y_pred)
        else:
            raise NotImplementedError("The metric hasn't been implemented yet.")
            sys.exit(1)


        

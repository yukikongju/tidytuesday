from abc import ABC


class SklearnModel(ABC):

    def __init__(self, config):
        self.config = config


    def get_model(self):
        pass

    def get_metric_score(self):
        pass
        

        

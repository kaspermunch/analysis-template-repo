import yaml
import pprint

class Params():
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value) 
            
    def __getitem__(self, attr):
        return self.__dict__[attr]
        
    def __repr__(self):
        return pprint.pformat(self.__dict__)

        
def load_params(parameter_yaml_file):
    """
    Load parameters from yaml file and produce an object where
    parameters an be accessed as both keys and attributes
    """
    with open(parameter_yaml_file) as params:
        return Params(**yaml.load(params, Loader=yaml.Loader))
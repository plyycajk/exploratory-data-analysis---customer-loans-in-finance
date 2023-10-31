import os
import yaml


#loads yaml based on filename without extension
def load_credentials(filename):
    with open (f'{filename}.yaml','r') as f:
        loaded_credentials = yaml.safe_load(f)
        print(loaded_credentials)

load_credentials('credentials')
#class  RDSDatabaseConnector:
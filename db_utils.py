#imports required for script
from sqlalchemy import create_engine
import pandas as pd
import yaml


def load_credentials(filename):
    '''This function loads a .yaml file containing database credential information'''
    with open (f'{filename}.yaml','r') as f:
        loaded_credentials = yaml.safe_load(f)
        return loaded_credentials

class  RDSDatabaseConnector(object):
    '''
    This class establishes a connection to relational database
    
    Attributes:
        self.db_credentials (dict): database credentials to allow connection, loaded from load_credentials() function
        self.user (str): username for user connecting (loaded from credentials file)
        self.password (str): password for user connecting (loaded from credentials file)
        self.host (str): host info for the database being connected to (loaded from credentials file)
        self.database (str): database name of database being connected to (loaded from credentials file)
        self.db_type (str): type of database being connected to
        self.dbapi (str): chosen database API for connection
        self.engine (obj): SQLAlchemy engine to establish connection to the database
        self.dbconn (obj): database connection object
    '''

    def __init__(self, connection_credentials):
        '''
        See help(RDSDatabaseConnector) for accurate signature
        '''
        self.db_credentials = load_credentials(connection_credentials)
        self.user = self.db_credentials['RDS_USER']
        self.password = self.db_credentials['RDS_PASSWORD']
        self.host = self.db_credentials['RDS_HOST']
        self.port = self.db_credentials['RDS_PORT']
        self.database = self.db_credentials['RDS_DATABASE']
        self.db_type = 'postgresql'
        self.dbapi =  'psycopg2'
        self.engine = None
        self.dbconn = None

        print('connection credentials loaded')
    
    def __enter__(self):
        '''
        This function is used to instantiate a SQLAlchemy engine to connect to a database.
        
        Returns:
            A SQLAlchemy engine connected to the database: self.dbconn
        '''
        self.engine = create_engine(f"{self.db_type}+{self.dbapi}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
        print('creating engine')
        self.dbconn = self.engine.connect()
        print('establishing connection')
        return self.dbconn


    def __exit__(self, exc_type, exc_val, exc_tb):
        '''This function closes the connection to the database'''
        print('closing connection')
        self.dbconn.close()

def loan_payments_to_dataframe(db_credentials_file):
    '''
    This function extracts loan payments information to a dataframe
    
    Args:
        dbcredentials (str): filename (without extension) containing the database credentials to allow connection
    
    Returns:
        dataframe 
        '''
    with RDSDatabaseConnector(db_credentials_file) as conn:
        df = pd.read_sql_table('loan_payments', conn)
        # printed line confirms variable name of dataframe
        print('loan_payments data extracted and available in \'loan_payments\' dataframe') 
        return df

def save_to_csv(dataframe):
    '''
    This function saves a dataframe as a .csv file
    
    Args:
        dataframe: variable name of dataframe object to be saved as a .csv file

    Returns:
        .csv file of dataframe
    '''
    # dataframe.name ensures that name of dataframe is passed to the filename rather than the dataframe itself
    dataframe.to_csv(f'{dataframe.name}.csv', sep=',', index=False)
    
    # printed line confirms name of .csv file that has been created.
    print(f'{dataframe.name} dataframe saved to {dataframe.name}.csv in folder')

if __name__ == '__main__':
    loan_payments = loan_payments_to_dataframe('credentials')
    loan_payments.name = 'loan_payments'
    save_to_csv(loan_payments)



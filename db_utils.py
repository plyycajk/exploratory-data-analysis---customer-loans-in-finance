#imports required for script
import yaml
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy import inspect


#loads yaml based on filename without extension
def load_credentials(filename):
    with open (f'{filename}.yaml','r') as f:
        loaded_credentials = yaml.safe_load(f)
        return loaded_credentials

class  RDSDatabaseConnector(object):
    
    """
    This class docstring needs to be completed 
    
    Attributes:
        attributes need to be described in detail here
    """

    def __init__(self, connection_credentials):
        self.db_credentials = load_credentials(connection_credentials)
        self.user = self.db_credentials['RDS_USER']
        self.password = self.db_credentials['RDS_PASSWORD']
        self.host = self.db_credentials['RDS_HOST']
        self.port = self.db_credentials['RDS_PORT']
        self.database = self.db_credentials['RDS_DATABASE']
        self.engine = None
        self.dbconn = None

        print('connection credentials loaded')
    
    def __enter__(self):
        self.engine = create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
        print('creating engine')
        self.dbconn = self.engine.connect()
        print('establishing connection')
        return self.dbconn


    def __exit__(self, exc_type, exc_val, exc_tb):
        print('closing connection')
        self.dbconn.close()
        print('data extracted')


def loan_payments_to_dataframe(dbcredentials):
    with RDSDatabaseConnector(dbcredentials) as conn:
        df = pd.read_sql_table('loan_payments', conn)
        print('loan_payments data extracted and available in \'loan_payments\' dataframe') 
        return df

def save_to_csv(dataframe):
    dataframe.to_csv(f'{dataframe.name}.csv', sep=',', index=False)
    print(f'{dataframe.name} dataframe saved to {dataframe.name}.csv in folder')

if __name__ == '__main__':
    loan_payments = loan_payments_to_dataframe('credentials')
    loan_payments.name = 'loan_payments'
    save_to_csv(loan_payments)



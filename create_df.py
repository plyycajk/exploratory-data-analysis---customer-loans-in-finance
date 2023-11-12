import pandas as pd
from db_utils import load_yaml #imports yaml_load function from db_utils.


class DataTransform:
    '''
    This class performs transformations on a dataframe based on transformations specified in a supplied .yaml file
    
    Attributes:
      file (file): a .csv file to be loaded into a dataframe
      transformations (file): a .yaml file specifying the column transformations to be undertaken by the instance of the class
    '''
    
    def __init__(self, file, transformations):
      '''
      refer to help(DataTransform) for accurate signature
      ''' 
      self.df = pd.read_csv(file)
      self.transformations = load_yaml(transformations)
      self.str_to_datetime()
      self.to_category()
      self.remove_text()
      self.to_string()
      self.object_to_int()

    def str_to_datetime(self):
      datetime_transformations = self.transformations['str_to_datetime']
      '''This method converts dates stored as strings to the datetime format'''
      for col in datetime_transformations:
          self.df[col] = pd.to_datetime(self.df[col], format='%b-%Y')
      print(f'converted {datetime_transformations} to datetime format') #provides confirmation message to the terminal
      return self.df
    
    def to_category(self):
      '''This method converts the designated columns in the transformations file to categorical dtype'''
      category_cols = self.transformations['to_category']
      for col in category_cols:
          self.df[col] = self.df[col].astype('category')
      print(f'converted {category_cols} to categorical dtype') #provides confirmation message to the terminal
      return self.df

    def remove_text(self):
      '''This method replaces sepcified text in columns provided in the .yaml file'''
      str_transformations = self.transformations['remove_text']
      cols_to_change = []
      for d in str_transformations: #d corresponds to the column names specified under this method in the .yaml file
        for k in d:
          cols_to_change.append(k)  #adds required change list of changes for column(s)

      for i in range(len(str_transformations)):
        changes=(str_transformations[i][cols_to_change[i]]) #slices list of dictionaries to find each change per columns
        for old, new in changes.items():
          self.df[cols_to_change[i]] = self.df[cols_to_change[i]].str.replace(old, new, regex=False)
      (print(f'performed string replacements on {cols_to_change}'))
      return self.df
    
    def to_string(self):
       '''This method converts columns to the object dtype'''
       str_cols = self.transformations['to_string']
       for col in str_cols:
          self.df[col] = self.df[col].astype('string')
       print(f'converted {str_cols} to object dtype')
       return self.df
    
    def object_to_int(self):
       '''This method converts object columns to integers and is called after removing leading/trailing text on columns that are/should be numerical'''
       int_cols = self.transformations['object_to_int']
       for col in int_cols:
          self.df[col] = self.df[col].astype('Int64')
       print(f'converted {int_cols} to object int')
       return self.df

    def load(self):
       '''When called, this function ensures that a pandas dataframe is returned'''
       return self.df

    def __repr__(self):
      return repr(self.df)
    
class DataFrameInfo:
    '''
    This class provides summary information on a provided dataframe. Information includes 
      - a 'describe' call on each numerical column
      - the dtype of each column
      - the number of unique values in each categorical column
      - the shape of the dataframe
      - the percentage of null values in each column
      - the skew within each column

    Args: dataframe (pd.DataFrame): a pandas dataframe to have 
    '''

    def __init__(self, dataframe):
       self.df = dataframe
       self.describe_cols = self.df.select_dtypes(include='number').describe()
       self.dtype_cols = self.df.dtypes
       self.cat_distinct_values = self.df.select_dtypes(include='category').nunique()
       self.df_shape = self.df.shape
       self.null_percentage = self.df.isnull().sum()/len(self.df)*100
       self.skew_cols = self.df.skew()
       
    def describe_cols(self):
      return self.describe_cols

    def dtype_cols(self):
      return self.dtype_cols

    def cat_distinct_values(self):
      return self.cat_distinct_values

    def df_shape(self):
      return self.df_shape

    def null_percentage(self):
      return self.null_percentage
    
    def skew_cols(self):
       return self.skew_cols

def get_dataframe_info(dataframe):
   df = DataFrameInfo(dataframe)
   print('Summary statistics for each numeric column in the dataframe:\n')
   print(df.describe_cols)
   print('\nThe dtypes for the dataframe are:')
   print(df.dtype_cols)
   print('\nThe number of distinct values in each categorical column are:')
   print(df.cat_distinct_values)
   print('\nThe shape of the dataframe is: ')
   print(df.df_shape)
   print('\nThe percentage of null values per column is:')
   print(df.null_percentage)
   print('\nThe skew for each column is:')
   print(df.skew_cols)


if __name__ == '__main__':
    loan_payments_transformed = DataTransform('loan_payments.csv','df_transformations').load()
    
    get_dataframe_info(loan_payments_transformed)

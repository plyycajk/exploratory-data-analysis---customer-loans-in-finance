from db_utils import load_yaml
from create_df import DataTransform, DataFrameInfo, get_dataframe_info
from matplotlib import pyplot
from statsmodels.graphics.gofplots import qqplot
import missingno as msno 
import numpy as np
import pandas as pd 
import plotly.graph_objects as go
import seaborn as sns



class Plotter:
    '''
    This class returns different visualisations on a provided dataframe for use in EDA
    
    Args:
        dataframe (pd.DataFrame): the dataframe to be visualised
    '''

    def __init__(self, dataframe):
        self.df = dataframe

    def view_missing_vals(self):
        '''This function visualises null and NaN values for the columns in the DataFrame'''
        return msno.matrix(self.df)
    
    def hist(self, column):
        '''This function returns a histogram for the specified column'''
        return sns.histplot(data=self.df, x=column, kde=True)
    
    def heatmap(self):
        '''This function returns a heatmap in order to help visualise collinearity between columns in the DataFrame'''
        corr = self.df.corr()
        mask = np.zeros_like(corr, dtype=np.bool_) #provides a mask on chart to avoid duplicate information
        mask[np.triu_indices_from(mask)] = True

        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        return sns.heatmap(corr, mask=mask, square=True, linewidths=.5, annot=False, cmap=cmap)
  
    def qq_plot(self,column):
        '''This function returns a qq_plot in order to help visualise skew in the specified column of the dataframe'''
        return qqplot(self.df[column] , scale=1 ,line='q', fit=True)

    def box_plot(self):
        '''This function returns boxplots for the number columns in the DataFrame, these can be navigated through by use of the dropdown buttons. For viewing outliers'''
        #return numeric data columns to visualise in box plot    
        cols = self.df.select_dtypes('number').columns
        #list of trace visibilities to allow filtering with a button
        vis = []
        fig = go.Figure()
        col_buttons = []    #for dropdown list of columns
        
        for count, col in enumerate(cols): #enumerate through cols to help set visibility of traces on button
          vis = [False]*len(cols)
          vis[count] = True #sets trace visibilities for each trace when selection made on the dropdown'
          fig.add_trace(go.Box(y=self.df[col], name=''))
          col_button = dict(label=col, method= "update", args=[{"visible": vis},{"title":f'Distribution of data in the <b>{col}</b> column'}])
          col_buttons.append(col_button)
          fig.update(layout_showlegend=False)
        
        fig.update_layout(
            {"updatemenus":[
             {"name":"Select Column",
           "type":"dropdown",
           "showactive":True,
           "buttons":col_buttons,"x":-0.04, "y":1
           }
             ]})
        return fig    

class DataFrameTransform:
    '''
    This class performs a number of transformations on a dataframe from a specified .yaml file. The transformations are imputations based on mean and median as well as column drops.
    These transformations can be performed in isolation or combined in a single call of impute_and_dropna. The remove_outliers method requires a list of columns to be specified.
    '''

    def __init__(self, dataframe, transformations):
        self.df = dataframe
        self.transformations = load_yaml(transformations)
    
    def impute_mean(self, columns: list):
        '''This function imputes na values in the column with the mean value for the column'''
        for col in columns:
            self.df[col] = self.df[col].fillna(value=self.df[col].mean())
        return self.df

    def impute_median(self, columns: list):
        '''This function imputes na values in the column with the median value for the column'''
        for col in columns:
            self.df[col] = self.df[col].fillna(value=self.df[col].median())
        return self.df
    
    def impute_with_col(self):
        '''This function imputes na values in the column with values from another column in the dataframe'''
        col_to_col_imputations = self.transformations['impute_with_col']
        cols_to_change = []
        for d in col_to_col_imputations:
            for k in d:
                cols_to_change.append(k)
        
        for i in range(len(col_to_col_imputations)):
            changes=(col_to_col_imputations[i][cols_to_change[i]])
            for null_cols, value_cols in changes.items():
                self.df[null_cols] = self.df[null_cols].fillna(self.df[value_cols])
            return self.df

    def drop_cols(self, cols: list):
        '''This function drops columns from the DataFrame'''
        self.df.drop(columns=cols, inplace=True)
        return self.df
    
    def drop_rows(self):
        '''This function drops rows containing na data from the DataFrame'''
        self.df.dropna(axis=0, inplace=True)
        return self.df
    
    def log_transform(self):
        '''This function applies log transformations on columns specified in the yaml file'''
        skewed_cols_log = self.transformations['log_transforms']
        for col in skewed_cols_log:
            self.df[col] = self.df[col].map(lambda x: np.log(x) if x > 0 else 0)
        return self.df
    
    def impute_and_dropna(self):
        self.impute_mean(self.transformations["impute_mean"])
        self.impute_median(self.transformations["impute_median"])
        self.impute_with_col()
        self.drop_cols(self.transformations['drop_cols'])
        self.drop_rows()
        return self.df

    def remove_outliers(self, columns: list):
      for outlier_col in columns:
            Q1 = self.df[outlier_col].quantile(0.25)
            Q3 = self.df[outlier_col].quantile(0.75)
            IQR = Q3 - Q1
            # identify outliers
            threshold = 1.5
            outliers = self.df[(self.df[outlier_col] < Q1 - threshold * IQR) | (self.df[outlier_col] > Q3 + threshold * IQR)]
            self.df = self.df.drop(outliers.index)
      return self.df

    def load(self):
        return self.df
    
if __name__ == '__main__':
    

    loan_payments_initial = DataTransform('loan_payments.csv','df_transformations').load()

    transformed_loan_payments = DataFrameTransform(loan_payments_initial, 'drops_and_imputations').impute_and_dropna()

    log_transforms = DataFrameTransform(transformed_loan_payments, 'drops_and_imputations').log_transform()

    outliers = ['annual_inc',
            'funded_amount',
            'int_rate',
            'inq_last_6mths',
            'loan_amount',
            'instalment',
            'total_payment',
            'last_payment_amount',
            'total_rec_int',
            'total_rec_late_fee',
            'collections_12_mths_ex_med']

    log_transformed_no_outliers = DataFrameTransform(log_transforms, 'drops_and_imputations').remove_outliers(outliers)

    collinear_cols = ['funded_amount','funded_amount_inv','out_prncp_inv','total_payment_inv','total_rec_prncp']

    log_transformed_no_outliers = DataFrameTransform(log_transforms, 'drops_and_imputations').drop_cols(collinear_cols)

    log_transformed_no_outliers.to_csv('Data_Post_Transformation.csv')





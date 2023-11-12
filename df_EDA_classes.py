from db_utils import load_yaml
from create_df import DataTransform, DataFrameInfo, get_dataframe_info
import missingno as msno 
import numpy as np
import pandas as pd 
import seaborn as sns
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot
import plotly.graph_objects as go


class Plotter:
    '''
    This class
    '''

    def __init__(self, dataframe):
        self.df = dataframe

    def view_missing_vals(self):
        return msno.matrix(self.df)
    
    def hist(self, column):
        return sns.histplot(data=self.df, x=column, kde=True)
    
    def heatmap(self):
        corr = self.df.corr()
        mask = np.zeros_like(corr, dtype=np.bool_)
        mask[np.triu_indices_from(mask)] = True

        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        return sns.heatmap(corr, mask=mask, square=True, linewidths=.5, annot=False, cmap=cmap)
  
    def qq_plot(self,column):
        return qqplot(self.df[column] , scale=1 ,line='q', fit=True)

    def box_plot(self):
        #return numeric data columns to visualise in box plot    
        cols = self.df.select_dtypes('number').columns
        #list of trace visibilities to allow filtering with a button
        vis = []
        fig = go.Figure()
        col_buttons = []    #for dropdown list of columns
        
        for count, col in enumerate(cols):
          vis = [False]*len(cols)
          vis[count] = True
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
    Docstring for class
    '''

    def __init__(self, dataframe, transformations):
        self.df = dataframe
        self.transformations = load_yaml(transformations)
    
    def impute_mean(self):
        for col in self.transformations["impute_mean"]:
            self.df[col] = self.df[col].fillna(value=self.df[col].mean())
        return self.df

    def impute_median(self):
        for col in self.transformations["impute_median"]:
            self.df[col] = self.df[col].fillna(value=self.df[col].median())
        return self.df
    
    def impute_with_col(self):
        '''Docstring for this method'''
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
        self.df.drop(columns=cols, inplace=True)
        return self.df
    
    def drop_rows(self):
        self.df.dropna(axis=0, inplace=True)
        return self.df
    
    def log_transform(self):
        skewed_cols_log = self.transformations['log_transforms']
        for col in skewed_cols_log:
            self.df[col] = self.df[col].map(lambda x: np.log(x) if x > 0 else 0)
        return self.df
    
    def impute_and_dropna(self):
        self.impute_mean()
        self.impute_median()
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
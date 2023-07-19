from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

class Preprocessing:
    def __init__(self, categorical_cols, number_cols, model_columns):
        self.categorical_cols = categorical_cols
        self.number_cols = number_cols
        self.columns = self.categorical_cols + self.number_cols 
        self.min_max_scaler = None
        self.model_columns = model_columns
        
    
    def transform(self,df):
        
        df = df[self.columns]
        data = pd.get_dummies(df, columns = self.categorical_cols, dtype=float)
        data[self.number_cols] = self.transforms_scaler(np.array(df[self.number_cols]))
        return df.reindex(columns=self.model_columns, fill_value=0)

    def transforms_scaler(self, data): 
        if not self.min_max_scaler:
            self.min_max_scaler = MinMaxScaler().fit(data)
        transform_data = self.min_max_scaler.transform(data)
        return transform_data
import numpy as np
import pandas as pd

class TargetMeanEncoder:
    def __init__(self):
        self.map_ = {}
        self.classes_ = []
        
    def fit(self, X, y):
        '''
        @param X: feature column
        @param y: target column
        '''
        df = pd.concat([X, y], axis=1)
        col = df.columns[0]
        target = df.columns[1]
        
        means = df.groupby(col)[target].mean()
        self.classes_ = list(means.index)
        self.map_     = {self.classes_[i]: means.values[i] for i in range(len(self.classes_))}

    def transform(self, X):
        '''
        @param X: list of values to transform
        '''
        newX = []
        for x in X:
            try:
                newX.append(self.map_[x])
            except KeyError: # if trying to transform a value that never got fit
                newX.append( np.mean(list(self.map_.values())) )
                continue
        return newX
    
    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

class RankLabelEncoder:
    '''
    (Modified) Label Encoder
    Label encoding works fine for ordinal variables, but many of the categorical variables
    are not (necessarily/obviously) ordinal. 
    For example, looking at 'Neighborhood' names or 'LotConfig' one couldn't obviously order 
    them. But, knowing the situation, some neighborhoods (and other property features) tend 
    to be more expensive than others, so we can use this order to encode the feature (i.e. 
    by mean or median price of of observations w/ in same category)
    '''
    def __init__(self):
        self.map_ = {}
        self.classes_ = []
        
    def fit(self, X, y):
        '''
        @param X: feature column
        @param y: target column
        '''
        df = pd.concat([X, y], axis=1)
        col = df.columns[0]
        target = df.columns[1]
        
        self.classes_ = list(df.groupby(col)[target].median().sort_values().index)
        self.map_ = {self.classes_[i]: i for i in range(len(self.classes_))}

    def transform(self, X):
        '''
        @param X: list of values to transform
        '''
        newX = []
        for x in X:
            try:
                newX.append(self.map_[x])
            except KeyError: # if trying to transform a value that never got fit
                newX.append( np.mean(list(self.map_.values())) )
                continue
        return newX
    
    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------- DISTRIBTUIONS ------------------------------------
def data_distribution_scatters(X, y):
    '''
    Plots the distribution of training data against the (continuous) target 
    variable.

    @param X: column vector(s) of features
    @param y: column vector of target data
    '''
    features    = X.columns
    object_cols = [col for col in features if X[col].dtype == "object"]

    for i in range(len(features)):
        fig     = plt.figure(figsize=(20,5))
        feature = features[i]
        x       = X[feature]
        
        if x.dtype == "object":
            # catergorical scatterplot
            sns.swarmplot(x=x, y=y, s=1.5)
            counts = dict(x.value_counts())
            plt.legend(
                [f'{k}: {v}' for k,v in counts.items()], 
                bbox_to_anchor=(1.05,1), 
                loc="upper right",
            )            
                    
        else:
            # quantitative scatterplot
            sns.scatterplot(x=x, y=y)
            counts = dict(x.value_counts())
                    
        plt.title(f'{feature} Distribution (index: {i})', {'fontsize': 16})
        plt.annotate(
            f'Total: {sum(counts.values())}', 
            xy=(0.01, 0.95), 
            xycoords='axes fraction',
        )
        plt.show()

# ------------------------------------------------------------------------------
# ----------------------------- HEATMAPS ---------------------------------------
def features_heatmap(data):
    '''
    Plots the lower triangle of the correlation matrix as a heatmap.

    @param data: df of training data
    '''
    # use the pands .corr() function to compute pairwise correlations for the dataframe
    corr = data.corr()
    # visualise the data with seaborn
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    sns.set_style(style = 'white')
    f, ax = plt.subplots(figsize=(24, 24))
    sns.heatmap(
        corr, 
        ax=ax,
        cbar_kws={"shrink": .5}, 
        cmap='BrBG',
        linewidths=.5, 
        mask=mask, 
        vmin=-1,
        vmax=1,
    );

def target_heatmap(data, target):
    '''
    Plots a heatmap of correlations between features and the target as a column 
    in descending order. 

    @param data: dataframe of training data
    @param target: string of target name (as seen in data)
    '''
    # Features sorted by correlation with targets
    fig, ax = plt.subplots(figsize=(10, 20))
    corr = data.corr()[[target]].sort_values(by=target, ascending=False).drop(target)
    # Heatmap
    heatmap = sns.heatmap(
        corr,
        annot=True,
        ax=ax, 
        cmap='BrBG',
        vmin=-1,
        vmax=1,
    )
    heatmap.set_title(
        f'Features Correlating with {target}', 
        fontdict={'fontsize':12}, 
        pad=16,
    );
# ------------------------------------------------------------------------------

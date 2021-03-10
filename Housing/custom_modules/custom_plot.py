import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from IPython.display import display
from ipywidgets import interact, interactive_output, fixed, Layout, Dropdown, HBox, ToggleButtons

# --------------------------- DISTRIBTUIONS ------------------------------------
def distribution_helper(x, y, data):
    '''
    Plots the distribution of training data against the (continuous) target 
    variable.

    @param x, y: column vector of data
    '''
    x, y = data[x], data[y]
    fig  = plt.figure(figsize=(20,5))

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
                
    plt.xlabel(x.name, {'fontsize': 16})
    plt.ylabel(y.name, {'fontsize': 16})
    plt.annotate(
        f'Total: {sum(counts.values())}', 
        xy=(0.01, 0.95), 
        xycoords='axes fraction',
    )
    plt.show()
    
def interactive_distributions(data, default_y):
    '''
    Plots the distribution of training data against the (continuous) target 
    variable.

    @param data: dataframe
    '''
    x = Dropdown(options=data.columns, description='x')
    y = Dropdown(options=data.columns, value=default_y, description='y')
    
    ui = HBox([x, y])
    out = interactive_output(distribution_helper, {'x': x, 'y': y, 'data': fixed(data)})
    return display(ui, out)

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

def heatmap_helper(type_, data, target): 
    if type_ == 'Lower Triangle Correlation':
        return features_heatmap(data)

    elif type_ == 'Target Correlation':
        return target_heatmap(data, target)
    
    else:
        return None
   
def interactive_heatmap(data, target):
    button = ToggleButtons(
        options=['Lower Triangle Correlation', 'Target Correlation'],
        description='Type: ',
        tooltips=[
            'heatmap of correlations between all features', 
            'heatmap of correlations between each feature and target',
        ],
    )

    out = interactive_output(heatmap_helper, {'type_': button, 'data': fixed(data), 'target': fixed(target)})
    return display(button, out)
# ------------------------------------------------------------------------------

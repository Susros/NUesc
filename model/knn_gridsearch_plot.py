""" Plot for KNN Grid Search Result

This script plot performance line chart of
KNN with three metric and K values from 1 to 
50.

Author: Kelvin Yin
"""

import pickle
import plotly.graph_objects as go

from plotly.subplots import make_subplots

# Grid Search parameters
param_K = range(1, 51)
param_metric = ["Euclidean", "Manhattan", "Chebyshev"]

# Load Grid Search result
try:
    gridsearch = pickle.load(open(OUTPUT_DIR + 'knn_gridsearch.p', 'rb'))
except IOError:
    print("Could not load SVM Grid Search result. Please make sure to run SVM Grid Search before running this script.")

'''
    Performance line chart
'''

fig = go.Figure()

for i in range(3):
    x = list(range(1, 51))
    y = grid_accuracy[i]
    
    fig.add_trace(go.Scatter(x = x, y = y, mode='lines', name=param_metric[i]))

fig.show()
""" SVM Grid Search Plot

This script load Grid Search results and plot heatmap for
C Parameters vs Gamma Parameters vs Accuracy.

Author: Kelvin Yin
"""

import pickle
import plotly.graph_objects as go

from plotly.subplots import make_subplots

# Output Directory
OUTPUT_DIR = 'output/'

# Grid Search Parmaeters for plotting
param_C = ['{1e-04}', '{1e-03}', '{1e-02}', '{1e-01}', '{1.0}', '{1e+01}', '{1e+02}', '{1e+03}', '{1e+04}', '{1e+05}', '{1e+06}', '{1e+07}', '{1e+08}']
param_gamma = ['{1e-11}', '{1e-10}', '{1e-09}', '{1e-08}', '{1e-07}', '{1e-06}', '{1e-05}', '{1e-04}', '{1e-03}', '{1e-02}', '{1e-01}', '{1.0}', '{10.0}']

# Load grid search result
try:
    gridsearch = pickle.load(open(OUTPUT_DIR + 'svm_gridsearch.p', 'rb'))
except IOError:
    print("Could not load SVM Grid Search result. Please make sure to run SVM Grid Search before running this script.")

''' 
Sort out data for plotting.

Construct data for heatmap plotting to the following
matrix:

     g1  g2  g3  ...   gn
    ----------------------------
C1  [v1, v2, v3, ... , vn],
C2  [v1, v2, v3, ... , vn],
Cn  ...

Where g is gamma parameter and C is C parameter

'''

gridsearch_index = 0
heatmap_data = []

# For checking the best parameters
highest_accuracy = 0
highest_accuracy_C_index = 0
highest_accuracy_gamma_index = 0

for i in range(len(param_C)):
    
    # Chunk it for each parmaeter C
    chunk = []

    for j in range(len(param_gamma)):
        
        # Convert accuracy into percentage
        accuracy_perct = round(gridsearch[gridsearch_index] * 100, 2)

        chunk.append(accuracy_perct)

        if (accuracy_perct > highest_accuracy):
            highest_accuracy = accuracy_perct
            highest_accuracy_C_index = i
            highest_accuracy_gamma_index = j

        gridsearch_index += 1

    heatmap_data.append(chunk)

''' Plot Heatmap '''
fig = go.Figure(data = go.Heatmap(z = heatmap_data, x = param_gamma, y = param_C))

fig.update_layout(
    title = 'SVM Grid Search',
    xaxis_title = 'Gamma Parameter',
    yaxis_title = 'C Parameter'
)

fig.show()

''' Show the best parameters '''

print("The best parameters:")
print("==========================")
print("C = ", param_C[highest_accuracy_C_index])
print("Gamma = ", param_gamma[highest_accuracy_gamma_index])
print("Accuracy = ", highest_accuracy)
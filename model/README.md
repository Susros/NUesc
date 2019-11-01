# Training Machine Learning Model

There are two models in this project: Support Vector Machine (SVM) and K-Nearest Neighbour (KNN).

## Requirement

The models are trained and tested in Python3. The following python packages need to be installed:

* sklearn
* pandas
* librosa
* pickle
* numpy
* plotly

The dataset used in this training is __UrbanSound8K__

## Usage

First, download UrbanSound8K dataset and put it in dataset folder: *__dataset/UrbanSound8K__*

### Feature Extraction

Before training the dataset, extract the feature by running:

``` console
python3 feature_extraction.py
```

This will take awhile. When all features are extracted, the features are saved in *__output/__* directory as *mfcc_feature.p*.

### Grid Search

When the feature is extracted, the grid search can be run to get the best parameters for the model as follow:

For SVM:

``` console
python3 svm_gridsearch.py
```

In SVM, there are 13 C parmaeters and gamma parameter values for grid search. The values are as following:

C = {1e-4, 1e-3, 1e-2, 1e-1, 1.0, 1e+1, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6, 1e+7, 1e+8}

gamma = {1e-11, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 1e-02, 1e-01, 1.0, 10.0}

The parameters can be modified in *svm_gridsearch.py*.

For KNN:

``` console
python3 knn_gridsearch.py
```

In KNN, there are three matric: Euclidean, Manhattan, and Chebyshev. The K values range from 1 to 50. Grid search parameters for KNN can be modified in *knn_gridsearch.py*.

The grid search takes a few hours to finish. Once it's done, the grid search results will be saved in *__output/__* directory.

### Plotting Grid Search

The grid search can be plotted into a graph by running:

For SVM:

``` console
python3 svm_gridsearch_plot.py
```

For KNN:

``` console
python3 knn_gridsearch_plot.py
```

From the graph, the best paramters can be obtained and used for training the model.

### Training Model

To train the model, simply just run:

For SVM,

``` console
python3 svm.py
```

For KNN,

``` console
python3 knn.py
```

Once the training is done, model is saved to *__output/__* folder.

Both SVM and KNN are now using the best parameters obtained from grid search. You may change the parameters before running it.
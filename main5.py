import pandas as pd
import numpy as np
from numpy import mean, std, cov, set_printoptions
from scipy.stats import pearsonr, spearmanr, kendalltau
from matplotlib import pyplot
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, SelectFromModel, f_classif, RFE, chi2, f_regression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

names = ['nameWithOwner', 'tag', 'typeRelease','isFirstRow(bool)', 'isNotaMax(bool)',
                    'isLOCchanged(bool)', 'isMetricChanged(bool)', 'qtDias', 'qtDiasChangedRel', 'porcValF(%)', 
                    'deltaLOC(qtd)', 'deltaSLOC(qtd)', 'deltaMIF', 'deltaMIT', 'deltaDiff', 'deltaEff',
                    'deltaTimeH', 'deltaBug', 'deltaFiles(qtd)', 'totalFiles(qtd)']
dataFrame = pd.read_csv("AnaliseFinalRelease3.csv", sep=';', header=0, decimal=',')
array = dataFrame.values
#print(dataFrame)
arrName = array[:,0]
arrIsMetric = array[:,6]
arrQtDias = array[:,7]
arrQtDiasChangedRel = array[:,8]
arrLOC = array[:,10]
arrMetrics = array[:,12:18]
arrLOCeMetrics = np.column_stack((arrLOC, arrMetrics))
arrLOCeSLOCeMetrics = array[:,10:18]
arrDeltaFiles = array[:,18]
arrMIF = array[:,12]
arrMIT = array[:,13]
arrDiff = array[:,14]
arrEff = array[:,15]
arrTime = array[:,16]
arrBug = array[:,17]
#print(arrDeltaFiles)
#print("")
#print(arrLOCeMetrics)
#print("")
#print(arrLOC)
#print("")
#print(z)





#________Univariate Selection________

# ANOVA F-value method is appropriate for numerical inputs and categorical data. 
# This can be used via the f_classif() function. 

data = arrMetrics
scaler = MinMaxScaler()
scaler.fit(data)
X = scaler.transform(data)
print("")
data = arrIsMetric.reshape(-1, 1)
scaler = MinMaxScaler()
scaler.fit(data)
Y = scaler.transform(data)
Y = Y.ravel()
Y = arrIsMetric
#ok

print("\nANOVA F-value - f_classif")
test = SelectKBest(score_func=f_classif, k=5)
fit = test.fit(X, Y)
print(fit.scores_)
features = fit.transform(X)
print("")



# Classification Feature Selection
# Numerical Input, Categorical Output)




#__________Recursive Feature Elimination___________
"""
The Recursive Feature Elimination (or RFE) works by recursively removing attributes and building 
a model on those attributes that remain.
It uses the model accuracy to identify which attributes (and combination of attributes) contribute 
the most to predicting the target attribute.
The example below uses RFE with the logistic regression algorithm to select the top 3 features

#não ok
model = LogisticRegression(solver='lbfgs')
rfe = RFE(model, n_features_to_select=3)
fit = rfe.fit(X, Y)
print("Num Features: %d" % fit.n_features_)
print("Selected Features: %s" % fit.support_)
print("Feature Ranking: %s" % fit.ranking_)

#não ok
model = LogisticRegression()
# create the RFE model and select 3 attributes
rfe = RFE(model, 3)
rfe = rfe.fit(dataset.data, dataset.target)
# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)

#não ok
rfe_selector = RFE(estimator=LogisticRegression(), n_features_to_select=8, step=10, verbose=5)
rfe_selector.fit(X, Y)
rfe_support = rfe_selector.get_support()
print(rfe_support)



#__________Principal Component Analysis___________

# Principal Component Analysis (or PCA) uses linear algebra to transform the dataset into a compressed form.

# Generally this is called a data reduction technique. A property of PCA is that you can choose the number of 
# dimensions or principal component in the transformed result.

#não ok
pca = PCA(n_components=8)
fit = pca.fit(arrLOCeSLOCeMetrics)
print("Explained Variance: %s" % fit.explained_variance_ratio_)
print(fit.components_)
"""


#___________Feature Importance___________

print("\nFeature Importance")
#Bagged decision trees like Random Forest and Extra Trees can be used to estimate the importance of features.
Y=arrIsMetric.flatten().astype(int)
model = ExtraTreesClassifier(n_estimators=5)
model.fit(arrMetrics, Y)
print(model.feature_importances_)


#___________Regression Feature Selection__________
"""
(Numerical Input, Numerical Output)
This section demonstrates feature selection for a regression problem that as numerical inputs 
and numerical outputs.

Feature selection is performed using Pearson’s Correlation Coefficient via the f_regression() function.
"""
print("\nRegression Feature Selection - f_regression")
Y=arrIsMetric.flatten().astype(int)
#não OK
fs = SelectKBest(score_func=f_regression, k=5)
X_selected = fs.fit_transform(X, Y)
print(X_selected)
"""
#não OK
#Y=arrLOC
model = ExtraTreesClassifier()
model.fit(X, Y)
# display the relative importance of each attribute
print(model.feature_importances_)
"""

#___________Regression Feature Selection__________

print("\nRegression Feature Selection - LogisticRegression")
Y=arrIsMetric.flatten().astype(int)
embeded_lr_selector = SelectFromModel(LogisticRegression(penalty="l2"), max_features=8)
embeded_lr_selector.fit(arrLOCeSLOCeMetrics, Y)

embeded_lr_support = embeded_lr_selector.get_support()
print(embeded_lr_support)

"""
#___________Tree-based: SelectFromModel__________

Y=arrQtDiasChangedRel.flatten().astype(int)
embeded_rf_selector = SelectFromModel(RandomForestClassifier(n_estimators=8), max_features=8)
embeded_rf_selector.fit(arrLOCeSLOCeMetrics, Y)

embeded_rf_support = embeded_rf_selector.get_support()
print(embeded_rf_support)


# put all selection together

feature_selection_df = pd.DataFrame({'Feature':feature_name, 'Pearson':cor_support, 'Chi-2':chi_support, 'RFE':rfe_support, 'Logistics':embeded_lr_support,
                                    'Random Forest':embeded_rf_support})
# count the selected times for each feature
feature_selection_df['Total'] = np.sum(feature_selection_df, axis=1)
# display the top 100
feature_selection_df = feature_selection_df.sort_values(['Total','Feature'] , ascending=False)
feature_selection_df.index = range(1, len(feature_selection_df)+1)
feature_selection_df.head(num_feats)


"""
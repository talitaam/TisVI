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
dataFrame = pd.read_csv("AnaliseFinalRelease2.csv", sep=';', header=0, decimal=',')
array = dataFrame.values
#print()
arrName = array[:,0]
arrIsMetric = array[:,6]
arrQtDias = array[:,7]
arrQtDiasChangedRel = array[:,8]
arrLOC = array[:,10]
arrSLOC = array[:,11]
arrLOCeSLOC = array[:,10:12]
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


#_______Test Dataset_________

data1 = arrLOC
data2 = arrMIT
print('data1: mean=%.3f stdv=%.3f' % (mean(data1), std(data1)))
print('data2: mean=%.3f stdv=%.3f' % (mean(data2), std(data2)))
# plot
pyplot.scatter(data1, data2)
pyplot.show()
"""

#___________Covariance___________

#Variables can be related by a linear relationship. 
#This is a relationship that is consistently additive across the two data samples.

#This relationship can be summarized between two variables, called the covariance. 
#It is calculated as the average of the product between the values from each sample, 
#where the values haven been centered (had their mean subtracted).

#The sign of the covariance can be interpreted as whether the two variables change in the same 
#direction (positive) or change in different directions (negative). 

data1 = arrLOC
data2 = array[:,12]
covariance = cov(data1, data2)
print(covariance)

#___________Pearson’s Correlation___________


The Pearson correlation coefficient (named for Karl Pearson) can be used to summarize the 
strength of the linear relationship between two data samples.

The coefficient returns a value between -1 and 1 that represents the limits of correlation from a 
full negative correlation to a full positive correlation. A value of 0 means no correlation. 
The value must be interpreted, where often a value below -0.5 or above 0.5 indicates a notable correlation, 
and values below those values suggests a less notable correlation.

arrMIF = array[:,12]
arrMIT = array[:,13]
arrDiff = array[:,14]
arrEff = array[:,15]
arrTime = array[:,16]
arrBug = array[:,17]
arrQtDiasChangedRel = array[:,8]
arrDeltaFiles = array[:,18]

print("")
data1 = arrQtDiasChangedRel
data2 = arrBug
corr, p = pearsonr(data1, data2)
print('Pearsons correlation: %.3f' % corr)
alpha = 0.05
if p > alpha:
	print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
else:
	print('Samples are correlated p=%.3f' % p)


#nao funcionou
def cor_selector(X, y,num_feats):
    cor_list = []
    feature_name = X.columns.tolist()
    # calculate the correlation with y for each feature
    for i in X.columns.tolist():
        cor = np.corrcoef(X[i], y)[0, 1]
        cor_list.append(cor)
    # replace NaN with 0
    cor_list = [0 if np.isnan(i) else i for i in cor_list]
    # feature name
    cor_feature = X.iloc[:,np.argsort(np.abs(cor_list))[-num_feats:]].columns.tolist()
    # feature selection? 0 for not select, 1 for select
    cor_support = [True if i in cor_feature else False for i in feature_name]
    return cor_support, cor_feature
X = dataFrame.filter(items=['deltaLOC(qtd)']).values
y = dataFrame.filter(items=['deltaMIF']).values
num_feats = 2
cor_support, cor_feature = cor_selector(X, y,num_feats)
print(str(len(cor_feature)), 'selected features')

"""


#___________Spearman’s Correlation___________


#Two variables may be related by a nonlinear relationship, such that the relationship is stronger 
#or weaker across the distribution of the variables.

#As a statistical hypothesis test, the method assumes that the samples are uncorrelated (fail to reject H0).

#As with the Pearson correlation coefficient, the scores are between -1 and 1 for perfectly 
#negatively correlated variables and perfectly positively correlated respectively.



coef, p = spearmanr(data1, data2)
print('Spearmans correlation coefficient: %.3f' % coef)
# interpret the significance
alpha = 0.05
if p > alpha:
	print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
else:
	print('Samples are correlated p=%.3f' % p)
"""
The statistical test reports a strong positive correlation with a value of 0.9. 
The p-value is close to zero, which means that the likelihood of observing the data given 
that the samples are uncorrelated is very unlikely (e.g. 95% confidence) and that we can reject 
the null hypothesis that the samples are uncorrelated.

#___________Kendall’s Rank Correlation___________

The intuition for the test is that it calculates a normalized score for the number of matching or 
concordant rankings between the two samples. As such, the test is also referred to as Kendall’s concordance test.

The test takes the two data samples as arguments and returns the correlation coefficient and the p-value. 
"""

coef, p = kendalltau(data1, data2)
print('Kendall correlation coefficient: %.3f' % coef)
# interpret the significance
alpha = 0.05
if p > alpha:
	print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
else:
	print('Samples are correlated p=%.3f' % p)
"""
The p-value is close to zero (and printed as zero), as with the Spearman’s test, 
meaning that we can confidently reject the null hypothesis that the samples are uncorrelated.


pyplot.scatter(data1, data2)
pyplot.show()


#________Chi-Squared________

X = arrMetrics
Y = arrIsMetric
print("")
data = X
scaler = MinMaxScaler()
scaler.fit(data)
X = scaler.transform(data)
print("")
Y=arrIsMetric.flatten().astype(int)
print("")
print("")
#X_norm = MinMaxScaler().fit_transform(X)
chi_selector = SelectKBest(score_func=chi2, k=6)
chi_selector.fit(X, Y)
chi_support = chi_selector.get_support()
print(chi_support)
#chi_feature = X[:,chi_support]
#print(str(len(chi_feature)), 'selected features')
print("")
test = SelectKBest(score_func=chi2, k=6)
fit = test.fit(X, Y)

# Summarize scores
print(fit.scores_)

#features = fit.transform(X)
# Summarize selected features
#print(features[0:5,:])

"""




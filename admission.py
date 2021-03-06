    # -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 09:59:31 2019

@author: Simon
This file is for a interview question.
@copyright 2019
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler
#from statsmodels.stats.outliers_influence import summary_table
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
#from sklearn import preprocessing
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
import os
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import confusion_matrix 
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score


'''
This part is for read data file
'''
dataF = pd.read_csv("data.csv")
dataF.head()
#print(data.info())
dataD = dataF.describe() #print statistical information for this data file, ie: mean, std
Serial_No = dataF['Serial No.']

'''
第一步改名字纯属瞎搞啊哈哈哈，但原版LOR后面有空格，我rename之后把空格去掉了
'''
dataF.rename(columns = {'Chance of Admit ':'Admit Prob', 'LOR ':'LOR'}, inplace = True)
dataF.drop(labels = 'Serial No.', axis = 1, inplace = True) #drop out serial No.(useless)

'''
预测各个指标之间的关系
'''
dataVec = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR', 'Research', 'CGPA']
plt.figure(figsize = (10,40))

for i in range(len(dataVec)):
    plt.subplot(7,1,i+1)
    plt.scatter(dataF['Admit Prob'], dataF[dataVec[i]], color = 'blue')
    plt.title('Correlation between Chance of Admit and {}'.format(dataVec[i]))

plt.show()

'''
上面的和下面直接调sns function可以只写一个
'''

'''
用correlation matrix确认
'''
fig, ax = plt.subplots(figsize = (15,15))
sns.heatmap(dataF.corr(), annot = True, cmap = 'Oranges')

'''
这里根据correlation选取了三个重要的标签，分别为cgpa，gre和toefl
分别画distribution graph, swarm graph和回归后的图
'''
plt.figure(figsize = (20,10))
plt.subplot(2,2,1)
sns.distplot(dataF['CGPA'])
plt.title('Distribution of CGPA among all applicants')

plt.subplot(2,2,2)
sns.swarmplot(dataF['CGPA'], dataF['Admit Prob'])
plt.title('Swarm plot of CGPA and Chance of Admit')

plt.subplot(2,1,2)
sns.regplot(dataF['CGPA'], dataF['Admit Prob'])
plt.title('Regression graph of CGPA Vs. Chance of Admit')

#print('===============================================')

'''
graphs for GRE score
'''
plt.figure(figsize = (20,10))
plt.subplot(2,2,1)
sns.distplot(dataF['GRE Score'])
plt.title('Distribution of GRE Score among all applicants')

plt.subplot(2,2,2)
sns.swarmplot(dataF['GRE Score'], dataF['Admit Prob'])
plt.title('Swarm plot of GRE Score and Chance of Admit')

plt.subplot(2,1,2)
sns.regplot(dataF['GRE Score'], dataF['Admit Prob'])
plt.title('Regression graph of GRE Score Vs. Chance of Admit')

print('/n')

'''
graphs for TOEFL
'''
plt.figure(figsize = (20,10))
plt.subplot(2,2,1)
sns.distplot(dataF['TOEFL Score'])
plt.title('Distribution of TOEFL Score among all applicants')

plt.subplot(2,2,2)
sns.swarmplot(dataF['TOEFL Score'], dataF['Admit Prob'])
plt.title('Swarm plot of TOEFL Score and Chance of Admit')

plt.subplot(2,1,2)
sns.regplot(dataF['TOEFL Score'], dataF['Admit Prob'])
plt.title('Regression graph of TOEFL Score Vs. Chance of Admit')

'''
A quick look at other factors that affect admission probability
ie: university rating, SOP and research experience
'''
fig, ax = plt.subplots(figsize = (10,6))
sns.countplot(dataF['University Rating'])
plt.title('University Rating')
plt.ylabel('Number of applicants')

fig, ax = plt.subplots(figsize = (10,6))
sns.countplot(dataF['SOP'])
plt.title('SOP Result')
plt.ylabel('Number of applicants')

fig, ax = plt.subplots(figsize = (10,6))
sns.countplot(dataF['Research'])
plt.title('Research experience')
plt.ylabel('Number of applicants')
ax.set_xticklabels(['No experience', 'Has experience'])

'''
Prepare data for linear regression and calculate coe for simple LR
'''
X = dataF.drop(['Admit Prob', 'Research'], axis = 1)
Y = dataF['Admit Prob']

smodel = LinearRegression()
smodel.fit(X,Y)
print('Coefficients are: ', smodel.coef_)
print('Interception is: ', smodel.intercept_)

X = sm.add_constant(X)
model1 = sm.OLS(Y,X).fit()
modelS = model1.summary()
print(modelS)

'''
By looking at the P value(assume 95% CI) we can conclude that university rating and SOP has nearly zero effect repsect to the admission chance
now lets do LR
'''
y = dataF['Admit Prob'].values
x = dataF.drop(['Admit Prob'], axis = 1)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 84)
#Normalization
X_scaler = MinMaxScaler(feature_range = (0,1))
x_train[x_train.columns] = X_scaler.fit_transform(x_train[x_train.columns])
x_test[x_test.columns] = X_scaler.fit_transform(x_test[x_test.columns])
#base on 0.8/0.2 rate to change data to 0,1
y_train_bin = [1 if each > 0.8 else 0 for each in y_train]
y_test_bin = [1 if each > 0.8 else 0 for each in y_test]
y_train_bin = np.array(y_train_bin)
y_test_bin = np.array(y_test_bin)

lr = LinearRegression()
lr.fit(x_train, y_train)
y_Plr = lr.predict(x_test)

print('The real value for y_test[1] is: ' + str(y_test[1]) + ', ------> the predict value for y_test[1] is: ' + str(lr.predict(x_test.iloc[[1],:])))
print('The real value for y_test[2] is: ' + str(y_test[2]) + ', ------> the predict value for y_test[2] is: ' + str(lr.predict(x_test.iloc[[2],:])))

#lr_score = (lr.score(x_test, y_test))
#print(lr_score)

print('r square score: ', r2_score(y_test, y_Plr))
y_Plr_train = lr.predict(x_train)
print('r square score for trained dataset: ', r2_score(y_train, y_Plr_train))

'''
This is the method of logistic regression
'''
LogR = LogisticRegression()
LogR.fit(x_train, y_train_bin)
print('The score is: ', LogR.score(x_test, y_test_bin))
print('The real value for y_test[1] is: ' + str(y_test_bin[1]) + ', ------> the predict value for y_test[1] is: ' + str(LogR.predict(x_test.iloc[[1],:])))
print('The real value for y_test[2] is: ' + str(y_test_bin[2]) + ', ------> the predict value for y_test[2] is: ' + str(LogR.predict(x_test.iloc[[2],:])))

#let's compute the confusion matrix

conM = confusion_matrix(y_test_bin, LogR.predict(x_test))
fig, ax = plt.subplots(figsize = (8,8))
sns.heatmap(conM, annot = True, linewidths = 0.25, linecolor = 'white', fmt = '.0f', ax = ax)
plt.title('confusion matrix for data set')
plt.ylabel('Real value')
plt.xlabel('Predict value')
plt.show()

print('precision score is: ', precision_score(y_test_bin, LogR.predict(x_test)))
print('Recall score is: ', recall_score(y_test_bin, LogR.predict(x_test)))






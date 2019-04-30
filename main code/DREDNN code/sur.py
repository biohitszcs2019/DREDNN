from __future__ import print_function
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
import bp
import test

import test


file1 = './data/GEO1/example_expression.csv'


expression = np.loadtxt(file1, dtype=float, delimiter=",")


label_vec = np.array(expression[:,-1], dtype=int)
expression = np.array(expression[:,:-1])


expression = (expression-expression.min(axis=0))/(expression.max(axis=0)-expression.min(axis=0))
print(expression.shape)


labels = []
for l in label_vec:
        if l == 1:
            labels.append([0,1])
        else:
            labels.append([1,0])
labels = np.array(labels,dtype=int)

print(expression.shape)
print(labels.shape)

y_s = test.test(expression,labels)

print(y_s)

s = []

for item in y_s:
    if item[0]>0.5:
        s.append((0))
    else:
        s.append(1)
print(s)

fr = pd.DataFrame(s)
fr.to_csv('./result/fr.csv')






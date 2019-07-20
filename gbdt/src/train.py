# coding: utf8
"""Usage:
    模型训练
"""
import sys
import xgboost as xgb

# 训练集
file_train = sys.argv[1]

dtrain = xgb.DMatrix(file_train)

param = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'binary:logistic'}
num_round = 2

bst = xgb.train(param, dtrain, num_round)

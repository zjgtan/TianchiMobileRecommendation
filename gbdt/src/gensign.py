# coding: utf8
"""Usage:
    特征签名
"""

import sys

feature_idx_dict = {}
for line in file("./conf/feature_idx.txt"):
    toks = line.rstrip().split("\t")
    feature_idx_dict[toks[0]] = toks[1]

for line in sys.stdin:
    date, userid_itemid, label, features = line.rstrip().split("\t")
    ins = []
    for feature, value in features.iteritems():
        feature_idx = feature_idx_dict[feature]
        ins.append("%s:%f" % (featrue_idx, value))

    print "%s %s" % (label, " ".join(ins))


# usage: offline训练和预测

cat ./data/offline_train.dat | python ./src/featrue_extract.py > data/offline_train.ins
cat ./data/offline_train.ins | python ./src/gensign.py > data/offline_train.sign
cat ./data/offline_test.dat | python ./src/featrue_extract.py > data/offline_test.ins
cat ./data/offline_test.ins | python ./src/gensign.py > data/offline_test.sign

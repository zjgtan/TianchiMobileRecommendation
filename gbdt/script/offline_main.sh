# usage: offline训练和预测

echo "offline train feature extract"
cat ./data/offline_train.dat | python ./src/feature_extract.py > data/offline_train.ins
echo "offline train gensign"
cat ./data/offline_train.ins | python ./src/gensign.py > data/offline_train.sign
echo "offline test feature extract"
cat ./data/offline_test.dat | python ./src/feature_extract.py > data/offline_test.ins
echo "offline test gensign"
cat ./data/offline_test.ins | python ./src/gensign.py > data/offline_test.sign

python ./src/train.py ./data/offline_train.ins

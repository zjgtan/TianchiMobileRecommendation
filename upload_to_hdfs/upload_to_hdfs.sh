source /mnt/storage00/chenjiawei/project/chenjiawei/utils/common_utils.sh

set -x

mkdir -p ./upload_to_hdfs/user_data
cat ./fresh_comp_offline/tianchi_fresh_comp_train_user.csv | python ./upload_to_hdfs/trans_user_data.py ./upload_to_hdfs/user_data 

mkdir -p ./upload_to_hdfs/item_data
cat ./fresh_comp_offline/tianchi_fresh_comp_train_item.csv | python ./upload_to_hdfs/trans_item_data.py ./upload_to_hdfs/item_data 

USER_DATA_PATH="/department/buss_product/chenjiawei/mobile_recommendation/tianchi_fresh_comp_train_user/"

${HADOOP_BIN} fs -mkdir -p ${USER_DATA_PATH}

start_date=20141118
while [ $start_date -ne 20141219 ]
do
    ${HADOOP_BIN} fs -mkdir -p ${USER_DATA_PATH}/log_date=${start_date}
    ${HADOOP_BIN} fs -put ./upload_to_hdfs/user_data/tianchi_fresh_comp_train_user_${start_date}.csv ${USER_DATA_PATH}/log_date=${start_date}
    start_date=`date -d "1 days ${start_date}" +%Y%m%d`
done

ITEM_DATA_PATH=/department/buss_product/chenjiawei/mobile_recommendation/tianchi_fresh_comp_train_item/
${HADOOP_BIN} fs -mkdir -p ${ITEM_DATA_PATH}
${HADOOP_BIN} fs -put ./upload_to_hdfs/item_data/* ${ITEM_DATA_PATH}

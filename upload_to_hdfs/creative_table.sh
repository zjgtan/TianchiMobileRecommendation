hive -e "
CREATE EXTERNAL TABLE sycpb.tmp_mobile_recommendation_user_behavoir(
    user_id string,
    item_id string,
    behavior_type int,
    user_geohash string,
    item_category string,
    log_date string,
    log_hour string)
PARTITIONED BY (
    log_date string
)
ROW FORMAT delimited fields terminated by ','
LOCATION 'viewfs://jssz-bigdata-cluster/department/buss_product/chenjiawei/mobile_recommendation/tianchi_fresh_comp_train_user/'
"

hive -e "
CREATE EXTERNAL TABLE sycpb.tmp_mobile_recommendation_item(
    item_id string,
    item_geohash string,
    item_category string,
)
ROW FORMAT delimited fields terminated by ','
LOCATION 'viewfs://jssz-bigdata-cluster/department/buss_product/chenjiawei/mobile_recommendation/tianchi_fresh_comp_train_item/'
"


set -x 

hive -e "
CREATE EXTERNAL TABLE sycpb.tmp_mobile_recommendation_evalset(
    user_id string,
    item_id string
)
PARTITIONED BY (
    log_date string
)
ROW FORMAT delimited fields terminated by ','
LOCATION 'viewfs://jssz-bigdata-cluster/department/buss_product/chenjiawei/mobile_recommendation/evalset/'
"

hive -e "
    INSERT OVERWRITE TABLE sycpb.tmp_mobile_recommendation_evalset PARTITION(log_date=20141218)  
    SELECT
        user_id,
        item_id
    FROM
        sycpb.tmp_mobile_recommendation_user_behavior
    WHERE
        log_date=20141218
        AND
        behavior_type=4
    GROUP BY
        user_id, item_id




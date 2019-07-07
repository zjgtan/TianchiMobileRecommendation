set -x 

hive -e "
CREATE EXTERNAL TABLE sycpb.tmp_mobile_recommendation_dataset(
    user_id string,
    item_id string,
    label int,
    example_age int
)
PARTITIONED BY (
    log_date string
)
ROW FORMAT delimited fields terminated by ','
LOCATION 'viewfs://jssz-bigdata-cluster/department/buss_product/chenjiawei/mobile_recommendation/dataset/'
"


start_date=20141125
while [ ${start_date} -ne 20141219 ]
do
    hive -e "
        INSERT OVERWRITE TABLE sycpb.tmp_mobile_recommendation_dataset PARTITION(log_date=${start_date})  
        SELECT
            t1.user_id,
            t1.item_id,
            case when t2.label = 1 then 1 else 0 end as label
        FROM
        (
            SELECT
                user_id,
                item_id
            FROM
                sycpb.tmp_mobile_recommendation_user_behavoir
            WHERE
                datediff(
                    from_unixtime(unix_timestamp(\"${start_date}\", 'yyyyMMdd'), 'yyyy-MM-dd'),
                    from_unixtime(unix_timestamp(log_date, 'yyyyMMdd'), 'yyyy-MM-dd')) <= 7
                AND
                datediff(
                    from_unixtime(unix_timestamp(\"${start_date}\", 'yyyyMMdd'), 'yyyy-MM-dd'),
                    from_unixtime(unix_timestamp(log_date, 'yyyyMMdd'), 'yyyy-MM-dd')) > 1
                AND
                behavior_type in (2, 3, 4)
            UNION ALL
                SELECT
                    user_id,
                    item_id
                FROM
                    sycpb.tmp_mobile_recommendation_user_behavoir
                WHERE
                    datediff(
                        from_unixtime(unix_timestamp(\"${start_date}\", 'yyyyMMdd'), 'yyyy-MM-dd'),
                        from_unixtime(unix_timestamp(log_date, 'yyyyMMdd'), 'yyyy-MM-dd')) = 1
                GROUP BY
                    user_id, item_id
        ) t1
        LEFT JOIN
        (
            SELECT
                user_id,
                item_id,
                1 as label
            FROM
                sycpb.tmp_mobile_recommendation_user_behavoir
            WHERE
                log_date=\"${start_date}\"
                AND
                behavior_type=4
            GROUP BY
                user_id, item_id
        ) t2
        ON
            t1.user_id = t2.user_id and t1.item_id = t2.item_id
        "

    start_date=`date -d "1 day ${start_date}" +%Y%m%d`
    break
done


select
    count(*),
    sum(if(flag == 1, 1, 0)),
    sum(if(flag == 1, 1, 0)) / count(*) * 100
from
(
select
    t1.user_id,
    t1.item_id,
    t2.flag
from
(
select 
    user_id,
    item_id,
    log_date
from 
    sycpb.tmp_mobile_recommendation_user_behavoir 
where 
    log_date>=20141119 and log_date <= 20141218
    and
    behavior_type=4
group by
    user_id, item_id, log_date
) t1
left join
(
select
    user_id,
    item_id,
    flag,
    log_date
from
(
select
    user_id,
    item_id,
    1 as flag,
    case when log_date != 20141130 then log_date + 1 else 20141201 end as  log_date
from 
    sycpb.tmp_mobile_recommendation_user_behavoir 
where 
    log_date>=20141118 and log_date <= 20141217
    and
    behavior_type = 1
) t4
group by
    user_id, item_id, flag, log_date
)t2
on t1.user_id = t2.user_id and t1.item_id = t2.item_id and t1.log_date = t2.log_date
) t3

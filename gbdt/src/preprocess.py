# coding: utf8
import re

def load_user_behavior(filename):
    user_behavior_dict = {}
    for ix, line in enumerate(file(filename)):
        if ix == 0:
            continue
        user_id, item_id, behavior_type, user_geohash, item_category, time = line.rstrip().split(",")
        date, hour = time.split(" ")
        date = re.sub("-", "", date)
        user_behavior_dict.setdefault(date, {})
        user_behavior_dict[date].setdefault(behavior_type, [])
        user_behavior_dict[date][behavior_type].append([user_id, item_id, user_geohash, item_category, hour])

    return user_behavior_dict

def do_daily_behavior_count(user_behavior_dict, type):
    behavior_count_dict = {}
    for date in user_behavior_dict:
        behavior_count_dict[date] = {}
        for behavior_type, behaviors in user_behavior_dict[date].iteritems():
            behavior_count_dict[date][behavior_type] = {}
            for record in behaviors:
                if type == "userid_itemid":
                    key = "%s_%s" % (record[0], record[1])
                elif type == "userid_itemcate":
                    key = "%s_%s" % (record[0], record[3])
                else:
                    continue

                behavior_count_dict[date][behavior_type].setdefault(key, 0)
                behavior_count_dict[date][behavior_type][key] += 1

    return behavior_count_dict

def do_aggregate_behavior_count(user_behavior_count_dict, window_size):
    aggregate_count_dict = {}
    user_behavior_count_list = sorted(user_behavior_count_dict.items(), key = lambda (x, y): x)
    for i in range(len(user_behavior_count_list)):
        for 


def main():
    user_behavior_dict = load_user_behavior("./data/tianchi_fresh_comp_train_user.csv")
    daily_user_item_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "userid_itemid")
    daily_user_itemcate_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "userid_itemcate")


    # 统计特征
    user_item_behavior_aggregate_count_dict = {}
    for window_size in [1, 3, 7]:
        last_nday_user_item_behavior_sum_dict[window_size] = do_last_nday_behavior_sum(daily_user_item_behavior_count_dict, window_size)
        
    

if __name__ == "__main__":
    main()

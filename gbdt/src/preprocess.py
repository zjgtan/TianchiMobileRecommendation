# coding: utf8
import re
import sys
import datetime

def load_user_behavior(filename):
    user_behavior_dict = {}
    # 初始化日期
    date = "20141118"
    while int(date) <= 20141218:
        user_behavior_dict[date] = {}
        date = (datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(1)).strftime("%Y%m%d")
    
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
                elif type == "userid":
                    key = record[0]
                elif type == "itemid":
                    key = record[1]
                elif type == "itemcate":
                    key = record[3]
                else:
                    continue

                behavior_count_dict[date][behavior_type].setdefault(key, 0)
                behavior_count_dict[date][behavior_type][key] += 1

    return behavior_count_dict

def do_daily_count_sum(last_nday_daily_counts):
    daily_count_sum_dict = {}
    for daily_count_dict in last_nday_daily_counts:
        for behavior_type, count_dict in daily_count_dict.iteritems():
            daily_count_sum_dict.setdefault(behavior_type, {})
            for key, count in count_dict.iteritems():
                daily_count_sum_dict[behavior_type].setdefault(key, 0)
                daily_count_sum_dict[behavior_type][key] += count

    return daily_count_sum_dict


def do_last_nday_sum(daily_count_dict, window_size):
    last_nday_sum_dict = {}
    daily_count_list = sorted(daily_count_dict.iteritems(), key = lambda (x, y): x)

    for i in range(7, len(daily_count_list)):
        date = daily_count_list[i][0]
        last_nday_daily_counts = [daily_count_list[j][1] for j in range(i - window_size, i)]
        last_nday_sum_dict[date] = do_daily_count_sum(last_nday_daily_counts)

    return last_nday_sum_dict

def last_nday_sum_dict_to_file(last_nday_sum_dict, filename):
    fd = open(filename, "w")
    for window_size in last_nday_user_item_behavior_sum_dict:
        for date in last_nday_user_item_behavior_sum_dict[window_size]:
            for behavior_type in last_nday_user_item_behavior_sum_dict[window_size][date]:
                for key, value in last_nday_user_item_behavior_sum_dict[window_size][date][behavior_type].iteritems():
                    print >> fd, "%d\t%s\t%s\t%s\t%d" % (window_size, date, behavior_type, key, value)

def main():
    print >> sys.stderr, "load user behavior"
    user_behavior_dict = load_user_behavior("./data/tianchi_fresh_comp_train_user.csv")
    print >> sys.stderr, "daily user item behavior count"
    daily_user_item_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "userid_itemid")
    print >> sys.stderr, "daily user behavior count"
    daily_user_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "userid")
    print >> sys.stderr, "daily user itemcate behavior count"
    daily_user_itemcate_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "userid_itemcate")
    print >> sys.stderr, "daily item behavior count"
    daily_item_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "itemid")
    print >> sys.stderr, "daily itemcate behavior count"
    daily_itemcate_behavior_count_dict = do_daily_behavior_count(user_behavior_dict, "itemcate")

    # 统计特征
    print >> sys.stderr, "sum last nday user item behavior"
    last_nday_user_item_behavior_sum_dict = {}
    for window_size in [1, 3, 7]:
        last_nday_user_item_behavior_sum_dict[window_size] = do_last_nday_sum(daily_user_item_behavior_count_dict, window_size)

    last_nday_sum_dict_to_file(last_nday_user_item_behavior_sum_dict, "./data/last_nday_user_item_behavior_sum.txt")

    print >> sys.stderr, "sum last nday user behavior"
    last_nday_user_behavior_sum_dict = {}
    for window_size in [1, 3, 7]:
        last_nday_user_behavior_sum_dict[window_size] = do_last_nday_sum(daily_user_behavior_count_dict, window_size)

    last_nday_sum_dict_to_file(last_nday_user_behavior_sum_dict, "./data/last_nday_user_behavior_sum.txt")

    print >> sys.stderr, "sum last nday user itemcate behavior"
    last_nday_user_itemcate_behavior_sum_dict = {}
    for window_size in [1, 3, 7]:
        last_nday_user_itemcate_behavior_sum_dict[window_size] = do_last_nday_sum(daily_user_itemcate_behavior_count_dict, window_size)

    last_nday_sum_dict_to_file(last_nday_user_itemcate_behavior_sum_dict, "./data/last_nday_user_itemcate_behavior_sum.txt")

    print >> sys.stderr, "sum last nday item behavior"
    last_nday_item_behavior_sum_dict = {}
    for window_size in [1, 3, 7]:
        last_nday_item_behavior_sum_dict[window_size] = do_last_nday_sum(daily_item_behavior_count_dict, window_size)

    last_nday_sum_dict_to_file(last_nday_item_behavior_sum_dict, "./data/last_nday_item_behavior_sum.txt")

    print >> sys.stderr, "sum last nday itemcate behavior"
    last_nday_itemcate_behavior_sum_dict = {}
    for window_size in [1, 3, 7]:
        last_nday_itemcate_behavior_sum_dict[window_size] = do_last_nday_sum(daily_itemcate_behavior_count_dict, window_size)

    last_nday_sum_dict_to_file(last_nday_itemcate_behavior_sum_dict, "./data/last_nday_itemcate_behavior_sum.txt")

if __name__ == "__main__":
    main()

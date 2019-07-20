# coding: utf8
"""Usage:
    特征抽取
"""
import sys
import json

def load_lastnday_behavior_data(filename):
    lastnday_behavior_dict = {}
    for line in file(filename):
        window_size, date, behavior_type, key, count = line.rstrip().split("\t")
        lastnday_behavior_dict.setdefault(key, {})
        lastnday_behavior_dict[key].setdefault(date, {})
        lastnday_behavior_dict[key][date].setdefault(behavior_type, {})


    return lastnday_behavior_dict

def main():
    lastnday_behavior_dict = {}
    lastnday_behavior_dict["userid"] = load_lastnday_behavior_data("./data/last_nday_user_behavior_sum.txt")
    lastnday_behavior_dict["itemid"] = load_lastnday_behavior_data("./data/last_nday_item_behavior_sum.txt")
    lastnday_behavior_dict["itemcate"] = load_lastnday_behavior_data("./data/last_nday_itemcate_behavior_sum.txt")
    lastnday_behavior_dict["userid_itemid"] = load_lastnday_behavior_data("./data/last_nday_user_item_behavior_sum.txt")
    lastnday_behavior_dict["userid_itemcate"] = load_lastnday_behavior_data("./data/last_nday_user_itemcate_behavior_sum.txt")

    for line in sys.stdin:
        date, user_item, label = line.rstrip().split("\t")
        userid, itemid = user_item.split("_")
        record = {"userid": userid, "itemid": itemid, "date": date}

        features = {}

        # 历史活跃频次特征
        for key in ["userid", "itemid", "userid_itemid"]:
            for behavior_type in ["1", "2", "3", "4"]:
                for window_size in ["1", "3", "7"]:
                    feature_name = "sum_%s_last%sd_%s" % (key, window_size, behavior_type)
                    try:
                        features[feature_name] = lastnday_behavior_dict[key][record[key]][date][behavior_type]
                    except:
                        features[feature_name] = 0

        print line.rstrip() + "\t" + json.dumps(features)


if __name__ == "__main__":
    main()



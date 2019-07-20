# coding: utf8
"""Usage:
   划分数据集
"""
def load_user_behavior(filename):
    user_behavior_dict = {}
    # 初始化日期
    date = "20141118"
    while int(date) <= 20141219:
        user_behavior_dict[date] = {}
        for behavior_type in [1, 2, 3, 4]:
            user_behavior_dict[date]["%d" % (behavior_type)] = set()

        date = (datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(1)).strftime("%Y%m%d")
    
    for ix, line in enumerate(file(filename)):
        if ix == 0:
            continue
        user_id, item_id, behavior_type, user_geohash, item_category, time = line.rstrip().split(",")
        date, hour = time.split(" ")
        date = re.sub("-", "", date)
        user_behavior_dict.setdefault(date, {})
        user_behavior_dict[date].setdefault(behavior_type, set())
        user_behavior_dict[date][behavior_type].add("%s_%s" % (user_id, item_id))

    return user_behavior_dict

def load_item_subset(filename):
    items = set()
    for ix, line in enumerate(file(filename)):
        if ix == 0:
            continue
        toks = line.rstrip().split(",")
        items.add(toks[0])
    return items

def get_user_item_label_data(daily_user_behavior_list):
    daily_user_item_label_list = []
    for i in range(7, len(daily_user_behavior_list)):
        user_item_label_dict = {}
        # 召回
        for j in range(i - 7, i):
            daily_user_behavior_dict = daily_user_behavior_list[j][1]
            for behavior_type in daily_user_behavior_dict:
                if behavior_type != "1":
                    user_item_label_dict.update(dict(zip(list(daily_user_behavior_dict[behavior_type]), [0] * len(daily_user_behavior_dict[behavior_type]))))
                elif i - j == 1:
                    user_item_label_dict.update(dict(zip(list(daily_user_behavior_dict[behavior_type]), [0] * len(daily_user_behavior_dict[behavior_type]))))

        for key in daily_user_behavior_list[i][1]["4"]:
            if key in user_item_label_dict:
                user_item_label_dict[key] = 1

        date = daily_user_behavior_list[i][0]
        print >> sys.stderr, "%s" % (date)
        daily_user_item_label_list.append([date, user_item_label_dict])

    return daily_user_item_label_list

def get_offline_val_data(daily_user_behavior_list, item_subset):
    val_data = set()
    for date, user_behavior_dict in daily_user_behavior_list:
        if date != "20141218":
            continue

        user_items = user_behavior_dict["4"]
        for elem in user_items:
            userid, itemid = elem.split("_")
            if itemid not in item_subset:
                continue
            val_data.add(elem)
    return val_data

def main():
    print >> sys.stderr, "load item subset"
    item_subset = load_item_subset("./data/tianchi_fresh_comp_train_item.csv")
    print >> sys.stderr, "load user behavior"
    user_behavior_dict = load_user_behavior("./data/tianchi_fresh_comp_train_user.csv")
    daily_user_behavior_list = sorted(user_behavior_dict.items(), key = lambda (x, y): x)

    print >> sys.stderr, "get user item label"
    daily_user_item_label_list = get_user_item_label_data(daily_user_behavior_list)

    offline_val_data = get_offline_val_data(daily_user_behavior_list, item_subset)

    offline_train_fd = open("./data/offline_train.dat", "w")
    offline_test_fd = open("./data/offline_test.dat", "w")
    offline_evaluation_fd = open("./data/offline_val_dat", "w")

    online_train_fd = open("./data/online_train.dat", "w")
    online_test_fd = open("./data/online_test.dat", "w")

    for date, user_item_label_dict in daily_user_item_label_list:
        for key, label in user_item_label_dict.iteritems():
            if int(date) <= 20141217:
                print >> offline_train_fd, "%s\t%s\t%d" % (date, key, label)

            if int(date) > 20141125 and int(date) <= 20141218:
                print >> online_train_fd, "%s\t%s\t%d" % (date, key, label)

            if int(date) == 20141218:
                print >> offline_test_fd, "%s\t%s\t%d" % (date, key, label)

            if int(date) == 20141219:
                print >> online_test_fd, "%s\t%s\t%d" % (date, key, label)

    for elem in offline_val_data:
        print >> offline_evaluation_fd, elem

if __name__ == "__main__":
    main()

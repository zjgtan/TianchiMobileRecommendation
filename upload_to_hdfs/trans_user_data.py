import sys
import re

file_handler_dict = {}

path = sys.argv[1]

for ix, line in enumerate(sys.stdin):
    if ix == 0: continue
    toks = line.rstrip().split(",")
    date_str, hour = toks[-1].split(" ")
    date_str = re.sub("-", "", date_str)
    if date_str not in file_handler_dict:
        file_handler_dict[date_str] = open(path + "/tianchi_fresh_comp_train_user_%s.csv" % (date_str), "w")
    print >> file_handler_dict[date_str], ",".join(toks[:-1] + [hour])
    
    

#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>

import sys
import getopt
from Database import *
from patch import extract_patch,save_result
from ExtensionsManager import ExtensionsManager

def _get_extensions_manager(extensions):
    try:
        #print("Starting ExtensionsManager")
        emg = ExtensionsManager(extensions)
        return emg
    except Exception, e:
        print("Unknown extensions error: %s", (str(e),))
        sys.exit(1)

def main(argv):
    # Short (one letter) options. Those requiring argument followed by :
    short_opts = "u:p:d:r:s:e:t:c:n"
    # Long options (all started by --). Those requiring argument followed by =
    long_opts = ["db-user=", "db-password=",  "db-database=", "repository-id=", 
                 "start-time=", "end-time", "--changetype","--changepath",
                 "extensions=","understandfile=","statfile=","predictfile=",
                 "rankfile=","changemetricpath="]

    # Default options
    user = None
    passwd = None
    database = None
    repo_id=None
    start_time = None
    end_time = None
    change_type = None
    change_file_path = None
    extensions = None
    understand_file = None
    stat_file = None
    predict_file = None
    rank_file = None
    changemetric_file_path = None
    no_parse = False

    try:
        opts, args= getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError, e:
        print(str(e))
        return 1

    for opt, value in opts:
        if opt in("-u", "--db-user"):
            user = value
        elif opt in("-p", "--db-password"):
            passwd = value
        elif opt in("-d", "--db-database"):
            database = value
        elif opt in("-r", "--repository-id"):
            repo_id = value
        elif opt in("-s", "--start-time"):
            start_time = value
        elif opt in("-e","--end-time"):
            end_time = value
        elif opt in("-n"):
            no_parse = True
        elif opt in("-t","--changetype"):
            change_type = value
        elif opt in("-c","--changefile"):
            change_file_path = value
        elif opt in("--extensions", ):
            extensions = value.split(',')
        elif opt in("--understandfile"):
            understand_file = value
        elif opt in("--statfile"):
            stat_file = value
        elif opt in("--predictfile"):
            predict_file = value
        elif opt in("--rankfile"):
            rank_file = value
        elif opt in("--changemetricpath"):
            changemetric_file_path = value
    project_name = ""
    if repo_id=="1":
        project_name = "ant"
    elif repo_id=="2":
        project_name = "hibernate"
    elif repo_id=="3":
        project_name = "jedit"
    elif repo_id=="4":
        project_name = "eclipse"
    elif repo_id=="6":
        project_name = "spring"
    else:
        print "repository id not exist"
    
    try:
        db = Database(user, passwd, database)
        cnn = db.connect()
        cursor = cnn.cursor()
        if no_parse!=True:
            change_info = extract_patch(cursor,db,start_time,end_time,repo_id,change_type)
            save_result(change_info, change_file_path, change_type,project_name)
        cnn.close()
        if extensions!=None:
            emg = _get_extensions_manager(extensions)
            change_file = change_file_path+change_type+"_"+project_name+".csv"
            changemetric_file = changemetric_file_path+change_type+"_"+project_name+".csv"
            emg.run_extensions(change_file,understand_file,stat_file,rank_file,changemetric_file,predict_file,change_type)
#        print "Finish. Repository: "+ repo_id +", time: " + start_time+"-" +end_time+", bug: "+str(buggy) + ", Num_hunks: "+str(total_num_hunk)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])


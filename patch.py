#!/usr/bin/env python

import os
import re

def extract_patch(cursor,db,start_time,end_time,repo_id,change_type,file_path):
    if change_type=="bug":
        query = """select file_name,patch from patches,scmlog,files where patches.commit_id 
                 = scmlog.id and scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ? and is_bug_fix=1;"""
    else:
        query = """select file_name,patch from patches,scmlog,files where patches.commit_id 
                = scmlog.id and scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ?;"""
    db.execute_statement_with_param(query, (start_time, end_time, repo_id, "%.java"), cursor)
    file_patches = cursor.fetchall()
    change_info = "f"
    for i in range(0, len(file_patches)):
        filename = file_patches[i][0]
        patch = file_patches[i][1]
        change_number  = get_change_number(patch,change_type)
        change_info+=filename+","+str(change_number)+"\n"
    change_info_group = file_group(change_info)
    save_result(change_info_group,file_path,change_type,repo_id)

def get_change_number(patch,change_type):
    if change_type=="bug":
        return 1
    elif change_type=="time":
        return 1
    else:
        print patch
        num_addline = len(re.findall("(?<=\n)\+.*\n",patch)) - len(re.findall("(?<=\n)\+\+\+.*\n",patch))
        num_delline = len(re.findall("(?<=\n)\-.*\n",patch)) - len(re.findall("(?<=\n)\-\-\-.*\n",patch))
        return num_addline+num_delline

def file_group(change_info):
    change_info_files = re.split("\n", change_info)
    change_info_array = [ [0 for i in range(0,2)] for j in range(0,len(change_info_files)-1)]
    for i in range(0,len(change_info_files)-1):
        change_info_file = change_info_files[i]
        change_info_array[i][0] = re.split(",",change_info_file)[0]
        change_info_array[i][1] = re.split(",",change_info_file)[1]
    change_info_array.sort()
    change_info="file,change\n"
    previous_file = change_info_array[0][0]
    file = ""
    group_number = 0
    number = int(change_info_array[0][1])
    for i in range(1,len(change_info_array)):
        file = change_info_array[i][0]
        number = int(change_info_array[i][1])
        if file==previous_file:
            group_number+=number
        else:
            change_info+=previous_file+","+str(group_number)+"\n"
            group_number=number
        previous_file = file
    change_info+=previous_file+","+str(group_number)
    return change_info

def save_result(change_info_group, file_path, change_type,repo_id):
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
    if change_type=="bug":
        f = open(file_path+"bug_"+project_name+".csv",'w+',)
    elif change_type=="line":
        f = open(file_path+"line_"+project_name+".csv",'w+',)
    else:
        f = open(file_path+"time_"+project_name+".csv",'w+',)
    f.write(change_info_group+"\n")
    f.close
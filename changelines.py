#!/usr/bin/env python

import re

def get_change_line(cursor,db,start_datetime,end_datetime,repo_id,change_type):
    if change_type=="bug":
        query = """select file_name,patch,type from actions,patches,scmlog,files 
                where patches.file_id=actions.file_id and patches.commit_id
                =actions.commit_id and patches.commit_id = scmlog.id and 
                scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ? and is_bug_fix=1;"""
    else:
        query = """select file_name,patch,type from actions,patches,scmlog,files 
                where patches.file_id=actions.file_id and patches.commit_id
                =actions.commit_id and patches.commit_id = scmlog.id and 
                scmlog.commit_date >= ? and scmlog.commit_date < ?
                and scmlog.repository_id=? and patches.file_id=files.id and 
                file_name like ?"""
    db.execute_statement_with_param(query, (start_datetime, end_datetime, repo_id, "%.java"), cursor)
    file_patches = cursor.fetchall()
    change_info = ""
    for i in range(0, len(file_patches)):
        filename = file_patches[i][0]
        patch = file_patches[i][1]
        action_type = file_patches[i][2]
        if action_type=="M":
            change_number  = get_change_number(patch,change_type)
            change_info+=filename+","+str(change_number)+"\n"
    change_info_group = file_group(change_info)
    #save_result(change_info_group,change_file_path,change_type,project_name)
    return change_info_group

def get_change_number(patch,change_type):
    if change_type=="bug":
        return 1
    elif change_type=="time":
        return 1
    else:
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
    curfile = ""
    group_number = 0
    number = int(change_info_array[0][1])
    for i in range(1,len(change_info_array)):
        curfile = change_info_array[i][0]
        number = int(change_info_array[i][1])
        if curfile==previous_file:
            group_number+=number
        else:
            change_info+=previous_file+","+str(group_number)+"\n"
            group_number=number
        previous_file = curfile
    change_info+=previous_file+","+str(group_number)
    return change_info
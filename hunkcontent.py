#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>

import re
from exporthunk import save_change_to_file

#def save_hunk_to_database(commit_id, hunk, old_hunk, new_hunk, db, cursor):
#    query = "insert into hunk_content(commit_id, content, old_content, new_content) values(?, ?, ?, ?)"
#    db.execute_statement_with_param(query, (commit_id, hunk, old_hunk, new_hunk),cursor)
    
    
def parse_patch_content(patch_content, m, filepath):
    file_patch_split = re.split("@@.*@@", patch_content)
    leng = len(file_patch_split)
    for i in range(1,leng): 
        hunk = file_patch_split[i]
        old_hunk = re.sub('(?<=\n)\+.*\n','',hunk)
        old_hunk = re.sub("\n\-","\n ",old_hunk)
        new_hunk = re.sub('(?<=\n)\-.*\n','',hunk)
        new_hunk = re.sub("\n\+","\n ",new_hunk)
        save_change_to_file(hunk, old_hunk, new_hunk, m, filepath)
        m=m+1
    return m
            
    
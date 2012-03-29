#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


import getopt
import os
import glob
import re
import sys
from extensions import (Extension, register_extension, 
    ExtensionRunError)
class Metrics(object):
    def __init__(self):
            self.authors = {}
    def get_change_info(self,change_file):
        for infile in glob.glob(change_file):
            change_info = open(infile, 'r').read()
            change_info_split = re.split("\n", change_info)
            change_info_array = [[0 for i in range(0, 2)] for j in range(0, len(change_info_split)-2)]
            
        for i in range(0, len(change_info_split)-2):
            change_info_line = re.split(",", change_info_split[i+1])
            change_info_array[i][0] = change_info_line[0]
            change_info_array[i][1] = change_info_line[1]
        return change_info_array
    
    def get_understand_metric(self,file):
        for infile in glob.glob(os.path.join(file + '.csv')):
            understand_metric = open(infile, 'r').read()
            understand_metric_split = re.split("\n", understand_metric)
            file_number=  0
            for i in range(0, len(understand_metric_split)):
                understand_metric_line = re.split(",", understand_metric_split[i])
                kind = understand_metric_line[0]
                if kind=="File":
                    file_number+=1       
            understand_metric_array = [["" for i in range(0, 3)] for j in range(0, file_number)]
            understand_metric_name = ""
            understand_metric_line = re.split(",",understand_metric_split[0])
            for i in range(3,54):
                if i not in(11,12,13,17,22,27,34,35,40,41,42,43,47,48,49):
                    understand_metric_name += understand_metric_line[i]+","
            understand_metric_name += "SumEssential"
            file_number = 0
            for i in range(1, len(understand_metric_split)):
                understand_metric_line = re.split(",", understand_metric_split[i])
                kind = understand_metric_line[0]
                if kind=="File":
                    filefullname = understand_metric_line[2]
                    filefullnameparts = re.split("/",filefullname)
                    filename = filefullnameparts[len(filefullnameparts)-1]
                    metric_info = ""
                    for j in range(3,54):
                        if j not in(11,12,13,17,22,27,34,35,40,41,42,43,47,48,49):
                            metric_info += understand_metric_line[j]+","
                    metric_info += understand_metric_line[54]
                    understand_metric_array[file_number][0] = filename
                    understand_metric_array[file_number][1] = filefullname
                    understand_metric_array[file_number][2] = metric_info
                    file_number += 1
        return (understand_metric_array,understand_metric_name)
    
    def get_stat_metric(self,file):
        for infile in glob.glob( os.path.join(file+'.txt')):
            totalstat = open(infile,'r').read()
            filestats = re.split(".+File Statistics.+\n", totalstat)
            stat_metric_array = [["" for i in range(0, 3)] for j in range(0, len(filestats)-1)]
            stat_metric_name = "Totalline,Commentline,Blankline,FuncDecl,Func,DeclStmt,Decl,Block,Call,Continue,Break,Return,For,If,Else,While,Do,Switch,Case,Param,Argu,Assign,ZeroOpAssign,ZeroOpcallAssign,ConstAssign,Class,Constructor,Try,Catch,Throw"
            for i in range(0,len(filestats)-1):
                filestat = filestats[i+1]
                lines = re.split("\n",filestat)
                ffullname = lines[1]
                filefullname = ffullname[15:len(ffullname)-4]
                filefullnameparts = re.split("/",filefullname)
                filename = filefullnameparts[len(filefullnameparts)-1]
                stat_info = ""
                for j in range(3,len(lines)-4):
                    line = lines[j]
                    if line!="" and j not in(11,12,24,26,32,33,34,35,36):
                        number = re.split(": ",line)[1]
                        stat_info=stat_info+number+","
                line = lines[len(lines)-4]#after the last number, there is no ","
                number = re.split(": ",line)[1]
                stat_info+=number
                stat_metric_array[i][0] = filename
                stat_metric_array[i][1] = filefullname
                stat_metric_array[i][2] = stat_info
        return (stat_metric_array,stat_metric_name)
    
    def get_rank_metric(self,file):
        for infile in glob.glob(os.path.join(file + '.csv')):
            rank_metric = open(infile, 'r').read()
            rank_metric_split = re.split("\n", rank_metric)
            num_files = len(rank_metric_split) - 1    
            rank_metric_array = [["" for i in range(0, 3)] for j in range(0, num_files)]
            rank_metric_name = ""
            rank_metric_line = re.split(",",rank_metric_split[0])
            for i in range(1,10):
                rank_metric_name += rank_metric_line[i]+","
            rank_metric_name += "OutReference"
            file_number = -1
            for i in range(1, num_files):
                rank_metric_line = re.split(",", rank_metric_split[i])
                filefullname = rank_metric_line[0]
                filefullnameparts = re.split("/",filefullname)
                filename = filefullnameparts[len(filefullnameparts)-1]
                metric_info = ""
                for j in range(1,10):
                    metric_info += rank_metric_line[j]+","
                metric_info += rank_metric_line[10]
                rank_metric_array[file_number][0] = filename
                rank_metric_array[file_number][1] = filefullname
                rank_metric_array[file_number][2] = metric_info
                file_number += 1
        return (rank_metric_array,rank_metric_name)
    def get_change_metric(self,file):
        for infile in glob.glob(file):
            change_metric = open(infile, 'r').read()
            change_metric_split = re.split("\n", change_metric)
            change_metric_array = [[0 for i in range(0, 2)] for j in range(0, len(change_metric_split)-2)]
            
        for i in range(0, len(change_metric_split)-2):
            change_metric_line = re.split(",", change_metric_split[i+1])
            change_metric_array[i][0] = change_metric_line[0]
            change_metric_array[i][1] = change_metric_line[1]
        return change_metric_array
    def find_metric_info(self,filename,pathname,change_info,rank_metric,change_metric):
            num_change = len(change_info)
            num_rank = len(rank_metric)
            num_oldchange = len(change_metric)
            change = "0"
            rank_info = "0,0,0,0,0,0,0"
            oldchange = "0"
            for j in range(0,num_change):
                if change_info[j][0]==filename:
                    change = change_info[j][1]
                    break
            for k in range(0,num_rank):
                if rank_metric[k][1] == pathname:
                    rank_info = rank_metric[k][2]
                    break
            for j in range(0,num_oldchange):
                if change_metric[j][0]==filename:
                    oldchange = change_metric[j][1]
                    break
            return change,rank_info,oldchange
                
    def save_predict_file(self,change_info,understand_metric,stat_metric,rank_metric,change_metric,predict_file,predict_metric_name,change_type):
        understand_metric.sort()
        stat_metric.sort()
        rank_metric.sort()
        change_info.sort()
        change_metric.sort()
        num_understand_metric = len(understand_metric)
        predict_info = predict_metric_name+"\n"
        for i in range(0,num_understand_metric):
            filename = understand_metric[i][0]
            if i==0:
                if filename!=understand_metric[1][0]:
                    pathname = understand_metric[i][1]
                    (change,rank_info,oldchange) = self.find_metric_info(filename, pathname, change_info, rank_metric,change_metric)
                    predict_info += filename+","+pathname+","+change+","+oldchange+","+rank_info+","+stat_metric[i][2]+","+understand_metric[i][2]+"\n"
            elif i==num_understand_metric-1:
                if filename!=understand_metric[num_understand_metric-1][0]:
                    pathname = understand_metric[i][1]
                    (change,rank_info,oldchange) = self.find_metric_info(filename, pathname, change_info, rank_metric,change_metric)
                    predict_info += filename+","+pathname+","+change+","+oldchange+","+rank_info+","+stat_metric[i][2]+","+understand_metric[i][2]+"\n"
            elif filename!=understand_metric[i-1][0] and filename!=understand_metric[i+1][0]:
                pathname = understand_metric[i][1]
                (change,rank_info,oldchange) = self.find_metric_info(filename, pathname, change_info, rank_metric,change_metric)
                predict_info += filename+","+pathname+","+change+","+oldchange+","+rank_info+","+stat_metric[i][2]+","+understand_metric[i][2]+"\n"
        f = open(predict_file+"_"+change_type+".csv",'w+',)
        f.write(predict_info)
        f.close
    def run(self,change_file,understand_file,stat_file,rank_file,changemetric_file,predict_file,change_type):
        change_info = self.get_change_info(change_file)        
        (understand_metric,understand_metric_name) = self.get_understand_metric(understand_file)
        (stat_metric,stat_metric_name) = self.get_stat_metric(stat_file)
        (rank_metric,rank_metric_name) = self.get_rank_metric(rank_file)
        change_metric = self.get_change_metric(changemetric_file)
        predict_metric_name = "File,Path,Change,Oldchange,"+rank_metric_name+","+stat_metric_name+","+understand_metric_name
        self.save_predict_file(change_info,understand_metric,stat_metric,rank_metric,change_metric,predict_file,predict_metric_name,change_type)
register_extension("Metrics", Metrics)
        
        
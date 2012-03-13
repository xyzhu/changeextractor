# Copyright (C) 2007 LibreSoft
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors :
#       Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>

import MySQLdb

class Database():

    place_holder = "%s"

    def __init__(self, username, password, database):
        self.username = username
        self.password = password
        self.database = database

    def connect(self):

        try:
            return MySQLdb.connect("localhost",self.username, 
                               self.password, self.database)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
  
    def statement(self, query, ph_mark):
        if "?" == ph_mark or "?" not in query:
            return query
    
        query = query.replace("?", ph_mark)
        return query
        #tokens = query.split("'")
        #for i in range(0, len(tokens), 2):
         #   tokens[i] = tokens[i].replace("?", ph_mark)
    
        #retval = "'".join(tokens)
    
        #return retval          

    def create_tables(self, cursor):

        try:
            cursor.execute ("DROP TABLE IF EXISTS hunk_content")
            cursor.execute ("""
              CREATE TABLE hunk_content
              (
                id            INT NOT NULL AUTO_INCREMENT,
                commit_id     CHAR(10),
                content       longtext,
                old_content   longtext,
                new_content   longtext,
                PRIMARY KEY (id)
              );
            """)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


    # Useful DB utility functions
    def execute_statement_with_param(self, query, parameters, cursor):
        """Run a statement. Note that the cursor is *mutable*, and will contain
            the results after running.
        """
    
        try:
            return cursor.execute(self.statement(query, self.place_holder), parameters)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            
    def execute_statement(self, query, cursor):
        """Run a statement. Note that the cursor is *mutable*, and will contain
            the results after running.
        """
    
        try:
            return cursor.execute(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

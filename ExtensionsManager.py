# Copyright (C) 2008 LibreSoft
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

from extensions import (get_extension, ExtensionRunError, 
                        ExtensionUnknownError, ExtensionBackoutError)
from utils import printerr, printout, printdbg


class ExtensionException(Exception):
    '''ExtensionException'''


class InvalidExtension(ExtensionException):
    def __init__(self, name):
        self.name = name


class InvalidDependency(ExtensionException):
    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2
 
       
class ExtensionsManager(object):

    def __init__(self, exts):
        self.exts = {}

        for ext in exts:
            name = ext  
            try:
                self.exts[name] = get_extension(ext)
            except ExtensionUnknownError:
                raise InvalidExtension(ext)
                        
    def run_extension(self, name, extension, change_file,understand_file,stat_file,rank_file,changemetric_file,predict_file,change_type):
        # Trim off the ordering numeral before printing

        try:
            extension.run(change_file,understand_file,stat_file,rank_file,changemetric_file,predict_file,change_type)
        except ExtensionRunError, e:
            printerr("Error running extension %s: %s", (name, str(e)))
            return False
        return True
                     
    def run_extensions(self, change_file,understand_file,stat_file,rank_file,changemetric_file,predict_file,change_type):
        list = sorted(self.exts)
           
        for name, extension in [(ext, self.exts[ext]()) for ext in list]:
            self.run_extension(name, extension, change_file,understand_file,stat_file,rank_file,changemetric_file,predict_file,change_type)
            